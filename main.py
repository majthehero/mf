import curses
import time
import os
import sys
import subprocess


data = {
    "left": {
        "path": os.getcwd(),
        "fnames": [],
        "idx": 0,
        "selection": set(),
        "offset": 0,
    },
    "right": {
        "text_lines": [],
        "offset": 0,
    },
    "status": [],
    "options": {
        "show_hidden": False,
    },
    "scr": {
        "std": None,
        "left": None,
        "right": None,
    },
}


def log_status(msg):
    data["status"].append(msg)


def get_files():
    if data["options"]["show_hidden"]:
        cond = lambda fn: True
    else:
        cond = lambda fn: not fn.startswith(".")
    fnames = list(filter(cond, [fd.name for fd in os.scandir(data["left"]["path"])]))
    fnames.sort()
    return fnames

def set_loff(n):
    data["left"]["offset"] = n

def draw_file_list():
    scr = data["scr"]["left"]
    idx = data["left"]["idx"]
    R = scr.getmaxyx()[0]
    F = len(data["left"]["fnames"])
    
    if idx < R-3:
        da = 0
    if 



    offset = idx
    log_status(f"off:{offset}")

    for i in range(max_row):
        attr = 0
        if i + offset == idx:
            attr |= curses.A_BOLD

        if i + offset in data["left"]["selection"]:
            attr |= curses.A_UNDERLINE

        if i + offset < len(data["left"]["fnames"]):
            fname = data["left"]["fnames"][i + offset]
            scr.addstr(i, 1, fname, attr)


def draw_preview():
    scr = data["scr"]["right"]
    if data["right"]["text_lines"] == "viu":
        subprocess.run(["tput", "cup", str(scr.getbegyx()[0]), str(scr.getbegyx()[1])])
        subprocess.run(
            [
                "viu",
                os.path.join(
                    data["left"]["path"],
                    data["left"]["fnames"][data["left"]["idx"]],
                ),
                "-h",
                str(scr.getmaxyx()[0]),
                "-w",
                str(scr.getmaxyx()[1]),
            ]
        )
    else:
        for i, line in enumerate(data["right"]["text_lines"]):
            if i >= scr.getmaxyx()[0] - 1:
                break
            scr.addnstr(i, 0, data["right"]["text_lines"][i], scr.getmaxyx()[1] - 2)


def draw_status():
    scr = data["scr"]["std"]
    scr.addstr(0, 1, f"-mf- {data["left"]["path"]}")
    status = ""

    i = 0
    while len(status) < curses.COLS and i < len(data["status"]):
        status += " | " + data["status"][-i]
        i += 1
    if status != "":
        status += " |"
    if len(status) > curses.COLS - 4:
        status = "..." + status[-(curses.COLS - 4) :]
    scr.addstr(curses.LINES - 1, 0, status)


def main(std_scr):
    help_text = """
    Maja's File Manager

    Usage:
    mf [OPTION...] [dir]

    Options:
    --help / -h / h - show this help text.
    --show-all / -a / a - show all files, including hidden - those  starting with '.'.
    """
    for i in range(1, len(sys.argv)):
        if sys.argv[i] in ["--help", "-h", "h"]:
            print(help_text)
        if sys.argv[i] in ["--show-all", "-a", "a"]:
            data["options"]["show_hidden"] = True
            log_status("h+")
    if os.path.exists(sys.argv[-1]):
        path = sys.argv[-1]
    else:
        path = os.getcwd()

    # init screens
    curses.start_color()
    data["scr"]["std"] = std_scr
    left_scr = curses.newwin(curses.LINES - 2, curses.COLS // 2, 1, 0)
    data["scr"]["left"] = left_scr

    right_scr = curses.newwin(curses.LINES - 2, curses.COLS // 2, 1, curses.COLS // 2)
    data["scr"]["right"] = right_scr

    # main loop
    data["left"]["path"] = path
    data["left"]["fnames"] = get_files()
    uin = None
    RUNNING = True
    while RUNNING:

        # draw
        std_scr.clear()
        draw_file_list()
        draw_preview()
        draw_status()

        # refresh
        std_scr.refresh()
        left_scr.refresh()
        right_scr.refresh()

        # take input
        uin = std_scr.getkey()

        # UP / DOWN
        idx = data["left"]["idx"]
        if uin in ["KEY_UP", "k"]:
            idx = idx - 1 if idx - 1 > 0 else 0
        if uin in ["KEY_DOWN", "j"]:
            idx = idx + 1 if idx + 1 < len(data["left"]["fnames"]) else idx
        data["left"]["idx"] = idx

        # select
        if uin in [" "]:
            try:
                data["left"]["selection"].remove(idx)
            except KeyError as _:
                data["left"]["selection"].add(idx)

        # LEFT
        if uin in ["KEY_LEFT", "h"]:
            # move to parent
            data["left"]["path"] = os.path.dirname(data["left"]["path"])
            data["left"]["fnames"] = get_files()
            data["left"]["idx"] = 0
            data["left"]["selection"] = set()
            data["left"]["offset"] = 0

        # RIGHT
        if uin in ["KEY_RIGHT", "l"]:
            # move to child
            path = os.path.join(
                data["left"]["path"], data["left"]["fnames"][data["left"]["idx"]]
            )
            if os.path.isdir(path):
                data["left"]["path"] = path
                data["left"]["fnames"] = get_files()
                data["left"]["idx"] = 0
                data["left"]["selection"] = set()
                data["left"]["offset"] = 0
            # if not dir show preview
            else:
                with open(path) as fd:
                    try:
                        data["right"]["text_lines"] = fd.readlines()
                    except UnicodeDecodeError as e:
                        data["right"]["text_lines"] = "viu"
        # quit
        if uin in ["q"]:
            with open("/tmp/mf_q_dir", "w") as fd:
                fd.write(data["left"]["path"])
            RUNNING = False


if __name__ == "__main__":
    curses.wrapper(main)
