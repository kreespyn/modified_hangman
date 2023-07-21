import os
import random
import time
from functools import reduce


def logo_hangman():
    print('''
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   █   █   █████   █   █   █████   █   █   █████   █   █   ║
    ║   █   █   █   █   ██  █   █       ██ ██   █   █   ██  █   ║
    ║   █████   █████   █ █ █   █████   █ █ █   █████   █ █ █   ║
    ║   █   █   █   █   █  ██   █   █   █   █   █   █   █  ██   ║
    ║   █   █   █   █   █   █   █████   █   █   █   █   █   █   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
''')


def image_hangman(deaths):
    # Lista de imágenes del ahorcado en formato ASCII art.
    # Cada elemento de la lista representa una etapa del ahorcado según el número de errores cometidos.
    hangman_images = [
        '''














        ''',
        '''
        
        
        _____________
      /             /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔
          ║
          ║
          ║
          ║
          ║
          ║
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║
          ║
          ║
          ║
          ║
          ║
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║
          ║
          ║
          ║
          ║
          ║   d   b
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║
          ║
          ║
          ║
          ║    / \\
          ║   d   b
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║
          ║
          ║
          ║     │
          ║    / \\
          ║   d   b
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║
          ║
          ║    ─┼─
          ║     │
          ║    / \\
          ║   d   b
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║
          ║
          ║   ┌─┼─┐
          ║     │
          ║    / \\
          ║   d   b
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║
          ║     @
          ║   ┌─┼─┐
          ║     │
          ║    / \\
          ║   d   b
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║     │
          ║     @       ¡AHORCADO!
          ║   ┌─┼─┐
          ║     │
          ║    / \\
          ║   d   b
        __║__________
      /   ║         /|
     /____________ / |
    |             | /
    |_____________|/
        ''',
        '''
          ╔═════╦  
          ║
          ║     
          ║
          ║              ¡GANASTE!
          ║
          ║                  
        __║__________        @
      /   ║         /|     └─┼─┘  
     /____________ / |       │
    |             | /       / \\
    |_____________|/       d   b
        '''
    ]

    return hangman_images[deaths]


def read_word():
    # Leer el archivo data.txt y seleccionar una palabra aleatoria
    with open('./archivos/data.txt', 'r', encoding='utf-8') as data_words:
        word = random.choice([word.strip().upper() for word in data_words])
    return word


def new_word():
    word = read_word()
    dict_word = {i: letter for i, letter in enumerate(word)}
    discovered = ['- ' for _ in range(len(dict_word))]
    deaths = 0
    letters = list('ABCDEFGHIJKLMNÑOPQRSTUVWXYZ')
    return word, dict_word, discovered, deaths, letters


def compare_letter(letter, dict_word, discovered, fail):
    # Compara la letra ingresada con las letras de la palabra.
    # Si se encuentra una coincidencia, actualiza la lista de letras descubiertas.
    for index, char in dict_word.items():
        if char == letter:
            discovered[index] = letter + ' '
            fail = False
    return discovered, fail


def refresh(deaths, letters, discovered):
    os.system('clear')
    logo_hangman()
    print('Letras disponibles: ' + "  ".join(letters))
    print(image_hangman(deaths))
    print("".join(discovered))


def run():
    word, dict_word, discovered, deaths, letters = new_word()
    non_letter = False

    while True:
        refresh(deaths, letters, discovered)

        if non_letter:
            print('Debes ingresar una de las letras disponibles')
            non_letter = False

        try:
            letter = input('¡Adivina la palabra! Ingresa una letra: ').upper()

            # Validar si la entrada es una letra válida
            if letter not in letters:
                raise ValueError

            letters.remove(letter)
        except ValueError:
            non_letter = True
            continue

        fail = True
        discovered, fail = compare_letter(letter, dict_word, discovered, fail)

        if fail:
            deaths += 1
            if deaths == 10:
                refresh(deaths, letters, discovered)
                print('¡Perdiste! La palabra era', word)
                again = input('¿Quieres jugar otra vez? (1-Si 0-No): ')
                if again == '1':
                    word, dict_word, discovered, deaths, letters = new_word()
                    continue
                else:
                    print('Gracias por jugar :)')
                    break

        if ''.join(discovered).replace(' ', '') == word:
            refresh(11, letters, discovered)
            print('Tuviste', deaths, 'errores      ' + ''.join(discovered))
            again = input('¿Quieres jugar otra vez? (1-Si 0-No): ')
            if again == '1':
                word, dict_word, discovered, deaths, letters = new_word()
                continue
            else:
                print('Gracias por jugar :)')
                break


if __name__ == '__main__':
    os.system('clear')
    run()
