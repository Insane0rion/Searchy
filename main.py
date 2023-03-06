#!/usr/bin/env python
import argparse
from os import system

from src.engines import *
from src.fh import *

error_get_help_msg = " Enter python main.py help for instructions."


SETTINGS = init_settings()
Youtube.API_KEY = SETTINGS["API_KEY"]

# TODO Add other Engines
# TODO AMAZON/EBAY/GEIZHALS
ENGINES = {"wiki": Wikipedia, "duck": DuckDuckGo, "yt": Youtube}


def print_engines() -> None:
    system("clear")
    print("Searchy!\nAvailable Engines:")
    for key, value in ENGINES.items():
        print(f"{'-'*25}")
        print(f"| {key}: {' '*(5-len(key))}{value.NAME}{' '*(15-len(value.NAME))}|")
    print(f"{'-'*25}\nIf you want other engines to be added please reach out to me!")
    quit()


def get_args_argparse() -> dict:
    parser = argparse.ArgumentParser(
        "Searchy! A CLI search enginge enter -h or --help to get further instructions",
        epilog="\nIf you got any questions or want another engine to be added please reach out to me!",
    )
    parser.add_argument(
        "--show-engines",
        help="prints a list of valid engines (USE '.' BETWEEN SCRIPT AND FLAG)",
        action="store_true",
    )
    parser.add_argument("QUERY", help="enter what you want to look for", type=str)
    parser.add_argument(
        "-N",
        "--amt",
        help="set the amount of results to be printed (default=20)",
        type=int,
        default=SETTINGS["STANDART_AMT"],
    )
    parser.add_argument(
        "-e",
        "--engine",
        help="set the engine you want to use (default engine can be changed in the settings.ini)",
        default=SETTINGS["STANDART_ENGINE"],
    )
    args = parser.parse_args()
    if args.show_engines:
        print_engines()
    return {"engine": args.engine, "amt": args.amt, "query": args.QUERY}


def run(parm: dict):
    try:
        ENGINES[parm["engine"]].get(parm["query"], parm["amt"])
    except KeyError:
        print(f"Error: wrong engine provided!{error_get_help_msg}")


def main():
    args = get_args_argparse()
    run(args)


def debug():
    get_args_argparse()


if __name__ == "__main__":
    main()
