#!/usr/bin/env python
from os import system


from sys import argv
from src.engines import *

error_get_help_msg = " Enter python main.py help for instructions."

# TODO Add other Engines
ENGINES = {"wiki": Wikipedia,
           "duck": DuckDuckGo}


def get_args():
    del argv[0]
    if len(argv) == 0 or len(argv) > 3: # Checking if its a valid input or if HELP or ENGINES needed
        print("Invalid amount of arguments enter HELP to get a usage description!")
        quit()
    if len(argv) == 1 and argv[0] == "HELP":
        print("|Searchy! An fast CLI search engine...\n|\n"
              "|Command Usage: main.py [QUERY](needed) [ENGINE](optional) [AMOUNT](optional)\n|\n"
              "|Please replace whitespaces of the query with underscores!!\n"
              "|If you want to know which engines are available enter main.py ENGINES !\n"
              "|If you want to report a bug please leave a ticket at github.com/Insane0rion/Searchy\n|\n"
              "|Enjoy you're day and thanks for using my application!")
        quit()
    elif len(argv) == 1 and argv[0] == "ENGINES":
        print("|Searchys available Engines:\n|")
        for key, value in ENGINES.items():
            print(f"| {value.name} : {key}")    # TODO Pretty up this
        print("|\n| Please tell me if you want an engine to be added!")
        quit()
    amt = 0 # Setting Stan amount
    engine = "duck" # Setting Stan Engine TODO mk file to get stan 
    query = '' 
    for arg in argv:
        if arg in ENGINES: # if arg an engine swap to that
            engine = arg
            argv.remove(engine)
            pass
        try:
            amt = int(arg) 
        except ValueError: # Else the query is set to arg if query is empty 
            if query == '':
                query = arg
            else:
                print("Error: The engine you provided is not available!")
                quit()
    return (engine, query, amt)


def run(parm:tuple):
    try:
        engine = ENGINES[parm[0]]
        engine.get(parm[1],parm[2])
    except KeyError:
        print(f"Error: wrong engine provided!{error_get_help_msg}")


def main():
    run(get_args())

def debug():
    run(("duck", "test", 0))

if __name__ == '__main__':
    main()