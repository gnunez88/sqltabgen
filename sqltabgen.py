#!/usr/bin/python3
# coding: utf-8

import argparse
import os
import pdb
import random
import re
import signal
import sys

# Global variables
outfile = None

# Functions
def ctrl_c(sig, frame):
    sys.stderr.write('\n[!] Exiting...\n')
    global outfile
    if outfile:
        outfile.close()
    sys.exit(1)


def check_format(field:list) -> list:
    pattern = r'^[^:]+:(v|fr?):.+(:[idfs])?$'
    is_valid = re.match(pattern, field)
    if not is_valid:
        error_msg = "The format for the fields is not right"
        raise argparse.ArgumentTypeError(error_msg)
    return field


# Since Python passes the parameters by value and not by reference
# we can use the parameter itself
def randomise(original:list) -> list:
    randomised = list()
    while len(original) > 0:
        index = random.randint(0, len(original)-1)
        value = original.pop(index)
        randomised.append(value)
    return randomised


def main(args):
    if args.debug:
        pdb.set_trace()

    signal.signal(signal.SIGINT, ctrl_c)
    global outfile

    if args.outfile:
        # Exceptions will tell you what you have wrong
        outfile = open(args.outfile, 'w')

    values = dict()
    for entry in args.fields:
        parts = entry.split(':')
        if parts[1] in ['f', 'fr']:
            with open(parts[2], 'r') as f:
                entries = f.read().split('\n')
                # Removing the last entry if empty
                if entries[-1] == '':
                    entries.pop()
            # Casting the values if needed (integer or float)
            if (len(parts) == 4 and parts[3] == 's') or len(parts) < 4:
                for index in range(len(entries)):
                    entries[index] = f"'{entries[index]}'"
            # Inserting the values into the dictionary
            if parts[1] == 'fr':
                values[parts[0]] = randomise(entries)
            else:
                values[parts[0]] = entries
        elif parts[1] == 'v':
            if (len(parts) == 4 and parts[3] == 's') or len(parts) < 4:
                value = [f"'{parts[2]}'"]
            else:
                value = [parts[2]]
            values[parts[0]] = value

    # Extracting the field values
    field_values = ','.join([x.split(':')[0] for x in args.fields])
    # First line of the SQL query
    output = f"INSERT INTO {args.table} ({field_values}) values"

    # Inserting the values
    for register in range(len(list(values.values())[0])):
        if register == args.quantity:
            break
        row_values = ','.join([str(x[register]) for x in list(values.values())])
        output += f"\n({row_values}),"

    # The last entry should have a semicolon
    output = output[:-1] + ";"

    if not args.quiet:
        print(output)
    if args.outfile:
        outfile.write(output)
        outfile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fields', type=check_format, nargs='+', 
        help="field:<v|f[r]>:<value|file>[:<n|s>] [field:<v|f[r]>:<value|file>[:<n|s>]]")
    parser.add_argument('-n', '--quantity', type=int, help="Amount of values to use")
    #parser.add_argument('-r', '--random', action='store_true', help="Use values randomly")
    parser.add_argument('-t', '--table', type=str, help="Table name")
    parser.add_argument('-o', '--outfile', type=str, help="Output SQL file")
    parser.add_argument('-q', '--quiet', action='store_true', help="Don't print the results")
    parser.add_argument('-d', '--debug', action='store_true', help="Debugging mode")
    args = parser.parse_args()
    main(args)
