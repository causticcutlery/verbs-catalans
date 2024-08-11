import json
import os
import random
import unicodedata
import requests
import pygame
from playsound import playsound
from playsound import PlaysoundException
from io import BytesIO
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings() 

# Path to the JSON file
json_file_path = os.path.join('llista de paraules', 'paraules.json')

# Read API key from file
with open("api.key", 'r') as file:
    API_KEY = file.read().strip()


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

# def make_word_list(verbs):
#     llista_de_paraules = []

#     for verb in verbs:
#         català = verb['català']
#         anglès = verb['anglès']
        
#         for persona, conjugacion in verb['conjugacions'].items():
#             llista_de_paraules.append({
#                 'catala': català,
#                 'angles': anglès,
#                 'conjugacion': conjugacion,
#                 'persona': persona
#             })

#     return llista_de_paraules

# Function to practice conjugations
def practice_conjugations(verbs, repetitions):
    score = 0

    for i in range(repetitions):
        random.shuffle(verbs)
        verb = verbs[i % len(verbs)]

        subject, conjugation = random.choice(list(verb['conjugacions'].items()))

        while True:
            clear_console()
            anglès = f" ({verb['anglès']})"
            print(f"Conjuga '{verb['català']}'{anglès} per '{subject}':")

            answer = "rr"
            while answer == "rr":
                play_audio(verb['català'])
                answer = input("La teva resposta ('rr' per repetir): ")
            

            # Remove accents from both the answer and the correct conjugation
            if remove_accents(answer.lower()) == remove_accents(conjugation):
                print(f"Correcte! La resposta correcta és '{conjugation}'.\n")
                
                score += 1
                answer = "rr"
                while answer == "rr":
                    play_audio(conjugation)
                    answer = input("Premeu Intro per continuar ('rr' per repetir)...")
                break
            else:
                print(f"Incorrecte. La resposta correcta era '{conjugation}'.\n")
                score -= 1
                input("Premeu Intro per tornar-ho a provar...")

    return score

def download_audio(verb):
    url = f"https://apifree.forvo.com/key/{API_KEY}/format/json/action/word-pronunciations/word/{verb}/language/ca"
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        
        # Assuming you want the first pronunciation in the list
        if 'items' in data and len(data['items']) > 0:
            mp3_url = data['items'][0]['pathmp3']
            
            # Download the mp3 file
            audio_response = requests.get(mp3_url, verify=False)
            if audio_response.status_code == 200:
                file_path = f'audio/{verb}.mp3'
                with open(file_path, 'wb') as file:
                    file.write(audio_response.content)
                return file_path
            else:
                file_path = f'audio/{verb}.mp3'
                with open(file_path, 'wb') as file:
                    file.write()
    return None

# def play_audio(verb):
#     try:
#         playsound(f'audio/{verb}.mp3', False)
#     except PlaysoundException:
#         pass

def play_audio(verb):
    verb = remove_accents(verb)
    file_path = f'audio/{verb}.mp3'
    
    if not os.path.exists(file_path):
        print(f"File not found locally. Downloading {verb}.mp3...")
        file_path = download_audio(verb)
        if not file_path:
            print(f"Failed to download {verb}.mp3")
            # open(file_path, 'a').close()
            # return
            pass
    
    try:
        playsound(file_path, False)
    except Exception as e:
        # print(f"Error playing sound: {e}")
        pass

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
