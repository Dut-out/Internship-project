import random
import string

def password_generator():
    try:
        # Input length
        length = int(input("Enter desired password length: "))
        use_special = input("Include special characters? (y/n): ").lower() == 'y'
        
        characters = string.ascii_letters + string.digits
        if use_special:
            characters += string.punctuation
            
        # Output secure password
        password = "".join(random.choices(characters, k=length))
        print(f"\nGenerated Password: {password}")
    except ValueError:
        print("Please enter a valid number for length.")

if __name__ == "__main__":
    password_generator()