import smtplib
import random
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Simulating a simple user database (email:password)
user_data = {}

# Function to generate a random 9-digit reset code
def generate_reset_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

# Function to send the reset code to the user's email
def send_reset_code(email, reset_code):
    sender_email = "enteryouremail@here.com"  # Replace with your email
    receiver_email = email
    password = "enteryouemailapppasswordhere"  # Replace with your email password (or use app-specific password)

    # Setting up the email content
    subject = "Password Reset Request"
    body = f"Your 9-digit password reset code is: {reset_code}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Sending the email via Gmail's SMTP server
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"{Fore.GREEN}A reset code has been sent to {email}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")

# Function to sign up a new user
def sign_up():
    print(f"{Fore.CYAN}Sign Up")
    email = input(f"{Fore.YELLOW}Enter your email: ")

    # Check if email is already registered
    if email in user_data:
        print(f"{Fore.RED}This email is already registered. Please log in or reset your password.")
        return None
    
    password = input(f"{Fore.YELLOW}Enter your password: ")

    # Store the new user in the database
    user_data[email] = {"password": password, "reset_attempts": 0}
    print(f"{Fore.GREEN}Sign up successful! You can now log in.")

    return email

# Function to authenticate user
def authenticate_user():
    print(f"{Fore.CYAN}Login")
    
    email = input(f"{Fore.YELLOW}Enter your email: ")
    if email not in user_data:
        print(f"{Fore.RED}No account found with that email. Please sign up or reset your password.")
        return None
    
    password = input(f"{Fore.YELLOW}Enter your password: ")
    
    if user_data[email]["password"] == password:
        print(f"{Fore.GREEN}Authentication successful! You can now play the game.")
        return email
    else:
        print(f"{Fore.RED}Invalid password.")
        return None

# Function to reset password
def reset_password(email):
    if user_data[email]["reset_attempts"] >= 3:
        print(f"{Fore.RED}You have reached the maximum number of password reset attempts.")
        return False
    
    print(f"{Fore.CYAN}\nPassword Reset")
    reset_code = generate_reset_code()
    send_reset_code(email, reset_code)
    
    # Simulate checking the reset code
    entered_code = input(f"{Fore.YELLOW}Enter the reset code sent to your email: ")
    
    if entered_code == reset_code:
        new_password = input(f"{Fore.YELLOW}Enter your new password: ")
        user_data[email]["password"] = new_password
        user_data[email]["reset_attempts"] = 0  # Reset the reset attempts after successful reset
        print(f"{Fore.GREEN}Your password has been successfully reset!")
        return True
    else:
        user_data[email]["reset_attempts"] += 1
        print(f"{Fore.RED}Invalid reset code. Try again.")
        return False

# Function to play the gambling game
def play_game(email):
    print(f"\n{Fore.MAGENTA}Welcome to the Number Betting Game!")
    
    # Player's balance (for simplicity, they start with 100 money)
    balance = 100
    
    # Game loop
    while balance > 0:
        print(f"\n{Fore.BLUE}Your current balance: ${balance}")
        
        # Asking the player to place a bet
        bet = int(input(f"{Fore.YELLOW}Place your bet (or enter 0 to exit): "))
        
        if bet == 0:
            print(f"{Fore.GREEN}Exiting the game. Your final balance is ${balance}")
            break
        
        if bet > balance:
            print(f"{Fore.RED}You don't have enough balance. Try again!")
            continue
        
        # Generate a random number between 1 and 10 (simulate the game outcome)
        number = random.randint(1, 10)
        
        print(f"\n{Fore.CYAN}The random number is: {number}")
        
        # Simple betting rule: if the number is greater than 5, the player wins
        if number > 5:
            print(f"{Fore.GREEN}You win! You double your bet.")
            balance += bet
        else:
            print(f"{Fore.RED}You lose! You lose your bet.")
            balance -= bet
        
        if balance <= 0:
            print(f"\n{Fore.RED}You're out of money! Game over.")
            break

# Main function
def main():
    while True:
        print(f"\n{Fore.MAGENTA}Welcome to the Game Hub!")
        print(f"{Fore.YELLOW}1. Sign Up")
        print(f"{Fore.YELLOW}2. Login")
        print(f"{Fore.YELLOW}3. Reset Password")
        print(f"{Fore.YELLOW}4. Exit")
        choice = input(f"{Fore.CYAN}What would you like to do? ").strip()
        
        if choice == '1':
            # Sign up new user
            email = sign_up()
            if email:
                play_game(email)
        elif choice == '2':
            # Log in existing user
            email = authenticate_user()
            if email:
                play_game(email)
        elif choice == '3':
            # Reset password
            email = input(f"{Fore.YELLOW}Enter your email to reset your password: ")
            if email in user_data:
                if reset_password(email):
                    continue
            else:
                print(f"{Fore.RED}No account found with that email.")
        elif choice == '4':
            print(f"{Fore.CYAN}Thank you for using the Game Hub. Goodbye!")
            break
        else:
            print(f"{Fore.RED}Invalid option. Please try again.")

if __name__ == "__main__":
    main()
