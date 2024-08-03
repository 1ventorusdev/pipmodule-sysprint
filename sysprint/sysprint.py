import threading
import time
import re
import sys
import datetime

# Fonction pour calculer la longueur visible d'une chaîne en ignorant les codes d'échappement ANSI
def visible_length(s):
    ansi_escape = re.compile(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]')
    return len(ansi_escape.sub('', s))

# Fonction pour centrer une chaîne en tenant compte des codes ANSI
def center_with_ansi(s, width):
    vis_len = visible_length(s)
    total_padding = width - vis_len
    if total_padding <= 0:
        return s
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    return ' ' * left_padding + s + ' ' * right_padding

# Fonction pour afficher une frame de chargement
def print_loading_frame(symbol, text, position):
    frame = [' '] * 12
    sym_len = visible_length(symbol)
    for i in range(sym_len):
        frame[(position + i) % len(frame)] = symbol
    print(f"[{''.join(frame)}]  {text}", end='\r')

class Print:
    @staticmethod
    def status(align, status, text):
        # Assurez-vous que la longueur du statut est au moins de 12 caractères
        min_length = 12
        status_length = visible_length(status)
        if status_length < min_length:
            padding = (min_length - status_length) // 2
            status = ' ' * padding + status + ' ' * (min_length - status_length - padding)

        # Centre le statut s'il est demandé
        if align == 'c':
            status = center_with_ansi(status, min_length)
        
        # Diviser le texte en plusieurs lignes
        lines = text.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            if i == 0:
                formatted_lines.append(f"[{status}]  {line}")
            else:
                formatted_lines.append(f"{' ' * (min_length + 2)}  {line}")
        
        # Affiche le texte avec le formatage spécial
        print('\n'.join(formatted_lines))

    class Loading:
        @staticmethod
        def bar(symbol, text, function, end_symbol="OK"):
            stop_loading = threading.Event()

            def animate():
                position = 0
                while not stop_loading.is_set():
                    print_loading_frame(symbol, text, position)
                    position = (position + 1) % 12
                    time.sleep(0.2)

            animation_thread = threading.Thread(target=animate)
            animation_thread.start()

            try:
                function()
            finally:
                stop_loading.set()
                animation_thread.join()
                end_frame = center_with_ansi(end_symbol, 12)  # Ensure the end frame is centered within 12 characters
                print(f"[{end_frame}]  {text}")

        
        def spinner(message, func):
            # Les symboles pour la roue de chargement
            spinner_symbols = ['|', '/', '-', '\\']
            stop_spinner = threading.Event()

            def animate():
                index = 0
                while not stop_spinner.is_set():
                    sys.stdout.write(f'\r{message} {spinner_symbols[index]}')
                    sys.stdout.flush()
                    index = (index + 1) % len(spinner_symbols)
                    time.sleep(0.1)

            animation_thread = threading.Thread(target=animate)
            animation_thread.start()

            try:
                func()
            finally:
                stop_spinner.set()
                animation_thread.join()
                # Afficher "Fait" à la fin de l'exécution
                sys.stdout.write(f'\r{message} Fait\n')
                sys.stdout.flush()

class Execute:
    def list(symbol, list, end_symbol="OK"):
        Print.status("c", "info", "start operation...")
        for func in list:
            text = f"function {func.__name__}"
            Print.Loading.bar(symbol, text, func, end_symbol)
        Print.status("c", "info", "operation is finish !")

    def dico(symbol, dico, end_symbol="OK"):
        # Affiche le début de l'opération
        Print.status("c", "info", "start operation...")
        
        for func, text in dico.items():
            # Affiche le texte associé à chaque fonction avec le chargement
            Print.Loading.bar(symbol, text, func, end_symbol)
        
        # Affiche la fin de l'opération
        Print.status("c", "info", "operation is finish !")


def timer():
    return f"[{datetime.datetime.now().strftime('%H:%M:%S')}.{datetime.datetime.now().microsecond // 1000:03d}]  "