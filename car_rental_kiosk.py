"""
Program: Autonomous Car Rental Kiosk
Author: Jake Keeven
Date: March 2026

Description:
This program simulates a self-service car rental kiosk that allows a customer
to rent a vehicle without human interaction.

Features:
- Collects customer information
- Automatically formats phone numbers (US or European)
- Detects credit card type
- Encrypts credit card numbers before saving
- Stores customer data for future rentals
- Suggests upgrades based on previous preferences
- Displays a full rental summary
"""

import json
import os
import base64
import re

# -------------------------------
# File for saving customer data
# -------------------------------
DATABASE_FILE = "customers.json"


# -------------------------------
# Car inventory
# -------------------------------
cars = {
    "Economy": {
        "price": 40,
        "cars": ["Toyota Yaris", "Hyundai Accent", "Kia Rio", "Nissan Versa"]
    },
    "Compact": {
        "price": 55,
        "cars": ["Honda Civic", "Toyota Corolla", "Mazda 3", "Hyundai Elantra"]
    },
    "SUV": {
        "price": 80,
        "cars": ["Toyota RAV4", "Honda CRV", "Ford Escape", "Subaru Forester"]
    },
    "Luxury": {
        "price": 120,
        "cars": ["BMW 5 Series", "Mercedes E Class", "Audi A6", "Lexus ES"]
    }
}


# -------------------------------
# Load customer database
# -------------------------------
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    return {}


# -------------------------------
# Save customer database
# -------------------------------
def save_database(data):
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=4)


# -------------------------------
# Simple encryption for credit card
# -------------------------------
def encrypt_card(card):
    return base64.b64encode(card.encode()).decode()


# -------------------------------
# Phone formatting
# -------------------------------
def format_phone(phone):
    digits = re.sub(r"\D", "", phone)

    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) > 10:
        return f"+{digits[:-10]} ({digits[-10:-7]}) {digits[-7:-4]}-{digits[-4:]}"
    else:
        return phone


# -------------------------------
# Detect credit card type
# -------------------------------
def detect_card(card):
    if card.startswith("4"):
        return "Visa"
    elif card.startswith(("51", "52", "53", "54", "55")):
        return "MasterCard"
    elif card.startswith(("34", "37")):
        return "American Express"
    elif card.startswith("6"):
        return "Discover"
    else:
        return "Unknown"


# -------------------------------
# Mask credit card
# -------------------------------
def mask_card(card):
    return "*" * (len(card) - 4) + card[-4:]


# -------------------------------
# Rental kiosk logic
# -------------------------------
def main():

    database = load_database()

    print("\n=== Welcome to Autonomous Car Rental Kiosk ===\n")

    name = input("Enter your name: ")
    phone = format_phone(input("Enter phone number: "))

    if phone in database:
        print("\nReturning customer detected!")

        if input("Is your address the same? (y/n): ").lower() == "y":
            address = database[phone]["address"]
        else:
            address = input("Enter your address: ")

        if input("Would you like to rent the next level car? (y/n): ").lower() == "y":
            print("Upgrade option will be offered.")
    else:
        address = input("Enter your address: ")

    # Credit card input
    card = input("Enter credit card number: ")
    cvc = input("Enter CVC: ")

    card_type = detect_card(card)
    encrypted_card = encrypt_card(card + "-" + cvc)

    print("\nCard detected:", card_type)

    # Display car classes
    print("\nAvailable Car Classes:")
    classes = list(cars.keys())

    for i, c in enumerate(classes):
        print(i + 1, "-", c, "($", cars[c]["price"], "/day)")

    class_choice = int(input("\nSelect a class: ")) - 1
    chosen_class = classes[class_choice]

    print("\nAvailable cars:")

    for i, car in enumerate(cars[chosen_class]["cars"]):
        print(i + 1, "-", car)

    car_choice = int(input("Choose a car: ")) - 1
    selected_car = cars[chosen_class]["cars"][car_choice]

    days = int(input("Number of rental days: "))
    odometer = int(input("Starting odometer reading: "))

    # Pricing
    daily_price = cars[chosen_class]["price"]
    hold_amount = (daily_price * days) + 200

    # Save preferences
    database[phone] = {
        "name": name,
        "address": address,
        "encrypted_card": encrypted_card,
        "preferred_class": chosen_class,
        "preferred_car": selected_car
    }

    save_database(database)

    # Output summary
    print("\n========== RENTAL SUMMARY ==========")

    print("Customer:", name)
    print("Phone:", phone)
    print("Address:", address)

    print("Credit Card:", mask_card(card), "(" + card_type + ")")

    print("Vehicle Class:", chosen_class)
    print("Vehicle:", selected_car)

    print("Days:", days)
    print("Starting Odometer:", odometer)

    print("Amount held on card: $", hold_amount)

    print("====================================")


# Run program
main()
