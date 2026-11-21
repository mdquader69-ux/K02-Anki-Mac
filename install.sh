#!/bin/bash
pip3 install hidapi
cp k02_anki.py ~/k02_anki.py
REAL_PY=$(python3 -c "import sys; print(sys.executable)")
mkdir -p ~/Library/LaunchAgents
sed -e "s|/Users/YOUR_USERNAME|$HOME|g" -e "s|/Library/Developer/CommandLineTools/usr/bin/python3|$REAL_PY|g" com.user.k02anki.plist > ~/Library/LaunchAgents/com.user.k02anki.plist
launchctl load ~/Library/LaunchAgents/com.user.k02anki.plist 2>/dev/null
launchctl kickstart -k gui/$(id -u)/com.user.k02anki
echo "Done! Add $REAL_PY to System Settings > Privacy & Security > Input Monitoring & Accessibility."
