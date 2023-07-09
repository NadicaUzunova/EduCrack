# EduCrack

EduCrack is a program for password cracking. It provides various methods of cracking passwords using brute force and dictionary attacks.

## Main Menu

The program starts by displaying the main menu. Users can choose from different cracking methods or access the program's help and usage instructions.

To select an option, enter the corresponding number from the menu. If the user wants to access the help, enter the number 4. This will display the help window.

The help window provides a brief description of each attack method and their available options. It also explains the input arguments and supported hashing algorithms. Press the Esc key to return to the main menu.

## Brute Force Attack

To choose the brute force attack option, enter the number 1 in the main menu. This will display the brute force attack options. There are two options available:

1. Classic Brute Force Attack: This option tries all possible combinations of characters until it finds the password.

2. Brute Force Mask Attack: This option attempts to crack the password using all possible combinations of characters but only considers the characters specified by the user in the mask input.

## Dictionary Attack

To choose the dictionary attack option, enter the number 2 in the main menu. This will display the dictionary attack options. There are three options available:

1. Classic Dictionary Attack: This option performs a dictionary attack by systematically testing a list of commonly used words, phrases, or passwords against the target hashed passwords.

2. Dictionary Attack with Precomputed Hashes: This option involves comparing a list of precomputed hashes (commonly known as a "rainbow table") with the target hashed passwords to find matches. This method significantly speeds up the password cracking process.

3. Rule-Based Dictionary Attack: This option is similar to the classic dictionary attack but allows the user to generate variations of passwords based on specified rules. It increases the number of tested passwords, especially when certain patterns or rules are known.

## Usage

For each attack method, the program prompts the user to enter the required parameters, such as the input file containing hashed passwords, dictionary file, and hashing algorithm. Once the necessary data is provided, the program starts the attack process. It systematically generates passwords and calculates their hashes using the specified algorithm. The generated hashes are then compared with the target hashed passwords. If a match is found, it means the password has been cracked. In this case, the password and its corresponding hashed value are displayed and optionally saved to an output file. If no match is found, the program notifies the user of an unsuccessful attempt.

## Download Instructions

If you want to download and run the EduCrack program, follow these steps:

1. Go to the /download folder in this repository.
2. Click on the executable file (educrack.exe) to start the download.
3. Once the download is complete, navigate to the downloaded file on your computer.

### Running the Executable

To run the EduCrack program:

- For Windows: Double-click on the downloaded executable file (`educrack.exe`) to launch the program.

Please note that the provided instructions assume you are using a Windows operating system. If you are using a different operating system, please refer to the appropriate instructions for running executables on your specific platform.

Make sure to review the system requirements and any additional dependencies mentioned in the previous sections to ensure compatibility and proper execution of the EduCrack program.


## This program was created within the scope of my thesis research solely for educational purposes.
