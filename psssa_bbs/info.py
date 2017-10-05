# -*- coding: utf-8 -*-

""" BBS menus. """

import pkg_resources
import re


def load_info():
    """ Read info.txt. """
    info = pkg_resources.resource_string(__name__, "info.txt")
    return info.decode("utf-8")


_TITLE_RE = re.compile(r"^===*$")
_SECTION_RE = re.compile(r"^---*$")


def load_menus():
    """ Parse info.txt into menus. """
    info = load_info()
    menu = Menu()
    sub_menu = None
    line = None
    lines = iter(info.splitlines())
    for line in lines:
        prev_line = line
        break
    for line in lines:
        if _TITLE_RE.match(line):
            menu.title = prev_line
            line = None
        elif _SECTION_RE.match(line):
            if sub_menu:
                if sub_menu.lines and not sub_menu.lines[-1].strip():
                    del sub_menu.lines[-1]
            sub_menu = Menu(title=prev_line)
            menu.sections.append(sub_menu)
            line = None
        elif sub_menu and prev_line is not None:
            sub_menu.lines.append(prev_line)
        prev_line = line
    if line and sub_menu:
        sub_menu.lines.append(line)
    return menu


class Menu:
    """ BBS Menu """
    def __init__(self, title="Unknown"):
        self.title = title
        self.lines = []
        self.sections = []
