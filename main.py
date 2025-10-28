import curses
import time
import os
import sys


data = {
    "left": {
        "path" : os.getcwd(),
        "fnames": [fd.name for fd in os.scandir()],
        "idx": 0,
        "selection" : set(),
        "offset": 0,
    },
    "right": {
        "text_lines": [],
        "offset": 0,
    }
}


def list_files(scr):
    for i, fname in enumerate(data["left"]["fnames"] [data["left"]["offset"]:data["left"]["offset"]+scr.getmaxyx()[0]-1]):
        if i >= scr.getmaxyx()[0]:
            break
        attr = 0
        if i == data["left"]["idx"]: # TODO: fix drawing with offset!
            attr |= curses.A_BOLD
        if i in data["left"]["selection"]:
            attr |= curses.A_UNDERLINE
        scr.addstr(i,1, fname, attr) 
        

def draw_preview(scr):
    for i, line in enumerate(data["right"]["text_lines"]):
        if i >= scr.getmaxyx()[0] -1:
            break
        scr.addnstr(i, 0, data["right"]["text_lines"][i], scr.getmaxyx()[1]-2)


def main(std_scr):
    RUNNING = True
    
    curses.start_color()

    path = os.getcwd()

    std_scr.addstr(0,1, "-mf- {paht}")

    left_scr = curses.newwin(curses.LINES - 2, curses.COLS // 2, 1, 0)
    right_scr = curses.newwin(curses.LINES - 2, curses.COLS // 2, 1, curses.COLS // 2)

    while RUNNING:

        std_scr.clear()

        list_files(left_scr)

        draw_preview(right_scr)

        std_scr.refresh()
        left_scr.refresh()
        right_scr.refresh()
    
        # take input
        uin = std_scr.getkey()
        std_scr.addstr(curses.LINES-1,1, uin)

        # UP / DOWN
        idx = data["left"]["idx"]
        if uin in ["KEY_UP", "k"]:
            idx = idx-1 if idx-1 > 0 else 0
            if idx < 0:
                data["left"]["offset"] -= 1
        if uin in ["KEY_DOWN", "j"]:
            idx = idx+1 if idx+1 < len(data["left"]["fnames"]) else idx 
            if idx >= right_scr.getmaxyx()[0]:
                data["left"]["offset"] += 1
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
            data["left"]["fnames"] = [fd.name for fd in os.scandir(data["left"]["path"])]
            data["left"]["idx"] = 0
            data["left"]["selection"] = set()
            data["left"]["offset"] = 0

        # RIGHT
        if uin in ["KEY_RIGHT", "l"]:
            # move to child 
            path = os.path.join(data["left"]["path"], data["left"]["fnames"][data["left"]["idx"]])
            if os.path.isdir(path):
                data["left"]["path"] = path
                data["left"]["fnames"] = [fd.name for fd in os.scandir(data["left"]["path"])]
                data["left"]["idx"] = 0
                data["left"]["selection"] = set()
                data["left"]["offset"] = 0
            else:
                with open(path) as fd:
                    data["right"]["text_lines"] = fd.readlines()
        
        # quit
        if uin in ["q"]:
            RUNNING = False


curses.wrapper(main)

