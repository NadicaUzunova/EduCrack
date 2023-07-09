import itertools
import sys

if 'win' in sys.platform.lower():
    import msvcrt
else:
    import termios
    import tty

from hasher import *
from generalLogic import *


def basic_brute_force_attack(print_main_menu):
    """
    Performs a basic brute force attack.

    This function prompts the user for necessary input, such as the hashes file, hashing algorithms, and print options.
    It then calls the 'brute_force_attack_algorithm' function to carry out the brute force attack.

    Returns:
        None
    """
    clear_screen()

    # Prompt the user for the hashes file and hashing algorithms
    hashes_file, algorithms, output_file = prompt_user_for_input(BRUTE_FORCE)

    # Read the contents of the hashes file
    hashes = read_file_content(hashes_file, BRUTE_FORCE)

    # Check if a hashes file is provided
    if hashes is None:
        print("No hashes file provided")
        basic_brute_force_attack(print_main_menu)

    characters = list(LOWER_CASE_LETTERS + UPPER_CASE_LETTERS + NUMBERS + SPECIAL_CHARACTERS)

    # Call the brute_force_attack_algorithm function to perform the brute force attack
    print(output_file)
    brute_force_attack_algorithm(characters, hashes, algorithms, output_file)


def brute_force_attack_algorithm(characters, hashes, algorithms, output_file=None):
    clear_screen()
    hashes_copy = hashes.copy()
    takes_count = 0
    cracked_count = 0
    total_hashes = len(hashes)

    print("Brute force attack in progress. Please do not close this window. "
          "Feel free to minimize it and continue working.")

    # Assign start time here
    attack_start_time = time.time()

    current_length = 4
    while current_length <= 64:
        # Generate all possible passwords for the current length
        for password in itertools.product(characters, repeat=current_length):
            password_str = "".join(password)
            # Hash the generated password using the specified hashing algorithms
            hashed_passwords = hash_password(algorithms, password_str)
            takes_count += 1

            for h in hashes_copy.copy():
                for hashed_password in hashed_passwords:
                    # Check if a hashed password matches any of the original hashes
                    if h.strip() == hashed_password.strip():
                        # Remove the matched hash and password from the list of remaining hashes
                        cracked_count += 1
                        hashes_copy.remove(h)
                        # Print the password found and its corresponding hashed value
                        print_password_found(password_str, hashed_password, (time.time() - attack_start_time))
                        if output_file:
                            save_match(output_file, password_str, hashed_password, takes_count)

                        if not hashes_copy:
                            # Check if all hashes have been found
                            print("All hashes found")
                            break

            if msvcrt.kbhit() or termios.kbhit() or tty.kbhit():
                key = msvcrt.getch() or termios.getch() or tty.getch()
                if key.lower() == b's':
                    elapsed_time = time.time() - attack_start_time
                    attack_status(elapsed_time, cracked_count, total_hashes, takes_count)
                    if msvcrt.getch() == b'c':
                        continue
                    elif msvcrt.getch() == b'q':
                        return

            if msvcrt.kbhit() or termios.kbhit() or tty.kbhit():
                key = msvcrt.getch() or termios.getch() or tty.getch()
                if key.lower() == b'f':
                    total_time_taken = time.time() - attack_start_time
                    attack_done(total_time_taken, cracked_count, total_hashes)
                    return

        current_length += 1

    total_time_taken = time.time() - attack_start_time
    attack_done(total_time_taken, cracked_count, total_hashes)


def generate_character_set(marker):
    if marker == 'd':
        return NUMBERS
    elif marker == 'l':
        return LOWER_CASE_LETTERS
    elif marker == 'u':
        return UPPER_CASE_LETTERS
    elif marker == 's':
        return SPECIAL_CHARACTERS
    elif marker == 'a':
        return LOWER_CASE_LETTERS + UPPER_CASE_LETTERS + NUMBERS + SPECIAL_CHARACTERS
    elif marker == 'd+l' or marker == 'l+d':
        return NUMBERS + LOWER_CASE_LETTERS
    elif marker == 'd+u' or marker == 'u+d':
        return NUMBERS + UPPER_CASE_LETTERS
    elif marker == 'd+s' or marker == 's+d':
        return NUMBERS + SPECIAL_CHARACTERS
    elif marker == 'l+u' or marker == 'u+l':
        return LOWER_CASE_LETTERS + UPPER_CASE_LETTERS
    elif marker == 'l+s' or marker == 's+l':
        return LOWER_CASE_LETTERS + SPECIAL_CHARACTERS
    elif marker == 'u+s' or marker == 's+u':
        return UPPER_CASE_LETTERS + SPECIAL_CHARACTERS
    elif marker == 'd+l+u' or marker == 'd+u+l' or marker == 'l+d+u' or marker == 'l+u+d' or marker == 'u+d+l' or marker == 'u+l+d':
        return NUMBERS + LOWER_CASE_LETTERS + UPPER_CASE_LETTERS
    elif marker == 'd+l+s' or marker == 'd+s+l' or marker == 'l+d+s' or marker == 'l+s+d' or marker == 's+d+l' or marker == 's+l+d':
        return NUMBERS + LOWER_CASE_LETTERS + SPECIAL_CHARACTERS
    elif marker == 'd+u+s' or marker == 'd+s+u' or marker == 'u+d+s' or marker == 'u+s+d' or marker == 's+d+u' or marker == 's+u+d':
        return NUMBERS + UPPER_CASE_LETTERS + SPECIAL_CHARACTERS
    elif marker == 'l+u+s' or marker == 'l+s+u' or marker == 'u+l+s' or marker == 'u+s+l' or marker == 's+l+u' or marker == 's+u+l':
        return LOWER_CASE_LETTERS + UPPER_CASE_LETTERS + SPECIAL_CHARACTERS

    else:
        return ''


def brute_force_mask():
    """
        Performs a brute force attack using a mask pattern to generate password combinations.
    """
    clear_screen()
    hash_file, algorithm, output_file = prompt_user_for_input(BRUTE_FORCE)
    hashes = read_file_content(hash_file, BRUTE_FORCE)
    mask = input("Enter the mask pattern: ")

    placeholders = []
    charset = []
    known_chars = []
    password_chars = []
    takes_count = 0
    attack_start_time = time.time()
    cracked_count = 0
    total_hashes = len(hashes)

    clear_screen()

    print("Mask attack in progress. Please do not close this window. "
          "Feel free to minimize it and continue working.")

    # Collect placeholders, character sets, and known characters from the mask pattern
    i = 0
    while i < len(mask):
        char = mask[i]
        password_chars.append(char)
        if char == '?':
            placeholders.append(char)
            if i + 1 < len(mask):
                known_chars.append(mask[i + 1])
        elif char == '_':
            placeholders.append(char)
            if i + 1 < len(mask):
                charset.append(generate_character_set(mask[i + 1]))
        i += 1

    combinations = itertools.product(*charset)

    # Generate and check password combinations
    for combination in combinations:
        password_string = ''
        placeholder_index = 0
        combination_index = 0
        for i in range(len(password_chars)):
            char = password_chars[i]
            if char == '?':
                if placeholder_index < len(known_chars):
                    password_string += known_chars[placeholder_index]
                    placeholder_index += 1
            elif char == '_':
                if combination_index < len(combination):
                    password_string += combination[combination_index]
                    combination_index += 1
                else:
                    password_string += '_'
            if len(password_string) >= len(password_chars):
                break

        hashed_passwords = hash_password(algorithm, password_string)

        # Check if any of the hashed passwords match the generated password
        for hashed_password in hashed_passwords:
            for h in hashes:
                if hashed_password.strip() == h.strip():
                    cracked_count += 1
                    print_password_found(password_string, hashed_password, (time.time() - attack_start_time))
                    if output_file:
                        save_match(output_file, password_string, hashed_password)

        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key.lower() == b's':
                elapsed_time = time.time() - attack_start_time
                attack_status(elapsed_time, cracked_count, total_hashes, takes_count)
                if msvcrt.getch() == b'c':
                    continue
                elif msvcrt.getch() == b'q':
                    return

        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key.lower() == b'f':
                total_time_taken = time.time() - attack_start_time
                attack_done(total_time_taken, cracked_count, total_hashes)
                return

        takes_count += 1  # Increment takes_count for each combination checked

    total_time_taken = time.time() - attack_start_time
    attack_done(total_time_taken, cracked_count, total_hashes)


# Menu for the brute force attack. The user can choose between cracking any password or a custom password.
def brute_force_menu(print_main_menu):
    """
    Displays the menu for the brute force attack and performs the chosen attack based on user input.
    """
    clear_screen()
    options = {
        "1": lambda: basic_brute_force_attack(print_main_menu),
        "2": lambda: brute_force_mask(),
    }

    brute_force_options_table()
    choice = input("\nEnter the number of the attack you would like to perform:\n")

    if choice in options:
        options[choice]()
