"""
    Module to record writer
    What should it do:
        - Will record in various ways
            - CSV
            - EXCEL
            - JSON
            - ...
            - Maybe SQL
       - How it will record
       ID, USERNAME, PASSWORD, MAIL, HINT, ADDITIONAL
"""
import pathlib as pl
from os.path import join
import csv
import sys
from settings import FILENAME, FILEPATH, FIELD_NAMES
import os
"""
FILENAME = "record"
FILEPATH = str(pl.Path(__file__).parent.absolute())
FIELD_NAMES = ['ID', 'USERNAME', 'PASSWORD','MAIL','HINT','ADDITIONAL'] # Store this in a ini file
"""
# DEBUG

"""
    Main structure:
        Check if exists
            if it doesn't exist:
                write_basics
            if it exists:
                contuniue
        Check if new writing matches old ones:
            if it doesen't throw an error(doesen't match)
        Write everything
"""
# Exceptions
def parse_input(string_list: list) -> dict:
    """
        This function will get a list of string and returns a dict:
            FIELD_NAME to string_list
    """
    parsed_dict = dict()
    if len(string_list) != len(FIELD_NAMES)-1: # -1 for ID section
        raise SystemExit("Cannot parse because key and values not equal!!!")
    for key, value in zip(FIELD_NAMES[1:], string_list):
        parsed_dict[key] = value
    print(parsed_dict)
    return parsed_dict
def recorder(rectype, *args, **kwargs):
    """
        rectype: function to save
        kwargs: kwargs to record
    """
    torecord = None
    if args:
        torecord = parse_input(args)
    elif kwargs:
        torecord = kwargs
    rectype(**torecord)
    # DEBUG
    print('I\'m a recorder')

def remover(remtype, *args, **kwargs):
    """
        Remove from any type
    """
    remtype(*args, **kwargs)

def lister(listtype, *args,**kwargs):
    """
        List the entries
    """
    return listtype(*args, **kwargs)


def isExists(filetype):
    fullpath = join(FILEPATH, FILENAME+'.'+filetype)
    return pl.Path(fullpath).exists()
def csvRecorder(**kwargs):
    """
        Record kwargs as csv
    """
    csvfile = join(FILEPATH, FILENAME+'.csv') # Filepath to record csv
    last_id = None # Variable placeholder
    if not isExists("csv"): # Check if file exists and create if it doesn't and writer headers
        with open(csvfile, 'w',newline='') as f:
            csv_write = csv.DictWriter(f, fieldnames=FIELD_NAMES,delimiter=',')
            csv_write.writeheader()
    with open(csvfile, 'r') as f: # Read the last id
        csv_reader = csv.reader(f)
        last_headers = next(csv_reader) # Check if headers same as others else throw error or rearrange
        for last, *everthingelse in csv_reader:
            last_id = last
    if not last_id: # If there's no entry last id is 1
        last_id = 0
    kwargs[FIELD_NAMES[0]] = int(last_id) + 1
    with open(csvfile, 'a',newline='') as f: # Write all to file
        csv_write = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        csv_write.writerow(kwargs)

def csvRemover(*args, **kwargs):
    csvfile = join(FILEPATH, FILENAME+'.csv') # Filepath to record csv
    remove_type = None
    header = None
    if args:
        remove_type = args[0]
    elif kwargs:
        for header, remove_type in kwargs.items():
            header = FIELD_NAMES.index(header)
            remove_type = remove_type
    check = None # Check function placeholder
    if header:
        check = lambda x: x[header] == remove_type # If there's a header
    else:                                          # Check for header
        check = lambda x: remove_type in x         # If not check for in
    with open(csvfile,'r') as file:
        csvreader = csv.reader(file) # Read all lines
        with open(csvfile+".part",'w') as wfile: # Write all in temp file
            csvwriter = csv.writer(wfile)
            for line in csvreader:
                if not check(line): # If check isn't true
                    csvwriter.writerow(line) # Write line else not 
    with open(csvfile,'w') as file:
        with open(csvfile+".part", 'r') as newfile:
            file.write(newfile.read())
    os.remove(csvfile+".part")

def csvLister(*args, **kwargs):
    """
        If args exist list n times
        If kwargs exist list only that header
    """
    print(args, kwargs)
    csvfile = join(FILEPATH, FILENAME+'.csv') # Filepath to record csv
    n_list = None
    header = None
    if args:
        n_list = args[0]
        if not isinstance(n_list, int) and not n_list.isdigit():
            raise TypeError("Cannot n list if n is not integer")
        n_list = int(n_list)
    elif kwargs:
        if len(kwargs) > 1:
            raise TypeError("Too many parameters")
        if not("header" in kwargs):
            raise TypeError("There's not header parameter")
        for temp, header in kwargs.items():
            temp = temp
            header = header
        if header not in FIELD_NAMES:
            raise TypeError("There's no header like that")
    else:
        raise TypeError("No arguments given") # Or list all file
    if not header:
        with open(csvfile,'r') as file:
            csvreader = csv.reader(file)
            next(csvreader) # Pass the header
            for i in range(n_list):
                try:
                    row = next(csvreader)
                except StopIteration:
                    print("There's not enough entry")
                    return False
                yield row

# DEBUG
def listertest():
    while True:
        answer = input("Listing")
        if answer == "exit" or not answer:
            return
        for i in csvLister(answer):
            print(",".join(i))

# DEBUG
def removetest():
    answer = input("Remove(1)/Remove by(2): ")
    if answer == "1":
        answer = input("What do you want to remove")
        csvRemover(answer)
    if answer == "2":
        answer = input("What to remove by header(HEADER:NAME): ")
        header, name = answer.split(':')
        kwargs = {header:name}
        csvRemover(**kwargs)
"""
def DEBUG():
    what_to_add = input("What to add with ,: ")
    USERNAME, PASSWORD, MAIL, HINT, ADDITIONAL = what_to_add.split(",")
    csvRecorder(USERNAME=USERNAME,PASSWORD=PASSWORD,MAIL=MAIL,HINT=HINT,ADDITIONAL=ADDITIONAL)
if __name__=="__main__":
    while True:DEBUG()
"""

def excelRecorder():
    return -1
def excelRemover():
    return -1
def excelLister():
    return -1

def jsonRecorder():
    return -1
def jsonRemover():
    return -1
def jsonLister():
    return -1

def sqlRecorder():
    return -1
def sqlRemover():
    return -1
def sqlLister():
    return -1

class rec:
    csv = csvRecorder
    excel = excelRecorder
    json = jsonRecorder
    sql = sqlRecorder

def handle_input():
    toret = list()
    for field in FIELD_NAMES[1:]:
        answer = input("What is {}: ".format(field))
        toret.append(answer)
    return toret
# Conversions 
strtorec = {'csv':rec.csv,
            'excel':rec.excel,
            'json':rec.json,
            'sql':rec.sql
           }
strtorem = {'csv':csvRemover,
            'excel':excelRemover,
            'json':jsonRemover,
            'sql':sqlRemover
           }
strtolist = {'csv':csvLister,
            'excel':excelLister,
            'json':jsonLister,
            'sql':sqlLister
           }




def main():
    for item in strtorec.items():
        print(item)
    while True:
        option = str(input("What do you want to try: ").strip())
        if not option:
            sys.exit()
        input_of = handle_input()
        recorder(strtorec[option], *input_of)

if __name__ == "__main__":
    listertest()
    # removetest()
    # main()
