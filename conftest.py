import glob
from pathlib import Path
import os
import subprocess
import time
import socket
import shutil
from urllib.parse import urlparse
import json
import re
from datetime import datetime

import pytest
from appium import webdriver
from appium.options.common import AppiumOptions


ARTIFACTS_DIR = Path("artifacts")


def _slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_.-]+", "_", s)
    return s.strip("_")[:180] if s else "unknown"


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _run_cmd_to_file(cmd: list[str], out_path: Path, timeout: int = 20) -> None:
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out_path.write_text(
            (res.stdout or "") + ("\n" + res.stderr if res.stderr else ""),
            encoding="utf-8",
        )
    except Exception as e:
        out_path.write_text(f"FAILED to run command: {cmd}\n{e}\n", encoding="utf-8")


def _collect_failure_artifacts(
    *,
    platform: str,
    nodeid: str,
    driver,
    appium_log_path: Path | None,
) -> Path:
    test_dir = ARTIFACTS_DIR / platform / f"{_slug(nodeid)}__{_now_stamp()}"
    test_dir.mkdir(parents=True, exist_ok=True)

    # 1) Screenshot
    try:
        driver.save_screenshot(str(test_dir / "screenshot.png"))
    except Exception as e:
        (test_dir / "screenshot_error.txt").write_text(str(e), encoding="utf-8")

    # 2) Page source
    try:
        (test_dir / "page_source.xml").write_text(driver.page_source or "", encoding="utf-8")
    except Exception as e:
        (test_dir / "page_source_error.txt").write_text(str(e), encoding="utf-8")

    # 3) Capabilities
    try:
        caps = getattr(driver, "capabilities", None) or {}
        (test_dir / "driver_caps.json").write_text(
            json.dumps(caps, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    except Exception as e:
        (test_dir / "caps_error.txt").write_text(str(e), encoding="utf-8")

    # 4) Appium server log (only if *we* started it)
    try:
        if appium_log_path and appium_log_path.exists():
            (test_dir / "appium_server.log").write_text(
                appium_log_path.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
    except Exception as e:
        (test_dir / "appium_log_error.txt").write_text(str(e), encoding="utf-8")

    # 5) Platform-specific logs
    if platform == "android":
        _run_cmd_to_file(["adb", "devices", "-l"], test_dir / "adb_devices.txt")
        _run_cmd_to_file(["adb", "logcat", "-d", "-v", "time"], test_dir / "logcat.txt", timeout=30)

    if platform == "ios":
        _run_cmd_to_file(["xcrun", "simctl", "list", "devices", "booted"], test_dir / "simctl_booted_devices.txt")
        _run_cmd_to_file(
            ["xcrun", "simctl", "spawn", "booted", "log", "show", "--style", "syslog", "--last", "2m"],
            test_dir / "sim_log_last_2m.txt",
            timeout=30,
        )

    return test_dir


def _is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host, port)) == 0


@pytest.fixture(scope="session", autouse=True)
def appium_server(request, appium_url):
    selected_platform = request.config.getoption("--platform")

    # Do not start Appium for web-only runs
    if selected_platform not in {"ios", "android"}:
        os.environ["PYTEST_APPIUM_LOG_PATH"] = ""
        yield
        return
    
    """
    Start Appium automatically for the test session if it's not already running.
    """
    parsed = urlparse(appium_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 4723

    # If already running, do nothing (and mark that we don't own a log file)
    if _is_port_open(host, port):
        print(f"Appium already running on {host}:{port}")
        os.environ["PYTEST_APPIUM_LOG_PATH"] = ""
        yield
        return

    appium_bin = shutil.which("appium")
    if not appium_bin:
        pytest.fail("Could not find 'appium' in PATH. (Try: `which appium` in this same terminal)")

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    appium_log_path = ARTIFACTS_DIR / "appium_server_session.log"

    cmd = [
        appium_bin,
        "--address", host,
        "--port", str(port),
        "--base-path", "/wd/hub",
        "--relaxed-security",
        "--allow-insecure", "shutdown_other_sims,shutdown_simulator",
    ]

    print(f"Starting Appium: {' '.join(cmd)}")
    log_f = open(appium_log_path, "w", encoding="utf-8")

    process = subprocess.Popen(
        cmd,
        stdout=log_f,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # expose to other fixtures/hooks
    os.environ["PYTEST_APPIUM_LOG_PATH"] = str(appium_log_path)

    # Wait up to 30s for port to open OR Appium to exit
    for _ in range(30):
        if _is_port_open(host, port):
            print(f"Appium is up on {host}:{port}")
            break
        if process.poll() is not None:
            try:
                log_f.close()
            except Exception:
                pass
            pytest.fail(
                f"Appium exited immediately (exit code {process.returncode}). "
                f"See {appium_log_path.resolve()} for details."
            )
        time.sleep(1)
    else:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        try:
            log_f.close()
        except Exception:
            pass
        pytest.fail(f"Appium did not start (port never opened). See {appium_log_path.resolve()}")

    yield

    print("Stopping Appium server...")
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
    try:
        log_f.close()
    except Exception:
        pass


def _find_ios_app_path(app_name: str = "CalculMath.app") -> str | None:
    pattern = os.path.expanduser(
        f"~/Library/Developer/Xcode/DerivedData/**/Build/Products/Debug-iphonesimulator/{app_name}"
    )
    matches = glob.glob(pattern, recursive=True)
    if not matches:
        return None
    matches.sort(key=lambda p: Path(p).stat().st_mtime, reverse=True)
    return matches[0]


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default=os.getenv("PLATFORM", "ios"),
        choices=["ios", "android", "web"],
        help="Target platform: ios, android, or web (can also be set via PLATFORM env var).",
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


@pytest.fixture(scope="function")
def driver(request, platform: str, appium_url: str, appium_server):
    """Creates an Appium session per test for the requested platform."""

    opts = AppiumOptions()
    terminate_id: str | None = None

    if platform == "android":
        app_package = os.getenv("ANDROID_APP_PACKAGE", "com.google.android.calculator")
        app_activity = os.getenv("ANDROID_APP_ACTIVITY", "com.android.calculator2.Calculator")

        opts.load_capabilities(
            {
                "platformName": "Android",
                "appium:automationName": "UiAutomator2",
                "appium:deviceName": os.getenv("ANDROID_DEVICE", "Pixel"),
                **({"appium:platformVersion": os.getenv("ANDROID_VERSION")} if os.getenv("ANDROID_VERSION") else {}),
                **({"appium:udid": os.getenv("ANDROID_UDID")} if os.getenv("ANDROID_UDID") else {}),
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

    # ✅ attach to the test node so the failure hook can grab it
    request.node._driver = drv
    request.node._platform = platform

    try:
        yield drv
    finally:
        if terminate_id:
            try:
                drv.terminate_app(terminate_id)
            except Exception:
                pass
        try:
            drv.quit()
        except Exception:
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Collect artifacts for failures in setup/call
    if rep.when not in ("setup", "call"):
        return
    if not rep.failed:
        return

    drv = getattr(item, "_driver", None)
    platform = getattr(item, "_platform", None) or "unknown"
    if not drv:
        return

    log_path_str = os.environ.get("PYTEST_APPIUM_LOG_PATH", "")
    appium_log_path = Path(log_path_str) if log_path_str else None

    out_dir = _collect_failure_artifacts(
        platform=platform,
        nodeid=item.nodeid,
        driver=drv,
        appium_log_path=appium_log_path,
    )

    print(f"\n[artifacts] Saved failure artifacts to: {out_dir}\n")