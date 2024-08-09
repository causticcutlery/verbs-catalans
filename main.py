import json
import os
import random
import unicodedata
import requests
import pygame
from playsound import playsound
from io import BytesIO
from bs4 import BeautifulSoup

# Path to the JSON file
json_file_path = os.path.join('llista de paraules', 'paraules.json')

# Function to load JSON data from the file
def load_verbs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            verbs = json.load(file)
        return verbs
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit()
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        exit()

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to remove accents from a string
def remove_accents(text):
    normalized_text = unicodedata.normalize('NFD', text)
    return ''.join([char for char in normalized_text if not unicodedata.combining(char)])

# Function to practice conjugations
def practice_conjugations(verbs, repetitions):
    score = 0

    for _ in range(repetitions):
        verb = random.choice(verbs)
        subject, conjugation = random.choice(list(verb['conjugacions'].items()))

        while True:
            clear_console()
            anglès = f" ({verb['anglès']})"
            print(f"Conjuga '{verb['català']}'{anglès} per '{subject}':")
            playsound(f'audio/{verb['català']}.mp3', False)
            answer = input("La teva resposta: ")

            # Remove accents from both the answer and the correct conjugation
            if remove_accents(answer.lower()) == remove_accents(conjugation):
                print(f"Correcte! La resposta correcta és '{conjugation}'.\n")
                score += 1
                input("Premeu Intro per continuar...")
                break
            else:
                print(f"Incorrecte. La resposta correcta era '{conjugation}'.\n")
                score -= 1
                input("Premeu Intro per tornar-ho a provar...")

    return score

# Main function to run the CLI menu
def main():
    clear_console()
    print("Benvinguts a la pràctica de conjugació de verbs en català!")

    verbs = load_verbs(json_file_path)

    while True:
        try:
            repetitions = int(input("Quantes repeticions t'agradaria practicar? "))
            if repetitions <= 0:
                print("Introduïu un número positiu.")
                continue
            break
        except ValueError:
            print("Introduïu un número vàlid.")

    score = practice_conjugations(verbs, repetitions)
    
    clear_console()
    print(f"Sessió de pràctica completada!\nLa teva puntuació: {score}/{repetitions}")
    input("Premeu Intro per continuar...")
    clear_console()

if __name__ == "__main__":
    main()
