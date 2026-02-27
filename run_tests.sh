#!/bin/bash

echo "📡 Checking if Appium is running..."
if nc -z localhost 4723; then
  echo "✅ Appium already running"
  appium_was_running=true
else
  echo "🚀 Appium not running — launching..."

  appium_script_path="/tmp/start_appium.sh"

  cat > "$appium_script_path" <<EOF
#!/bin/bash
cd /Users/Yutaka/Workspace/AppiumPythonProject
/usr/local/bin/appium
EOF

  chmod +x "$appium_script_path"

  echo "🖥 Launching Appium in detached Terminal window..."
  open -a Terminal "$appium_script_path"

  sleep 10
  appium_was_running=false
fi

echo "🧪 Running tests..."
/Library/Frameworks/Python.framework/Versions/3.13/bin/pytest -v --html=reports/report.html --self-contained-html
test_result=$?

if [ "$appium_was_running" = false ]; then
  echo "🛑 Stopping Appium"
  kill $(lsof -ti:4723) || true
fi

exit $test_result