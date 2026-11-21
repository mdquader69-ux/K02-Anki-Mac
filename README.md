# K02 Bluetooth TikTok Ring → Anki Mapper for macOS

Use a cheap **K02 Bluetooth scrolling/TikTok ring** (`VID: 1452, PID: 544`) to review **Anki** cards hands-free on macOS—with **zero paid apps** and **no Karabiner-Elements, Hammerspoon, or BetterTouchTool** required.

---

## Why Standard Remappers Fail on macOS
Most Bluetooth scrolling rings send raw **HID Digitizer / Touchscreen (`Usage Page 13`)** swipe and pinch packets for their directional buttons. Because macOS does not have a touchscreen driver, the OS silently drops `Usage Page 13` events—meaning Karabiner-Elements and standard mouse remappers only see the Camera/Shutter button and completely ignore Up, Down, Left, and Right.

This lightweight Python background service reads the raw `Usage Page 13` HID packets directly via `hidapi` and sends Anki keyboard shortcuts **only when Anki is your active window**.

---

## Button Layout in Anki

| K02 Ring Button | Key Sent | Anki Action |
| :--- | :---: | :--- |
| **Camera / Shutter** | `Spacebar` | **Show Answer** / Rate **Good** |
| **Up** | `1` | Rate **Again** |
| **Down** | `2` | Rate **Hard** |
| **Center** | `3` | Rate **Good** |
| **Right** | `4` | Rate **Easy** |
| **Left** | `Command + Z` | **Undo** *(works on all card types, including Type-in-the-Answer)* |

> **Note:** On **Type-in-the-Answer** cards, press the **Camera button (`Spacebar`)** first to submit/reveal the answer before pressing `1`, `2`, `3`, or `4`.

---

## Step-by-Step Setup Guide (5 Minutes)

### Step 1: Pair Your K02 Ring
1. Turn on your K02 ring.
2. On your Mac, open **System Settings → Bluetooth**, find **K02**, and click **Connect**.
3. *(Important)* If you previously installed **Karabiner-Elements** or **Hammerspoon**, either uninstall them or turn **OFF** *"Modify events"* for K02 in Karabiner—otherwise Karabiner locks the device and blocks Python from reading it.

---

### Step 2: Download & Run the Installer
1. On this GitHub page, click the green **`<> Code`** button → **Download ZIP**, and unzip it into your **Downloads** folder.
2. Open **Terminal** (`Command + Space` → type `Terminal` → press `Enter`).
3. Run these commands one line at a time:
   ```bash
   cd ~/Downloads/K02-Anki-Mac-main
   chmod +x install.sh
   ./install.sh
   ```
4. Look at the last line printed in Terminal—it will show your Mac's exact Python path, for example:
   ```text
   Done! Add /Library/Developer/CommandLineTools/usr/bin/python3 to System Settings...
   ```
   *(Copy or note down that exact path—you will need it in Step 3!)*

---

### Step 3: Grant macOS Permissions (Required Once)
macOS blocks background scripts from reading Bluetooth HID devices or sending keystrokes until you allow your Python binary:

1. **Allow Input Monitoring:**
   * Open **System Settings → Privacy & Security → Input Monitoring**.
   * Click the **`+`** button at the bottom.
   * Press **`Command + Shift + G`**, paste the exact Python path from Step 2 (e.g., `/Library/Developer/CommandLineTools/usr/bin/python3`), press `Enter`, and click **Open**.
   * Make sure the toggle next to `python3` is **ON**.

2. **Allow Accessibility:**
   * Go back to **System Settings → Privacy & Security → Accessibility**.
   * Click the **`+`** button at the bottom.
   * Press **`Command + Shift + G`**, paste that **same Python path**, press `Enter`, and click **Open**.
   * Make sure the toggle next to `python3` is **ON**.

---

### Step 4: Start the Background Service
Back in **Terminal**, run this single command to restart the background service with your new permissions:
```bash
launchctl kickstart -k gui/\$(id -u)/com.user.k02anki
```
You can now **quit Terminal (`Command + Q`)**. The script runs silently in the background, starts automatically every time you turn on your Mac, and reconnects automatically whenever your ring wakes up from sleep.

---

## Troubleshooting

* **Nothing happens when pressing buttons in Anki:**
  * Make sure **Anki** is the active frontmost window (the script ignores presses in other apps so it never types random numbers while you browse).
  * Double-check that you added the **real Python binary** (such as `/Library/Developer/CommandLineTools/usr/bin/python3`) and not just the `/usr/bin/python3` shim to **both** *Input Monitoring* and *Accessibility*.
  * Run `launchctl kickstart -k gui/$(id -u)/com.user.k02anki` in Terminal after changing permissions.

* **`OSError: open failed` when testing in Terminal:**
  * Another app (like Karabiner-Elements or the background service itself) is currently holding the ring. Stop the background service first with:
    ```bash
    launchctl unload ~/Library/LaunchAgents/com.user.k02anki.plist
    ```

* **Using a Different Bluetooth Ring (Not K02):**
  1. Run this in Terminal to see your ring's Vendor ID (`VID`) and Product ID (`PID`):
     ```bash
     python3 -c "import hid; [print(d['product_string'], d['vendor_id'], d['product_id'], d['usage_page']) for d in hid.enumerate()]"
     ```
  2. Replace `1452, 544` in `~/k02_anki.py` with your ring's `vendor_id` and `product_id`, then restart the service.

---

## How to Uninstall
If you ever want to stop the background service and remove all files:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.k02anki.plist 2>/dev/null
rm -f ~/Library/LaunchAgents/com.user.k02anki.plist ~/k02_anki.py
```
