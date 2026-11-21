import hid, subprocess, time
def send_key(k):
    m = " using command down" if k == 6 else ""
    s = f'tell application "System Events" to if name of (first application process whose frontmost is true) is "Anki" then key code {k}{m}'
    subprocess.run(("osascript", "-e", s))
KEYS = dict(UP=18, DOWN=19, CENTER=20, LEFT=6, RIGHT=21, CAMERA=49)
while True:
    try:
        paths = tuple(x.get("path") for x in hid.enumerate(1452, 544) if x["usage_page"] == 13)
        if not paths:
            time.sleep(2)
            continue
        d = hid.device()
        d.open_path(paths.__getitem__(0))
        sx, sy, last_t = None, None, 0
        while True:
            raw = d.read(64, 500)
            if not raw: continue
            r, now = tuple(raw), time.time()
            if r == (1, 64, 0) and now - last_t > 0.3:
                send_key(KEYS.get("CAMERA")); last_t = now
            elif len(r) == 5 and r.__getitem__(0) == 2 and r.__getitem__(2) == 244:
                b1, y = r.__getitem__(1), r.__getitem__(4)
                if b1 == 0 and sy is None: sy = y
                elif b1 == 7 and sy is None and y == 25: sy = 25
                elif b1 == 0 and sy is not None:
                    if now - last_t > 0.35:
                        if y > sy + 4: send_key(KEYS.get("UP"))
                        elif y < sy - 4: send_key(KEYS.get("DOWN"))
                        else: send_key(KEYS.get("CENTER"))
                        last_t = now
                    sy = None
            elif len(r) == 5 and r.__getitem__(0) == 2 and r.__getitem__(4) == 15:
                b1, b2 = r.__getitem__(1), r.__getitem__(2)
                if b1 == 2 and sx is None: sx = b2
                elif b1 == 0 and sx is not None:
                    if now - last_t > 0.35:
                        send_key(KEYS.get("RIGHT") if b2 < sx - 30 else KEYS.get("LEFT")); last_t = now
                    sx = None
            elif len(r) == 5 and r.__getitem__(0) == 2 and r.__getitem__(4) == 18:
                b1, b2 = r.__getitem__(1), r.__getitem__(2)
                if b1 == 14 and now - last_t > 0.35:
                    if b2 > 170: send_key(KEYS.get("UP")); last_t = now
                    elif b2 < 90: send_key(KEYS.get("DOWN")); last_t = now
    except Exception:
        time.sleep(2)
