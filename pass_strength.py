import os
import sys
import getpass
import secrets
import string
import time

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = NORMAL = ""


COMMON_PASSWORDS = [
    "123456", "password", "qwerty", "admin", "letmein", "12345678", 
    "12345", "123456789", "123123", "password123"
]


def clear_screen():
    """Clears the terminal screen based on the OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    """Displays the startup ASCII logo and credits."""
    logo = f"""
{Fore.CYAN}{Style.BRIGHT}  ___               ___ _                  _   _   
 | _ \ __ _ __ ___ / __| |_ _ _ ___ _ _  _| |_| |_ 
 |  _/ _` (_-<_-<  \__ \  _| '_/ -_) ' \/ _` |  _| ' \\
 |_| \__,_/__/__/  |___/\__|_| \___|_||_\__, |\__|_||_|
                                         |___/
{Fore.WHITE}
                  {Fore.YELLOW}Made by Vision | GitHub: vision-dev1{Fore.WHITE}
    """
    print(logo)

def get_input(prompt):
    """Simple wrapper for input to handle styling."""
    return input(f"{Fore.GREEN}{prompt}{Fore.RESET}")

def get_password_input(prompt):
    """Standard password input (visible)."""
    return input(f"{Fore.GREEN}{prompt}{Fore.RESET}")


def check_password_strength():
    """Option 1: Analyzes password strength and provides feedback."""
    clear_screen()
    print_logo()
    print(f"{Fore.CYAN}--- Password Strength Checker ---{Fore.RESET}\n")
    
    password = get_password_input("Enter password to check: ")
    
    if not password:
        print(f"\n{Fore.RED}Empty password input.{Fore.RESET}")
        input("\nPress Enter to return to menu...")
        return

    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    is_common = password.lower() in [p.lower() for p in COMMON_PASSWORDS]

    score = 0
    suggestions = []

    if length >= 8: score += 1
    else: suggestions.append("Make it at least 8 characters long.")

    if has_upper: score += 1
    else: suggestions.append("Add uppercase letters.")

    if has_lower: score += 1
    else: suggestions.append("Add lowercase letters.")

    if has_digit: score += 1
    else: suggestions.append("Add numbers.")

    if has_special: score += 1
    else: suggestions.append("Add special characters (e.g., @, #, $, %).")

    print(f"\n{Fore.CYAN}Results:{Fore.RESET}")
    print(f"- Length: {length} characters")
    
    if is_common:
        print(f"{Fore.RED}[!] WARNING: This is a very common password!{Fore.RESET}")
        score = min(score, 1) # Cap score if it's common

    if score <= 3:
        rating = f"{Fore.RED}WEAK"
    elif score == 4:
        rating = f"{Fore.YELLOW}MEDIUM"
    else:
        rating = f"{Fore.GREEN}STRONG"

    print(f"- Strength Rating: {rating} {Fore.RESET}({score}/5)")

    if suggestions:
        print(f"\n{Fore.YELLOW}Suggestions for improvement:{Fore.RESET}")
        for s in suggestions:
            print(f"  • {s}")
    else:
        print(f"\n{Fore.GREEN}Great job! This password meets all basic security criteria.{Fore.RESET}")

    input("\nPress Enter to return to menu...")

def show_weak_examples():
    """Option 2: Displays weak password examples and explanations."""
    clear_screen()
    print_logo()
    print(f"{Fore.CYAN}--- Weak Password Examples ---{Fore.RESET}\n")
    
    for pwd in COMMON_PASSWORDS[:5]:
        print(f"{Fore.RED}• {pwd}{Fore.RESET}")
    
    print(f"\n{Fore.YELLOW}Why are these weak?{Fore.RESET}")
    print("1. {Style.BRIGHT}Predictability:{Style.NORMAL} They are easily guessed by humans.")
    print("2. {Style.BRIGHT}Dictionary Attacks:{Style.NORMAL} Automated tools test these first.")
    print("3. {Style.BRIGHT}Data Breaches:{Style.NORMAL} These appear in almost every leaked database.")
    
    input("\nPress Enter to return to menu...")

def generate_strong_password():
    """Option 3: Generates a secure random password."""
    clear_screen()
    print_logo()
    print(f"{Fore.CYAN}--- Strong Password Generator ---{Fore.RESET}\n")
    
    length_input = get_input("Desired password length (default 12, min 4): ")
    try:
        length = int(length_input) if length_input else 12
        if length < 4: length = 12
    except ValueError:
        length = 12

    # Required categories
    uppers = string.ascii_uppercase
    lowers = string.ascii_lowercase
    digits = string.digits
    symbols = string.punctuation
    all_chars = uppers + lowers + digits + symbols

    # Build password with guaranteed characters
    password_list = [
        secrets.choice(uppers),
        secrets.choice(lowers),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]
    
    # Fill the rest
    password_list += [secrets.choice(all_chars) for _ in range(length - 4)]
    
    # Shuffle to avoid predictable patterns (first 4 being types in order)
    secrets.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    
    print(f"\n{Fore.GREEN}Generated Password: {Fore.WHITE}{Style.BRIGHT}{password}{Fore.RESET}")
    print(f"{Fore.YELLOW}(Length: {length}){Fore.RESET}")
    
    input("\nPress Enter to return to menu...")

def exit_program():
    """Option 4: Exit the program."""
    clear_screen()
    print_logo()
    print(f"{Fore.MAGENTA}Thank you for using PassStrength! Stay secure.{Fore.RESET}")
    time.sleep(1.5)
    sys.exit()


def main():
    while True:
        clear_screen()
        print_logo()
        
        print(f"{Fore.CYAN}Main Menu:{Fore.RESET}")
        print(f"1. Check your password")
        print(f"2. Show weak password examples")
        print(f"3. Generate a strong password")
        print(f"4. Exit")
        
        choice = get_input("\nSelect an option (1-4): ")
        
        if choice == '1':
            check_password_strength()
        elif choice == '2':
            show_weak_examples()
        elif choice == '3':
            generate_strong_password()
        elif choice == '4':
            exit_program()
        else:
            print(f"\n{Fore.RED}Invalid selection. Please try again.{Fore.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program interrupted. Exiting...{Fore.RESET}")
        sys.exit()
