from tkinter import Tk, filedialog, messagebox

from hasher import *
from generalLogic import *


def dictionary_attack_algorithm(hashes, dictionary_file, algorithms, output_file=None):
    clear_screen()
    takes_count = 0
    cracked_count = 0
    total_hashes = len(hashes)
    attack_start_time = time.time()

    for password in dictionary_file:
        password = password.strip()
        hashed_passwords = hash_password(algorithms, password)

        takes_count += 1

        for hashed_password in hashed_passwords:
            for h in hashes.copy():
                if h.strip() == hashed_password.strip():
                    print_password_found(password, hashed_password, (time.time() - attack_start_time))
                    hashes.remove(h)
                    cracked_count += 1
                    if output_file:
                        save_match(output_file, password, hashed_password, takes_count)

        if len(hashes) == 0:
            break

    total_time_taken = time.time() - attack_start_time
    attack_done(total_time_taken, cracked_count, total_hashes)


def rainbow_table_attack_with_precomputed_table(print_main_menu):
    clear_screen()
    hashes_file, output_file = prompt_user_for_input(PRECOMPUTED_DICTIONARY)
    hashes = read_file_content(hashes_file, DICTIONARY)
    total_hashes = len(hashes)
    cracked_count = 0

    if hashes is None:
        print("No hashes file provided.")
        dictionary_attack_menu(print_main_menu)

    precomputed_table_files = ["rainbow.txt"]  # Add the file names of precomputed tables
    print("Choose a file containing the precomputed table:")
    for i, file_name in enumerate(precomputed_table_files, start=1):
        print(f"{i}. {file_name}")
    print(f"{len(precomputed_table_files) + 1}. Enter your own file")
    choice = input("Enter the number of the file or 'own' to enter your own file path: ")

    if choice.isdigit() and 1 <= int(choice) <= len(precomputed_table_files):
        precomputed_table_file = precomputed_table_files[int(choice) - 1]
    elif choice.lower() == "own":
        root = Tk()
        root.withdraw()
        precomputed_table_file = filedialog.askopenfilename(title="Select Precomputed Table File")
    else:
        print("Invalid choice.")
        dictionary_attack_menu(print_main_menu)

    precomputed_table = read_file_content(precomputed_table_file, PRECOMPUTED_DICTIONARY)

    found_passwords = []
    takes_count = 0

    clear_screen()

    attack_start_time = time.time()
    precomputed_hashes = set(line.split(":")[1].strip() for line in precomputed_table)

    for hash_value in hashes:
        hash_value = hash_value.strip()
        takes_count += 1

        if hash_value in precomputed_hashes:
            for line in precomputed_table:
                line = line.strip().split(":")
                password, hashed_password = line[0], line[1]

                if hash_value == hashed_password:
                    found_passwords.append((password, hash_value))
                    cracked_count = len(found_passwords)
                    break

        if cracked_count == total_hashes:
            break

    total_time_taken = time.time() - attack_start_time

    if found_passwords:
        for password, hash_value in found_passwords:
            print_password_found(password, hash_value, (time.time() - attack_start_time))
            if output_file:
                save_match(output_file, password, hash_value, takes_count)

        attack_done(total_time_taken, cracked_count, total_hashes)

    else:
        print("Passwords not found.")


def leet_character(char):
    leet_chars = {
        'a': '4',
        'e': '3',
        'g': '6',
        'l': '1',
        'o': '0',
        's': '5',
        't': '7'
    }
    return leet_chars.get(char.lower(), char)


def parse_custom_rules(custom_rules):
    parsed_rules = []

    for rule_string in custom_rules:
        rule_parts = rule_string.split(':')
        rule_name = rule_parts[0]
        rule_arguments = rule_parts[1:]

        if rule_name == 'p':
            # Rule 'p': Prepend the given string to the input string
            def parsed_rule(x, prepend=rule_arguments[0]):
                return prepend + x

        elif rule_name == 'a':
            # Rule 'a': Append the given string to the input string
            def parsed_rule(x, append=rule_arguments[0]):
                return x + append

        elif rule_name == 'tc':
            # Rule 'tc': Toggle the case of a character at the specified position
            position = int(rule_arguments[0])

            def parsed_rule(x, pos=position):
                if pos <= len(x):
                    return x[:pos - 1] + x[pos - 1].swapcase() + x[pos:]
                else:
                    return x

        elif rule_name == 'dbl':
            if len(rule_arguments) == 0:
                # Rule 'dbl': Duplicate the input string
                def parsed_rule(x):
                    return x + x
            else:
                if rule_arguments[0].isdigit():
                    # Rule 'dbl:N': Repeat the input string N times
                    n = int(rule_arguments[0])

                    def parsed_rule(x, count=n):
                        return x * count

        elif rule_name == 'del':
            # Rule 'del': Delete a character at the specified position
            position = int(rule_arguments[0])

            def parsed_rule(x, pos=position):
                if pos <= len(x):
                    return x[:pos - 1] + x[pos:]
                else:
                    return x

        elif rule_name == 'r':
            if len(rule_arguments) == 0:
                # Rule 'r': Reverse the input string
                def parsed_rule(x):
                    return x[::-1]
            elif len(rule_arguments) == 1:
                if ',' in rule_arguments[0]:
                    # Rule 'r:x,y': Replace occurrences of character x with character y
                    old_char, new_char = rule_arguments[0].split(',')

                    def parsed_rule(x, old=old_char, new=new_char):
                        return x.replace(old, new)
                else:
                    # Rule 'r:N': Repeat the input string N times
                    n = int(rule_arguments[0])

                    def parsed_rule(x, count=n):
                        return x * count

        elif rule_name == 't':
            if len(rule_arguments) == 0:
                # Rule 't': Convert the input string to title case

                def parsed_rule(x):
                    return x.title()

            elif len(rule_arguments) == 1:
                # Rule 't:N': Truncate the input string at position N
                position = int(rule_arguments[0])

                def parsed_rule(x, pos=position):
                    if pos <= len(x):
                        return x[:pos]
                    else:
                        return x

        elif rule_name == 'l':
            if len(rule_arguments) == 0:
                # Rule 'l': Convert the input string to lowercase
                def parsed_rule(x):
                    return x.lower()
            elif len(rule_arguments) == 1:
                # Rule 'l:N': Replace a character at position N with its leet equivalent
                position = int(rule_arguments[0])

                def parsed_rule(x, pos=position):
                    if pos <= len(x):
                        return x[:pos - 1] + leet_character(x[pos - 1]) + x[pos:]
                    else:
                        return x

        elif rule_name == 'c':
            # Rule 'c': Capitalize the character at the specified position
            position = int(rule_arguments[0])

            def parsed_rule(x, pos=position):
                if pos <= len(x):
                    return x[:pos - 1] + x[pos - 1].capitalize() + x[pos:]
                else:
                    return x

        elif rule_name == 'i':
            # Rule 'i': Invert the case of the character at the specified position
            position = int(rule_arguments[0])

            def parsed_rule(x, pos=position):
                if pos <= len(x):
                    return x[:pos - 1] + x[pos - 1].swapcase() + x[pos:]
                else:
                    return x

        elif rule_name == 'u':
            # Rule 'u': Convert the input string to uppercase
            def parsed_rule(x):
                return x.upper()

        parsed_rules.append(parsed_rule)

    return parsed_rules


def apply_rules_to_dictionary(dictionary_content, custom_rules=None, predefined_rules=True):

    default_rules = [
        lambda x: x,  # Rule 1: No change
        lambda x: x.upper(),  # Rule 2: Convert to uppercase
        lambda x: x.lower(),  # Rule 3: Convert to lowercase
        lambda x: x[::-1],  # Rule 4: Reverse the password
        lambda x: x + '123',  # Rule 5: Append '123' to the password
        lambda x: x.capitalize(),  # Rule 6: Capitalize the first letter and lower the rest
        lambda x: x[:1].lower() + x[1:].upper(),  # Rule 7: Invert capitalize
        lambda x: x.swapcase(),  # Rule 8: Toggle case
        lambda x: x[:1].swapcase() + x[1:],  # Rule 9: Toggle @
        lambda x: x + x,  # Rule 10: Duplicate entire word
        lambda x: x * 3,  # Rule 11: Duplicate N times
        lambda x: x + x[::-1],  # Rule 12: Reflect
        lambda x: x[1:] + x[0],  # Rule 13: Rotate left
        lambda x: x[-1] + x[:-1],  # Rule 14: Rotate right
        lambda x: x[1:],  # Rule 15: Truncate left
        lambda x: x[:-1],  # Rule 16: Truncate right
        lambda x: x[:1] + x[2:],  # Rule 17: Delete @ N
        lambda x: ''.join([c * 2 for c in x]),  # Rule 18: Duplicate all
        lambda x: x.replace('X', 'Y')  # Rule 19: Replace X with Y
    ]

    if custom_rules is None:
        custom_rules = []
    if predefined_rules:
        rules = default_rules + parse_custom_rules(custom_rules)
    else:
        rules = parse_custom_rules(custom_rules)

    passwords = dictionary_content

    new_passwords = []

    for password in passwords:
        password = password.strip()

        new_passwords.append(password)

        for rule in rules:
            new_password = rule(password)

            if new_password != password:
                new_passwords.append(new_password)  # Add the modified passwords

    return new_passwords


def get_custom_rules_from_user():
    clear_screen()
    print_rules_table()

    parser = argparse.ArgumentParser(description='Apply rules to a dictionary of passwords.')
    parser.add_argument('-c', '--custom-rules', nargs='+',
                        help='Custom rules in the format rule_name:rule_argument.')

    args = parser.parse_args(input(f"Please use the following format to run the cracker and press enter:"
                                   f"\n{CUSTOM_RULES}\n").split())

    return args.custom_rules


def rule_based_dictionary_attack(print_main_menu):
    clear_screen()

    dictionary_file, output_file = prompt_user_for_input(RULE_BASED_DICTIONARY)
    words = read_file_content(dictionary_file, RULE_BASED_DICTIONARY)

    if words is None:
        print("No dictionary file provided.")
        return

    choice = input("Choose the option:\n"
                   "1. Use predefined rules only\n"
                   "2. Create custom rules only\n"
                   "3. Use predefined rules plus custom rules (skipping duplicates)\n")

    if choice == "1":
        new_passwords = apply_rules_to_dictionary(words, predefined_rules=True)
    elif choice == "2":
        custom_rules = get_custom_rules_from_user()
        new_passwords = apply_rules_to_dictionary(words, custom_rules=custom_rules, predefined_rules=False)
    elif choice == "3":
        custom_rules = get_custom_rules_from_user()
        new_passwords = apply_rules_to_dictionary(words, custom_rules=custom_rules, predefined_rules=True)
    else:
        print("Invalid choice.")
        rule_based_dictionary_attack(print_main_menu)

    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Output Folder")

    if not folder_selected:
        print("No folder selected. Output file creation aborted.")
        rule_based_dictionary_attack(print_main_menu)

    file_name = f"{os.path.splitext(os.path.basename(dictionary_file))[0]}_custom_rules.txt"
    file_path = os.path.join(folder_selected, file_name)

    if os.path.exists(file_path):
        overwrite = input(f"A file with the name '{file_name}' already exists at the same location. "
                          f"Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != YES_CHOICE:
            index = 1
            while os.path.exists(file_path):
                file_name = f"{os.path.splitext(os.path.basename(dictionary_file))[0]}_custom_rules_{index}.txt"
                file_path = os.path.join(folder_selected, file_name)
                index += 1

    with open(file_path, 'w') as file:
        file.write('\n'.join(new_passwords))

    clear_screen()

    new_words_path = os.path.abspath(file_path)
    message = f"New dictionary file created at.\nLocation: {new_words_path}"
    messagebox.showinfo("Rules applied", message)

    hashes_file, algorithm, output_file = prompt_user_for_input(BRUTE_FORCE)
    hashes = read_file_content(hashes_file, DICTIONARY)
    new_words = read_file_content(new_words_path, DICTIONARY) if new_words_path else None
    dictionary_attack_algorithm(hashes, new_words, algorithm, output_file)


def dictionary_attack_menu(print_main_menu):
    clear_screen()

    options = {
        "1": lambda: dictionary_attack(),
        "2": lambda: rainbow_table_attack_with_precomputed_table(print_main_menu),
        "3": lambda: rule_based_dictionary_attack(print_main_menu)
    }

    print("Dictionary attack options")
    dictionary_attack_options_table()

    choice = input("\nEnter the number of the attack you would like to perform:\n")

    if choice in options:
        options[choice]()
    else:
        dictionary_attack_menu(print_main_menu)


def dictionary_attack():
    clear_screen()

    hashes_file, algorithm, dictionary_file, out_file = prompt_user_for_input(DICTIONARY)

    hashes = read_file_content(hashes_file, DICTIONARY)
    words = read_file_content(dictionary_file, DICTIONARY) if dictionary_file else None

    dictionary_attack_algorithm(hashes, words, algorithm,  out_file)


def create_rainbow_table(print_main_menu, input_file, algorithm):
    with open(input_file, 'r') as file:
        plain_text_words = file.read().splitlines()

    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder to Save Rainbow Table")

    if not folder_selected:
        print("No folder selected. Rainbow table creation aborted.")
        retry = input("Do you want to try again? y/n\n")
        if retry.lower() == YES_CHOICE:
            create_rainbow_table_menu(print_main_menu)
        else:
            print_main_menu()

    file_name = os.path.splitext(os.path.basename(input_file))[0]
    rainbow_table_file = f"{file_name}_{algorithm}.txt"
    file_path = os.path.join(folder_selected, rainbow_table_file)

    if os.path.exists(file_path):
        overwrite = input(f"A file with the name '{rainbow_table_file}' already exists at the same location. "
                          f"Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != YES_CHOICE:
            index = 1
            while os.path.exists(file_path):
                rainbow_table_file = f"{file_name}_{algorithm}_{index}.txt"
                file_path = os.path.join(folder_selected, rainbow_table_file)
                index += 1

    with open(file_path, 'w') as file:
        for word in plain_text_words:
            hashed_values = hash_password(algorithm, word)
            hashed_value = ":".join(str(hashed) for hashed in hashed_values)
            file.write(f"{word}:{hashed_value}\n")

    message = f"Rainbow table created successfully.\nLocation: {file_path}"
    messagebox.showinfo("Rainbow Table Created", message)

    print_main_menu()


def create_rainbow_table_menu(print_main_menu):
    clear_screen()
    input_file = input("Enter the path to the dictionary file:\n")
    algorithm = input("Enter the hashing algorithm you would like to use:\n")

    create_rainbow_table(print_main_menu, input_file, algorithm)
