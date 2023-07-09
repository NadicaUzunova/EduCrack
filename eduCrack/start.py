#!/usr/bin/env python3

from dictionaryAttack import dictionary_attack_menu, create_rainbow_table_menu
from bruteForceAttack import brute_force_menu
from generalLogic import *
import os


# Main menu, which is printed when the program starts. The user can choose between different cracking methods.
def print_main_menu():
    """
    Displays the main menu of the program and performs the selected action based on user input.

    This function prints the main menu options, which include different cracking methods such as brute force,
    dictionary attack, and creating a rainbow table. The user can enter the corresponding number for their choice,
    and the function maps the user's choice to the corresponding action using a dictionary. If the choice is valid,
    the corresponding function is called.

    Returns:
        None
    """
    clear_screen()

    # Dictionary mapping user's choice to the corresponding function
    options = {
        "1": lambda: brute_force_menu(print_main_menu),
        "2": lambda: dictionary_attack_menu(print_main_menu),
        "3": lambda: create_rainbow_table_menu(print_main_menu),
        "4": lambda: printGeneralHelp(),
        "5": lambda: os.system('TASKKILL /F /IM cmd.exe'),
    }

    print("-------------------- eduCrack --------------------\n")
    print("Please select a cracking method:\n")
    print("1. Brute Force - Generate all possible combinations of characters\n")
    print("2. Dictionary Attack - Use a list of common passwords to guess the password\n")
    print("3. Create Rainbow Table\n")
    print("4. Help\n")
    print("5. Exit\n")

    algorithm_choice = input("Enter your choice: ")

    if algorithm_choice in options:
        options[algorithm_choice]()
    else:
        print("Invalid choice. Please try again.\n")
        print_main_menu()


print_main_menu()
