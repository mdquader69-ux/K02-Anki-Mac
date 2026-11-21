# K02 Bluetooth TikTok Ring -> Anki Mapper for macOS

A lightweight Python background daemon that maps Bluetooth scrolling rings (**K02**, `VID: 1452, PID: 544`) to **Anki** shortcuts on macOS—without Karabiner-Elements, Hammerspoon, or BetterTouchTool.

## Default Button Mapping
- **Camera / Shutter:** `Spacebar` (Show Answer / Rate Good)
- **Up:** `1` (Again)
- **Down:** `2` (Hard)
- **Center:** `3` (Good)
- **Right:** `4` (Easy)
- **Left:** `Command + Z` (Undo)

## Installation
1. Pair your **K02 Ring** in **System Settings > Bluetooth**.
2. Open **Terminal** in this folder and run `./install.sh`.
3. Add the Python path printed in Terminal to **System Settings > Privacy & Security > Input Monitoring** and **Accessibility**.
4. Restart the service: `launchctl kickstart -k gui/$(id -u)/com.user.k02anki`

## Adapting to Other Rings
Run `python3 -c "import hid; [print(d['product_string'], d['vendor_id'], d['product_id']) for d in hid.enumerate()]"` to find your ring's VID/PID and update `1452, 544` in `k02_anki.py`.
