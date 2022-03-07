"""
    This will create add and remove
"""
import writer
from settings import RECORD_TYPE
PROMPT = ">>> "

def print_help(*args):
    help_text = """
        help -> to get help
        add -> to add new entry
        remove -> to remove an entry
        list -> list the entries
    """
    print(help_text)
def add(*args: iter) -> None:
    """
        Takes an argument: iterator
    """
    inp = args[0]
    typer = writer.strtorec[RECORD_TYPE]
    writer.recorder(typer, *inp) # Record
def handle_add(*args):
    inp = input("Sep: ")
    inp = inp.split(";")
    add(inp)
def remove(*args):
    """
        If two arguments:
            0 index header
            1 index deletion
        If one argument:
            0 index deletion
        Takes two arguments:
            typeofdeletion: str
            deletion_data: str
    """
    remtype = writer.strtorem[RECORD_TYPE]
    if len(args) == 1:
        data = args[0]
        writer.remover(remtype, data)
    if len(args) == 2:
        header = args[0]
        data = args[1]
        kw = {header:data}
        writer.remover(remtype, **kw)
def handle_remove(*args):
    answer = input("Remove(entry or header:entry)")
    header = None
    data = None
    if ":" in answer:
        header, data = answer.split(":")
    else:
        data = answer
    if header:
        remove(header, data)
    elif data:
        remove(data)
    else:
        raise TypeError("Cannot remove nothing")


def _list(*args) -> iter:
    """
        Will return a generator that generates list of entries
    """
    listtype = writer.strtolist[RECORD_TYPE]
    # DEBUG
    print(listtype)
    if len(args) == 1:
        # DEBUG
        print("One argument")
        data = args[0]
        return writer.lister(listtype, data)
    if len(args) == 2:
        # DEBUG
        print("Two arguments")
        header, data = args
        kwargs = {header:data}
        return writer.lister(listtype, **kwargs)
def handle_list(*args):
    answer = input("List n times or header:n to")
    header = None
    data = None
    gen = None
    if ":" in answer:
        header, data = answer.split(":")
        gen = _list(header, data)
    else:
        data = answer
        gen = _list(data)
    for i in gen:
        print(i)

processes = {
        "h": print_help,
        "a": handle_add,
        "r": handle_remove,
        "l": handle_list
        }

def argparser():
    """
        Parse the arguments
    """
    pass

def handle_input():
    """
        Handle input
    """
    running = True
    while running:
        answer = input(PROMPT)
        if not answer: break # If no answer break
        answer, data = parse_input(answer)
        if answer in ("exit","e","quit","q"):
            running = False # Exit
        if answer in processes:
            func = processes[answer]
            func(data)

def parse_input(inp: str) -> tuple:
    """
        Return handleable input
        Return:
            h to help
            a to add
            r to remove
    """
    if not(isinstance(inp, str)): # If inp not str raise type error
        raise TypeError("Cannot Parse")
    command = None # Placeholder
    data = None
    s_inp = inp.strip()
    if len(s_inp) != 1:
        command = s_inp[0]
    else:
        command = s_inp
    cand = s_inp.split(":")
    if len(cand) > 1:
        data = cand[-1]

    return command, data

def handle_input_adder():
    pass

def parse_input_adder():
    pass

if __name__=="__main__":
    handle_input()
