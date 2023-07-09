import argparse
import datetime
import hashlib
import string
import os
from prettytable import *
import time

from hasher import detect_hash_algorithm

LOWER_CASE_LETTERS = string.ascii_lowercase
UPPER_CASE_LETTERS = string.ascii_uppercase
NUMBERS = string.digits
SPECIAL_CHARACTERS = string.punctuation

YES_CHOICE = "y"
NO_CHOICE = "n"

DICTIONARY = "Required: -hf <hashes file> Optional: -ha <hashing algorithm> " \
             "Required: -df <dictionary file> Optional: -of <output file>" \
             "\nExample: -hf hashes.txt -ha sha256 -df dictionary.txt -of output.txt"

BRUTE_FORCE = "Required: -hf <hashes file> Optional: -ha <hashing algorithm> " \
              "Optional: -of <output file>\nExample: -hf hashes.txt -ha sha256"

PRECOMPUTED_DICTIONARY = "Required: -hf <hashes file>  Optional: -of <output file>" \
                         "\nExample: -hf hashes.txt"

RULE_BASED_DICTIONARY = "Required: -df <dictionary file>\n Example: -df dictionary.txt"

CUSTOM_RULES = "Required: -c <rules string>\nExample: -c p:@ a:!"

HASH_ALGORITHM_FORMAT = "* To use multiple algorithms, separate them with a comma. Example: sha256,md5"  # Format

FILE_FORMAT = "* To use multiple files, separate them with a semi-colon. " \
              "Example: file1.txt;file2.txt"

SUPPORTED_ALGORITHMS = ['ntlm'] + list(set(hashlib.algorithms_available))

passwords_cracked_per_second = []


def prompt_user_for_input(attack_type):
    parser = argparse.ArgumentParser()
    parser.add_argument("-of", "--outfile", help="Output file for saving matches")

    if attack_type != RULE_BASED_DICTIONARY:
        parser.add_argument("-hf", "--hashes", help="File containing hashed passwords")

    if attack_type != RULE_BASED_DICTIONARY and attack_type != PRECOMPUTED_DICTIONARY:
        parser.add_argument("-ha", "--algorithm", help="Hashing algorithm(s) to use", nargs="+")

    if attack_type == DICTIONARY or attack_type == RULE_BASED_DICTIONARY:
        parser.add_argument("-df", "--dictionary", help="File containing dictionary words")

    if attack_type == PRECOMPUTED_DICTIONARY:
        parser.add_argument("-pcf", "--precomputed", help="File containing precomputed hashed values")

    try:
        args = parser.parse_args(input(f"To run the cracker, please provide the following information and press Enter:"
                                       f"\n{attack_type}\n{HASH_ALGORITHM_FORMAT}\n{FILE_FORMAT}\n").split())
    except SystemExit:
        print(f"Error: Invalid argument(s) provided.")
        return prompt_user_for_input(attack_type)

    if attack_type != RULE_BASED_DICTIONARY and args.hashes is None:
        print(f"Error: Hash file not provided.")
        return prompt_user_for_input(attack_type)

    if attack_type != RULE_BASED_DICTIONARY and attack_type != PRECOMPUTED_DICTIONARY and isinstance(args.algorithm,
                                                                                                     list):
        algorithms = [algorithm.strip() for algorithm in ",".join(args.algorithm).split(",")]
        for algorithm in algorithms:
            if algorithm not in SUPPORTED_ALGORITHMS:
                print(f"Error: Unsupported algorithm '{algorithm}'. Please use one of the following algorithms:"
                      f"\n{SUPPORTED_ALGORITHMS}")
                return prompt_user_for_input(attack_type)
    else:
        if (attack_type != RULE_BASED_DICTIONARY and attack_type != PRECOMPUTED_DICTIONARY) and args.algorithm is None:
            detected_algorithms = detect_hash_algorithm(args.hashes)
            if detected_algorithms:
                print("Detected hashing algorithms:")
                for i, algorithm in enumerate(detected_algorithms, start=1):
                    print(f"{i}. {algorithm}")
                choice = input("Enter the number of the algorithm to try, 'a' to try all of them, "
                               "'b' to go back or 'c' to enter your own algorithm(s): ")
                if choice.lower() == "a":
                    algorithms = detected_algorithms
                elif choice.lower() == "b":
                    clear_screen()
                    return prompt_user_for_input(attack_type)
                elif choice.lower() == "c":
                    custom_algorithm = input("Enter the algorithm(s) to use: ")
                    if custom_algorithm in SUPPORTED_ALGORITHMS:
                        algorithms = [custom_algorithm]
                else:
                    try:
                        choice_index = int(choice) - 1
                        if 0 <= choice_index < len(detected_algorithms):
                            algorithms = [detected_algorithms[choice_index]]
                        else:
                            print("Invalid choice.")
                            return prompt_user_for_input(attack_type)
                    except ValueError:
                        print("Invalid choice.")
                        return prompt_user_for_input(attack_type)
            else:
                algorithms = []
        elif attack_type != RULE_BASED_DICTIONARY and attack_type != PRECOMPUTED_DICTIONARY and args.algorithm not in SUPPORTED_ALGORITHMS:
            print(f"Error: Unsupported algorithm '{args.algorithm}'. Please use one of the following algorithms:"
                  f"\n{SUPPORTED_ALGORITHMS}")
            return prompt_user_for_input(attack_type)

    if attack_type == DICTIONARY or attack_type == RULE_BASED_DICTIONARY:
        if args.dictionary is None:
            print(f"Error: Dictionary file not provided.")
            return prompt_user_for_input(attack_type)

    if attack_type == DICTIONARY:
        return args.hashes, algorithms, args.dictionary, args.outfile

    if attack_type == RULE_BASED_DICTIONARY:
        return args.dictionary, args.outfile

    if attack_type == BRUTE_FORCE:
        return args.hashes, algorithms, args.outfile

    if attack_type == PRECOMPUTED_DICTIONARY:
        return args.hashes, args.outfile


def read_file_content(file_paths, attack_type):
    try:
        if ';' in file_paths:
            file_paths = file_paths.split(';')
            content = []
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    content.extend(file.readlines())
        else:
            with open(file_paths, 'r') as file:
                content = file.readlines()
        return content
    except FileNotFoundError as e:
        print(f"Error: file '{e.filename}' not found. Please check the file path and try again.")
        prompt_user_for_input(attack_type)
    except PermissionError as e:
        print(f"Error: you don't have permission to open file '{e.filename}'. Please check the file permissions and "
              f"try again.")
        prompt_user_for_input(attack_type)
    except IOError as e:
        print(f"Error: there was an error reading file '{e.filename}'. Please check the file and try again.")
        prompt_user_for_input(attack_type)
    except Exception as e:
        print(f"Error: {e}")
        exit()


def brute_force_options_table():
    bruteForceOptions = PrettyTable(["Option", "Description"])
    bruteForceOptions.max_width = 40

    bruteForceOptions.align = 'l'

    bruteForceOptions.add_rows([
        ["1. Classic brute-force attack",
         "Tries all possible combinations of characters until the password is found\n"],
        ["2. Brute-force mask attack", "This method tries every possible combination of characters to crack a password "
                                       "but only uses the characters specified by the user and the mask.\n"]
    ])

    print(bruteForceOptions)


def print_description():
    description = """This program is a password cracker that offers two types of attacks: brute force attack and 
    dictionary attack. Each attack provides different options for customization.

    Brute force attack is a method of trying every possible combination of characters or words to crack a password. 
    Although it guarantees finding the password, it can be time-consuming. The time required depends on the password 
    length and character set used. The more characters used, the longer it takes to crack the password. Here are the 
    options for brute force attack:

    """
    print(description)
    brute_force_options_table()

    dictionary_description = """Dictionary attack is a method of trying every word in a dictionary to crack a 
    password. It is faster than brute force attack but doesn't guarantee success. The dictionary can consist of 
    common passwords or words from a specific language. Here are the options for dictionary attack:

    """
    print(dictionary_description)
    dictionary_attack_options_table()


def printGeneralHelp():
    clear_screen()
    print_description()
    print(
        "To use the program, you must specify the type of attack you want to use, "
        "by entering it's number from the list and the options for that attack.\n")
    printArgumentsTable()
    print("\nThe program supports the following hashing algorithms:\n")
    print_supported_algorithms()


def printArgumentsTable():
    argumentsTable = PrettyTable(["Argument/Option", "Description"])

    argumentsTable.align = 'l'

    argumentsTable.add_row(["-hf, --hashes", "File containing hashed passwords"])
    argumentsTable.add_row(["-ha, --algorithm", "Hashing algorithm to use"])
    argumentsTable.add_row(["-df, --dictionary", "File containing dictionary words"])
    argumentsTable.add_row(["-c", "Custom rules to apply to dictionary words "
                                  "(Used only in rule-based dictionary attack)"])

    print(argumentsTable)


def print_rules_table():
    rulesTable = PrettyTable(["Rules options", "Description", "Example"])

    rulesTable.align = 'l'

    rulesTable.add_row(["p, prepend", "Prepend a string to the beginning of each word", "p:123"])
    rulesTable.add_row(["a, append", "Append a string to the end of each word", "a:123"])
    rulesTable.add_row(["tc, toggle case", "Toggle the case of a character at a specific position", "tc:1"])
    rulesTable.add_row(["dbl, double", "Double a word or a character", "dbl"])
    rulesTable.add_row(["del, delete", "Delete a character at a specific position", "del:1"])
    rulesTable.add_row(["r, replace", "Replace a character at a character with another character", "r:x,y"])
    rulesTable.add_row(["t, truncate", "Truncate a word at a specific position", "t:1"])
    rulesTable.add_row(["l, leet", "Replace a character with a leet character", "l:1"])
    rulesTable.add_row(["c, capitalize", "Capitalize a character at a specific position", "c:1"])
    rulesTable.add_row(["i, invert", "Invert the case of a character at a specific position", "i:1"])
    rulesTable.add_row(["r, reverse", "Reverse a word", "r"])
    rulesTable.add_row(["u, uppercase", "Convert a word to uppercase", "u"])
    rulesTable.add_row(["l, lowercase", "Convert a word to lowercase", "l"])
    rulesTable.add_row(["t, title", "Convert a word to title case", "t"])
    rulesTable.add_row(["r, repeat", "Repeat a word N times", "dbl:3"])

    print(rulesTable)


def print_supported_algorithms():
    table = PrettyTable(["Hashing algorithm"])

    table.align = 'l'

    print("Supported hashing algorithms:")
    for algorithm in SUPPORTED_ALGORITHMS:
        table.add_row([algorithm])

    print(table)


def prompt_print_options():
    clear_screen()
    print_takes_count = input(
        "Would you like to know how many tries were taken? (This will slow down the program) [y/n]") \
                            .lower() == YES_CHOICE

    return print_takes_count


def print_password_found(password, hash_value, time_taken):
    total_time_string = format_time(datetime.timedelta(seconds=time_taken))
    print(password + ":" + hash_value, "| {}".format(total_time_string))


def attack_done(total_time, cracked_count, total_hashes):
    total_time_string = format_time(datetime.timedelta(seconds=total_time))
    print("------------------------------------------")
    print("All combinations exhausted in {}".format(total_time_string))
    print(
        "Passwords cracked: {}/{} ({:.2f}%)".format(cracked_count, total_hashes, (cracked_count / total_hashes) * 100))


def format_remaining_time(remaining_time):
    minutes, seconds = divmod(remaining_time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)
    years, months = divmod(months, 12)

    years_str = f"{int(years)} years" if years > 0 else ""
    months_str = f"{int(months)} months" if months > 0 else ""
    days_str = f"{int(days)} days" if days > 0 else ""
    hours_str = f"{int(hours)} hours" if hours > 0 else ""
    minutes_str = f"{int(minutes)} minutes" if minutes > 0 else ""

    time_components = [years_str, months_str, days_str, hours_str, minutes_str]
    formatted_time = " ".join(component for component in time_components if component)

    return formatted_time


def attack_status(total_time, cracked_count, total_hashes, takes):
    total_time_string = format_time(datetime.timedelta(seconds=total_time))
    print("\n------------* Status *-------------")
    print("Elapsed time: {}".format(total_time_string))
    print(
        "Passwords cracked: {}/{} ({:.2f}%)".format(cracked_count, total_hashes, (cracked_count / total_hashes) * 100))
    print("Combinations generated: {}".format(takes))


def format_time(timedelta):
    days = timedelta.days
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = round(timedelta.microseconds // 1000, 2)
    return "{:d}:{:02d}:{:02d}:{:02d}:{:02d}".format(days, hours, minutes, seconds, milliseconds)


def clear_screen():
    os.system('cls')


def save_match(output_file, password, hashed_password, takes_count=None):
    with open(output_file, "a") as file:
        file.write("* Password: {}\n".format(password))
        file.write("* Hashed Password: {}\n".format(hashed_password))
        file.write("* Takes: {}\n".format(takes_count)) if takes_count else None
        file.write("-------------------\n")


def dictionary_attack_options_table():
    dictionaryAttackOptions = PrettyTable(["Option", "Description"])
    dictionaryAttackOptions.max_width = 40

    dictionaryAttackOptions.align = 'l'

    dictionaryAttackOptions.add_rows([
        ["1. Classic Dictionary Attack",
         "Uses a dictionary of words to try and crack the password. "
         "The dictionary can be modified to include common passwords, names, etc.\n"],
        ["2. Dictionary Attack with Precomputed Hashes", "Uses a precomputed table of hashes to crack the password.\n"],
        ["3. Rule-Based Dictionary Attack",
         "Uses a dictionary of words and applies rules to each word to generate new passwords. "
         "The rules can be predefined or custom.\n"]
    ])

    print(dictionaryAttackOptions)
