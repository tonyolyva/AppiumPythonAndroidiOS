import glob
from pathlib import Path
import os
import subprocess
import time
import socket
import pytest
from appium import webdriver
from appium.options.common import AppiumOptions


def _is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host, port)) == 0


from urllib.parse import urlparse
import shutil

@pytest.fixture(scope="session", autouse=True)
def appium_server(appium_url):
    """
    Start Appium automatically for the test session if it's not already running.
    """
    parsed = urlparse(appium_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 4723

    if _is_port_open(host, port):
        print(f"Appium already running on {host}:{port}")
        yield
        return

    appium_bin = shutil.which("appium")
    if not appium_bin:
        pytest.fail("Could not find 'appium' in PATH (but your `which appium` suggests it should be).")

    log_path = Path("appium_server.log")
    log_file = log_path.open("w")

    cmd = [
        appium_bin,
        "--address", host,
        "--port", str(port),
        "--base-path", "/wd/hub",
        "--relaxed-security",
        "--allow-insecure", "shutdown_other_sims,shutdown_simulator",
    ]

    print(f"Starting Appium: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # Wait up to 30s for port to open OR Appium to exit
    for _ in range(30):
        if _is_port_open(host, port):
            print(f"Appium is up on {host}:{port}")
            break
        if process.poll() is not None:
            log_file.close()
            pytest.fail(
                f"Appium exited immediately (exit code {process.returncode}). "
                f"See {log_path.resolve()} for details."
            )
        time.sleep(1)
    else:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        log_file.close()
        pytest.fail(f"Appium did not start (port never opened). See {log_path.resolve()}")

    yield

    print("Stopping Appium server...")
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
    log_file.close()


def _find_ios_app_path(app_name: str = "CalculMath.app") -> str | None:
    """
    Try to locate a built Simulator .app in Xcode DerivedData.
    Looks for: */Build/Products/Debug-iphonesimulator/<app_name>
    """
    pattern = os.path.expanduser(
        f"~/Library/Developer/Xcode/DerivedData/**/Build/Products/Debug-iphonesimulator/{app_name}"
    )
    matches = glob.glob(pattern, recursive=True)

    # Prefer newest build if multiple exist
    if not matches:
        return None
    matches.sort(key=lambda p: Path(p).stat().st_mtime, reverse=True)
    return matches[0]


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default=os.getenv("PLATFORM", "ios"),
        choices=["ios", "android"],
        help="Target platform: ios or android (can also be set via PLATFORM env var).",
    )
    parser.addoption(
        "--appium-url",
        action="store",
        default=os.getenv("APPIUM_URL", "http://127.0.0.1:4723/wd/hub"),
        help="Appium server URL (can also be set via APPIUM_URL env var).",
    )


@pytest.fixture(scope="session")
def platform(request) -> str:
    return request.config.getoption("--platform")


@pytest.fixture(scope="session")
def appium_url(request) -> str:
    url = request.config.getoption("--appium-url")
    # If user provided just host:port, assume /wd/hub
    if url.endswith(":4723") or url.endswith(":4723/"):
        url = url.rstrip("/") + "/wd/hub"
    return url


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        pytest.fail(f"Missing required environment variable: {name}")
    return value


@pytest.fixture(scope="function")
def driver(platform: str, appium_url: str, appium_server):
    """Creates an Appium session per test for the requested platform."""

    opts = AppiumOptions()
    terminate_id: str | None = None

    if platform == "android":
        # Android: Pixel + Google Calculator
        app_package = os.getenv("ANDROID_APP_PACKAGE", "com.google.android.calculator")
        app_activity = os.getenv("ANDROID_APP_ACTIVITY", "com.android.calculator2.Calculator")

        opts.load_capabilities(
            {
                "platformName": "Android",
                "appium:automationName": "UiAutomator2",
                "appium:deviceName": os.getenv("ANDROID_DEVICE", "Pixel"),
                # Provide ANDROID_VERSION only if you want to lock it. Otherwise omit.
                **(
                    {"appium:platformVersion": os.getenv("ANDROID_VERSION")}
                    if os.getenv("ANDROID_VERSION")
                    else {}
                ),
                **(
                    {"appium:udid": os.getenv("ANDROID_UDID")}
                    if os.getenv("ANDROID_UDID")
                    else {}
                ),
                "appium:appPackage": app_package,
                "appium:appActivity": app_activity,
                "appium:noReset": True,
                "appium:newCommandTimeout": int(os.getenv("APPIUM_NEW_COMMAND_TIMEOUT", "120")),
            }
        )
        terminate_id = app_package

    else:
        app_path = os.getenv("IOS_APP_PATH") or _find_ios_app_path("CalculMath.app")
        if not app_path or not os.path.exists(app_path):
            pytest.fail(
                "Set IOS_APP_PATH or build CalculMath for Simulator so it exists in DerivedData at "
                "Build/Products/Debug-iphonesimulator/CalculMath.app. "
                f"Got: {app_path}"
            )

        bundle_id = os.getenv("IOS_BUNDLE_ID", "com.example.CalculMath")

        caps = {
            "platformName": "iOS",
            "appium:automationName": "XCUITest",
            "appium:deviceName": os.getenv("IOS_DEVICE", "iPhone 14 Pro"),
            "appium:app": app_path,
            "appium:noReset": False,
            "appium:newCommandTimeout": int(os.getenv("APPIUM_NEW_COMMAND_TIMEOUT", "120")),
        }

        if os.getenv("IOS_SHUTDOWN_SIMULATOR") == "1":
            caps["appium:shutdownOtherSimulators"] = True
            caps["appium:shutdownSimulator"] = True

        if os.getenv("IOS_VERSION"):
            caps["appium:platformVersion"] = os.getenv("IOS_VERSION")
        if os.getenv("IOS_UDID"):
            caps["appium:udid"] = os.getenv("IOS_UDID")

        opts.load_capabilities(caps)
        terminate_id = bundle_id


    drv = webdriver.Remote(appium_url, options=opts)
    try:
        yield drv
    finally:
        # terminate_app expects Android package or iOS bundle id
        if terminate_id:
            try:
                drv.terminate_app(terminate_id)
            except Exception:
                pass
        try:
            drv.quit()
        except Exception:
            pass
