# -*- coding: utf-8 -*-

""" Python Software Society of South Africa BBS """

import asyncio
import itertools

import click
import pyfiglet
import telnetlib3
import termcolor

from . import info

CLEAR_SCREEN = "\033[2J"


def title_style(text):
    """ Style a title string. """
    return termcolor.colored(text, 'blue', attrs=['bold'])


def prompt_style(text):
    """ Format a prompt. """
    return termcolor.colored(text, 'yellow')


def format_banner(text):
    """ Return banner text. """
    banner_text = pyfiglet.figlet_format(text, font="standard")
    banner_colour = termcolor.colored(banner_text, 'blue')
    return banner_colour.splitlines()


def format_main(menu):
    """ Return lines for the main menu. """
    return list(itertools.chain(
        [title_style(menu.title), ""],
        ("{}. {}".format(i, section.title)
         for i, section in enumerate(menu.sections)),
        ["{}. Exit".format(len(menu.sections))],
        ["", prompt_style("Select:"), ""],
    ))


def format_section(section):
    """ Return lines for the given subsection. """
    return list(itertools.chain(
        [title_style(section.title)],
        section.lines,
        ["", prompt_style("Press any key ..."), ""],
    ))


def write_lines(writer, lines):
    """ Write lines. """
    for line in lines:
        writer.write("  ")
        writer.write(line)
        writer.write("\r\n")


@asyncio.coroutine
def interact_read_integer(reader, writer, start, end):
    """ Interact with the main menu. """
    opt = None
    while opt is None:
        response = yield from reader.read(1)
        if not response:
            continue
        writer.echo(response)
        writer.write("\r\n")
        try:
            response = int(response)
        except (TypeError, ValueError):
            continue
        if start <= response <= end:
            return response


@asyncio.coroutine
def interact_wait_key(reader, writer):
    """ Interact with the main menu. """
    response = yield from reader.read(1)
    if response:
        writer.echo(response)
        writer.write("\r\n")


@asyncio.coroutine
def interact_section(section, reader, writer):
    """ Interact with a section. """
    writer.write(CLEAR_SCREEN)
    write_lines(writer, format_section(section))
    yield from interact_wait_key(reader, writer)


@asyncio.coroutine
def interact_main(menu, reader, writer):
    """ Interact with the main menu. """
    writer.write(CLEAR_SCREEN)
    write_lines(writer, format_banner("PSSSA"))
    write_lines(writer, format_main(menu))
    opt = yield from interact_read_integer(
        reader, writer, 0, len(menu.sections))
    return opt


@asyncio.coroutine
def shell(reader, writer):
    """ Shell connection to a client. """
    menu = info.load_menus()
    opt = None
    while True:
        if opt is None:
            opt = yield from interact_main(menu, reader, writer)
            if opt >= len(menu.sections):
                break
        else:
            yield from interact_section(menu.sections[opt], reader, writer)
            opt = None

    write_lines(writer, ["", prompt_style('Goodbye!')])
    yield from writer.drain()
    writer.close()


@click.command("psssa-bbs")
@click.option("--port", default=6023)
def cli(port):
    """ Python Software Society of South Africa BBS server.
    """
    loop = asyncio.get_event_loop()
    coro = telnetlib3.create_server(port=port, shell=shell)
    server = loop.run_until_complete(coro)
    try:
        loop.run_until_complete(server.wait_closed())
    except KeyboardInterrupt:
        pass
