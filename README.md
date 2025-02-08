# EduCrack

## Overview
**EduCrack** is an advanced password cracking tool designed for educational and research purposes. It implements various password recovery techniques, including brute-force and dictionary-based attacks, to analyze and understand password vulnerabilities. The program provides an interactive interface that allows users to select different cracking methods, configure attack parameters, and retrieve cracked passwords efficiently.

## Features
- **Brute Force Attacks**
  - **Classic Brute Force**: Tries all possible character combinations until the correct password is found.
  - **Brute Force Mask**: Attempts password cracking with user-defined character sets and structures.
- **Dictionary Attacks**
  - **Classic Dictionary Attack**: Tests a list of commonly used passwords against the target hashes.
  - **Dictionary Attack with Precomputed Hashes**: Uses a "rainbow table" for faster cracking.
  - **Rule-Based Dictionary Attack**: Generates password variations based on user-defined rules.
- **User-Friendly Interface**
  - Main menu for selecting attack types and configurations.
  - Help section with detailed explanations of attack methods and hashing algorithms.
- **Supports Multiple Hashing Algorithms**
  - SHA-256, SHA-512, MD5, and more.
- **Customizable Parameters**
  - Users can specify input files, dictionaries, hash algorithms, and output files.
- **Real-Time Progress and Reporting**
  - Displays ongoing attack progress and results.

## Installation and Usage

### Downloading EduCrack
To download and run the **EduCrack** program, follow these steps:

1. Navigate to the `/download` folder in this repository.
2. Download the executable file: **educrack.exe**.
3. Locate the downloaded file on your system.

### Running EduCrack

#### Windows Users:
1. Double-click **educrack.exe** to launch the program.
2. Follow the on-screen instructions to select an attack method and provide input files.

#### Linux/Mac Users:
EduCrack is primarily designed for Windows. If you are using a different operating system, consider running it in a Windows virtual machine or using a compatibility layer like **Wine**.

### Attack Methods

#### **Brute Force Attack**
1. Select **Option 1** in the main menu.
2. Choose:
   - **Classic Brute Force Attack** (Tests all character combinations)
   - **Brute Force Mask Attack** (Uses a predefined character set and structure)
3. Configure the attack parameters and start cracking.

#### **Dictionary Attack**
1. Select **Option 2** in the main menu.
2. Choose from:
   - **Classic Dictionary Attack** (Tests common passwords from a wordlist)
   - **Dictionary Attack with Precomputed Hashes** (Faster lookup-based cracking)
   - **Rule-Based Dictionary Attack** (Applies password mutation rules)
3. Provide the required input files and hashing algorithm.

### Output
- If a password is cracked, it is displayed alongside its hashed value.
- Results can be optionally saved to a specified output file.
- If the attack is unsuccessful, the program notifies the user.

## Help and Documentation
For assistance, select **Option 4** in the main menu to access the help window. It provides:
- Descriptions of attack methods
- Supported hashing algorithms
- Explanation of required input arguments
- Instructions on how to exit the help menu (press **Esc** to return to the main menu)

## System Requirements
- **Operating System**: Windows 10/11 (or Wine on Linux/macOS)
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: At least 50MB of free space
- **Dependencies**: No additional dependencies required

## Disclaimer
**EduCrack** was developed as part of a **bachelor’s thesis research project** and is intended **solely for educational and ethical security research purposes**. Unauthorized or illegal use of this tool is strictly prohibited. The author assumes no liability for misuse.

## License
This project is open-source and distributed under the MIT License. Feel free to modify and contribute while adhering to ethical hacking practices.

---

For any inquiries, suggestions, or contributions, please open an issue in this repository or contact the author.
