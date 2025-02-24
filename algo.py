import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import string
import subprocess
import zipfile  # Für das Komprimieren und Dekomprimieren

# Alphabet für die Verschlüsselung und Rückentschlüsselung
alphabet = [
    ("A", "Z"), ("B", "Y"), ("C", "X"), ("D", "W"), ("E", "V"),
    ("F", "U"), ("G", "T"), ("H", "S"), ("I", "R"), ("J", "Q"),
    ("K", "P"), ("L", "O"), ("M", "N"), ("N", "M"), ("O", "L"),
    ("P", "K"), ("Q", "J"), ("R", "I"), ("S", "H"), ("T", "G"),
    ("U", "F"), ("V", "E"), ("W", "D"), ("X", "C"), ("Y", "B"),
    ("Z", "A"), ("a", "z"), ("b", "y"), ("c", "x"), ("d", "w"),
    ("e", "v"), ("f", "u"), ("g", "t"), ("h", "s"), ("i", "r"),
    ("j", "q"), ("k", "p"), ("l", "Ö"), ("m", "o"), ("n", "m"),
    ("o", "l"), ("p", "k"), ("q", "j"), ("r", "i"), ("s", "h"),
    ("t", "g"), ("u", "f"), ("v", "e"), ("w", "d"), ("x", "c"),
    ("y", "b"), ("z", "a"), ("Ä", "ü"), ("Ö", "ß"), ("Ü", "ö"),
    ("ä", "Ä"), ("ö", "n"), ("ü", "Ü"), ("ß", "ä"),
    ("0", "9"), ("1", "8"), ("2", "7"), ("3", "6"), ("4", "5"),
    ("5", "4"), ("6", "3"), ("7", "2"), ("8", "1"), ("9", "0"),
    ("@", "#"), ("!", "?"), ("#", "@"), ("$", "%"), ("%", "$"),
    ("^", "&"), ("&", "^"), ("*", "("), ("(", "*"), (")", ")"),
    ("_", "-"), ("-", "_"), ("+", "="), ("=", "+"), ("[", "]"),
    ("]", "["), ("{", "}"), ("}", "{"), ("|", "\\"), ("\\", "|"),
    (";", ":"), (":", ";"), ("'", "\""), ("\"", "'"), (",", "<"),
    ("<", ","), (".", ">"), (">", "."), ("/", "?"), ("?", "/"),
    ("`", "~"), ("~", "`"), (" ", " ")
]

# Emoji-Tabelle mit eindeutigen Symbolen aus Wingdings
spassbilder_table = {
    "A": "😀", "B": "😃", "C": "😄", "D": "😁", "E": "😆",
    "F": "😅", "G": "😂", "H": "🤣", "I": "😊", "J": "😇",
    "K": "😉", "L": "😍", "M": "🥰", "N": "😘", "O": "😗",
    "P": "😋", "Q": "😜", "R": "🤪", "S": "😝", "T": "🤑",
    "U": "🤗", "V": "🤭", "W": "🤫", "X": "🤔", "Y": "🤨",
    "Z": "😐", "a": "😑", "b": "😶", "c": "😌", "d": "😏",
    "e": "😣", "f": "😥", "g": "😮", "h": "🤐", "i": "😯",
    "j": "😪", "k": "😫", "l": "😴", "m": "🙄", "n": "🥳",
    "o": "😎", "p": "🤓", "q": "🧐", "r": "🤠", "s": "😈",
    "t": "👿", "u": "👹", "v": "👺", "w": "💀", "x": "👻",
    "y": "👽", "z": "👾", "Ä": "🦄", "Ö": "🐉", "Ü": "🦋",
    "ä": "🌸", "ö": "🌼", "ü": "🌹", "ß": "🐝", " ": " ",
    ".": "⚫", ",": "⚪", "0": "🍏", "1": "🍐", "2": "🍊",
    "3": "🍋", "4": "🍌", "5": "🍉", "6": "🍇", "7": "🍓",
    "8": "🍒", "9": "🍑", "@": "🔑",
    "!": "🥳", "?": "🧐", "$": "💵", "%": "💸", "^": "💹", "&": "💼",
    "*": "💎", "(": "👛", ")": "👜", "_": "👗", "-": "👠",
    "+": "👒", "=": "🧢", "[": "🎩", "]": "👑", "{": "💍", "}": "📿",
    "|": "👓", "\\": "🥽", ":": "🎯", ";": "🎱", "'": "🎳", "\"": "🏆",
    "<": "🥇", ">": "🥈", "/": "🥉",  "`": "🎮",  "~": "🕹", "#": "🏅"
}

# Alphabet für die Verschlüsselung und Rückentschlüsselung
encryption_alphabet = {key: value for key, value in alphabet}
decryption_alphabet = {value: key for key, value in alphabet}

# Emoji-Tabelle und umgekehrte Tabelle
reverse_spassbilder_alphabet = {v: k for k, v in spassbilder_table.items()}

def delete_user_logs(data):
    """
    Verschlüsselt die eingegebenen Daten basierend auf dem benutzerdefinierten Alphabet.
    Arbeitet direkt auf Byte-Ebene, um binäre Daten verlustfrei zu verschlüsseln.
    """
    translated = bytearray()
    for byte in data:
        encrypted_byte = (byte + 128) % 256  # Einfache Verschiebung zur Verschlüsselung
        translated.append(encrypted_byte)
    return bytes(translated)

def restore_system_settings(data):
    """
    Entschlüsselt die Daten und stellt die ursprünglichen Zeichen basierend auf dem Alphabet wieder her.
    Arbeitet direkt auf Byte-Ebene, um binäre Daten verlustfrei zu entschlüsseln.
    """
    translated = bytearray()
    for byte in data:
        decrypted_byte = (byte - 128) % 256  # Entschlüsselung durch Rückverschiebung
        translated.append(decrypted_byte)
    return bytes(translated)

def generate_decoy_key(real_key, output_directory):
    """
    Generiert einen ablenkenden Schlüssel, bestehend aus zufälligen Emojis, und fügt den realen Schlüssel an einer
    zufälligen Stelle ein. Speichert die Position in einer separaten Lizenzdatei.
    """
    decoy_key = ''.join(random.choices(list(spassbilder_table.values()), k=100000))  # Ein langer zufälliger Emoji-String
    insertion_point = random.randint(0, len(decoy_key))
    full_key = decoy_key[:insertion_point] + decoy_key[insertion_point:]
    save_position_to_file(insertion_point, output_directory)
    return full_key

def save_position_to_file(position, output_directory):
    """
    Speichert die Position des echten Schlüssels in einer Lizenzdatei (Lizenz.txt).
    """
    license_path = os.path.join(output_directory, "Lizenz.CipherCore")
    with open(license_path, "w") as pos_file:
        pos_file.write(str(position))

def save_decoy_key_to_file(full_key, directory):
    """
    Speichert den ablenkenden Schlüssel in einer Datei (key.key).
    """
    key_path = os.path.join(directory, "k.CipherCore")
    with open(key_path, "w", encoding='utf-8') as key_file:
        key_file.write(full_key)

# Funktion zum Komprimieren der verschlüsselten Dateien
def dateien_komprimieren(dateinamen, kcp_datei_name):
    """
    Komprimiert alle angegebenen Dateien in eine .kcp-Datei.
    Nur .CipherCore und Metadaten (Lizenz und Schlüssel) werden komprimiert.
    """
    with zipfile.ZipFile(kcp_datei_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for datei in dateinamen:
            if os.path.exists(datei):
                zipf.write(datei, os.path.basename(datei))  # Fügt die Datei zur KCP-Datei hinzu
            else:
                print(f"Datei {datei} wurde nicht gefunden und wird übersprungen.")
    print(f"Dateien erfolgreich in {kcp_datei_name} komprimiert.")


# Funktion zum Entpacken der KCP-Datei
def kcp_entpacken(kcp_dateiname, ziel_ordner):
    """
    Entpackt die .kcp-Datei in den Zielordner.
    """
    if zipfile.is_zipfile(kcp_dateiname):
        with zipfile.ZipFile(kcp_dateiname, 'r') as zip_ref:
            zip_ref.extractall(ziel_ordner)  # Entpackt alle Dateien in den Zielordner
        print(f"{kcp_dateiname} erfolgreich entpackt.")
    else:
        print(f"{kcp_dateiname} ist keine gültige KCP-Datei oder ZIP-Datei.")

# Funktion zur Entschlüsselung der Datei
def datei_entschluesseln(input_file, output_directory):
    """
    Entschlüsselt die Datei und speichert sie unter dem ursprünglichen Namen.
    """
    try:
        # Pfad sicherstellen und überprüfen
        input_file = os.path.normpath(input_file)  # Normalisiert den Pfad, um Probleme mit doppelten Backslashes zu vermeiden
        print(f"Entschlüsselung von Datei: {input_file}")
        
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = restore_system_settings(encrypted_data)

        # Dateiname bereinigen und Pfad erstellen
        output_file = os.path.join(output_directory, os.path.basename(input_file).replace(".CipherCore", ""))
        output_file = os.path.normpath(output_file)  # Normalisiert den Pfad für das Speichern

        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"Datei {input_file} erfolgreich entschlüsselt und gespeichert unter {output_file}.")
    except Exception as e:
        print(f"Fehler bei der Entschlüsselung: {e}")



# Funktion zum Verschlüsseln von Dateien
# Funktion zum Verschlüsseln von Dateien
def encrypt_module(input_file, output_directory):
    """
    Verschlüsselt die Datei und speichert sie als .CipherCore-Datei.
    """
    # Erstelle die verschlüsselte .CipherCore Datei
    output_file = os.path.join(output_directory, os.path.basename(input_file) + ".CipherCore")
    with open(input_file, 'rb') as f:
        original_data = f.read()
    encrypted_data = delete_user_logs(original_data)
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

    # Schlüssel und Lizenzdateien erzeugen
    real_key = "".encode('utf-8')  # Beispiel für einen echten Schlüssel
    full_key = generate_decoy_key(real_key, output_directory)
    save_decoy_key_to_file(full_key, output_directory)

    # Komprimiere alle relevanten Dateien in eine .kcp-Datei
    cipher_files = [
        output_file,
        os.path.join(output_directory, "Lizenz.CipherCore"),
        os.path.join(output_directory, "k.CipherCore")
    ]
    kcp_file = os.path.join(output_directory, "archivierte_dateien.kcp")
    dateien_komprimieren(cipher_files, kcp_file)

    # Lösche die erstellten Dateien nach dem Komprimieren
    for datei in cipher_files:
        if os.path.exists(datei):
            os.remove(datei)
            print(f"{datei} wurde gelöscht.")






def load_encrypted_module(encrypted_file, output_file):
    """
    Entschlüsselt die Datei und speichert sie.
    """
    try:
        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = restore_system_settings(encrypted_data)
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
    except Exception as e:
        print(f"Fehler beim Entschlüsseln der Datei: {e}")

def send_email_via_system(subject, body, attachments):
    """
    Öffnet das Standard-E-Mail-Programm des Systems und fügt die Dateien als Anhänge ein.
    """
    attachment_paths = " ".join(f'"{attachment}"' for attachment in attachments)
    command = f'explorer "mailto:?subject={subject}&body={body}&attach={attachment_paths}"'
    subprocess.run(command, shell=True)


# Tkinter GUI
class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Datei Verschlüsselungs-/Entschlüsselungstool")
        self.root.geometry("500x400")

        self.file_paths = []
        self.output_directory = None

        self.select_files_button = tk.Button(root, text="Dateien auswählen", command=self.select_files)
        self.select_files_button.pack(pady=10)

        self.select_output_directory_button = tk.Button(root, text="Ausgabeverzeichnis auswählen", command=self.select_output_directory)
        self.select_output_directory_button.pack(pady=10)

        self.encrypt_button = tk.Button(root, text="Dateien verschlüsseln", command=self.encrypt_files)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(root, text="Dateien entschlüsseln", command=self.decrypt_files)  # Achte darauf, dass decrypt_files hier aufgerufen wird
        self.decrypt_button.pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(title="Wähle eine oder mehrere Dateien aus")
        if files:
            self.file_paths = list(files)
            messagebox.showinfo("Auswahl bestätigt", f"{len(self.file_paths)} Datei(en) ausgewählt.")

    def select_output_directory(self):
        directory = filedialog.askdirectory(title="Wähle das Ausgabeverzeichnis aus")
        if directory:
            self.output_directory = directory
            messagebox.showinfo("Auswahl bestätigt", f"Ausgabeverzeichnis: {self.output_directory}")

    def encrypt_files(self):
        if not self.file_paths:
            messagebox.showwarning("Warnung", "Keine Dateien ausgewählt!")
            return

        if not self.output_directory:
            messagebox.showwarning("Warnung", "Kein Ausgabeverzeichnis ausgewählt!")
            return

        try:
            for file_path in self.file_paths:
                encrypt_module(file_path, self.output_directory)
            messagebox.showinfo("Erfolg", "Dateien erfolgreich verschlüsselt und komprimiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Verschlüsselung: {e}")

    def decrypt_files(self):
        file_path = filedialog.askopenfilename(title="Wähle eine verschlüsselte Datei aus", filetypes=[("Verschlüsselte Dateien", "*.kcp *.CipherCore")])
        if not file_path:
            messagebox.showwarning("Warnung", "Keine Datei ausgewählt!")
            return

        try:
            # Wenn es eine KCP-Datei ist, entpacken und entschlüsseln
            if file_path.endswith(".kcp"):
                ziel_ordner = filedialog.askdirectory(title="Wähle einen Ordner zum Entpacken der KCP-Datei")
                if not ziel_ordner:
                    return
                kcp_entpacken(file_path, ziel_ordner)

                # Entschlüssele alle .CipherCore-Dateien im Zielordner
                for datei in os.listdir(ziel_ordner):
                    if datei.endswith(".CipherCore") and datei not in ["k.CipherCore", "Lizenz.CipherCore"]:
                        input_file = os.path.join(ziel_ordner, datei)
                        datei_entschluesseln(input_file, ziel_ordner)

                        # Nach der Entschlüsselung die .CipherCore-Datei löschen
                        os.remove(input_file)
                        print(f"{input_file} wurde nach der Entschlüsselung gelöscht.")

                # Lösche die Schlüssel- und Lizenzdateien nach der Entschlüsselung
                schluessel_datei = os.path.join(ziel_ordner, "k.CipherCore")
                lizenz_datei = os.path.join(ziel_ordner, "Lizenz.CipherCore")
                if os.path.exists(schluessel_datei):
                    os.remove(schluessel_datei)
                    print(f"{schluessel_datei} wurde gelöscht.")
                if os.path.exists(lizenz_datei):
                    os.remove(lizenz_datei)
                    print(f"{lizenz_datei} wurde gelöscht.")

                messagebox.showinfo("Erfolg", "Dateien erfolgreich entpackt, entschlüsselt und bereinigt.")
            else:
                # Wenn es keine KCP-Datei ist, nur entschlüsseln
                output_file = filedialog.asksaveasfilename(title="Speichere entschlüsselte Datei unter", initialfile=os.path.basename(file_path).replace(".CipherCore", ""))
                if output_file:
                    load_encrypted_module(file_path, output_file)
                    messagebox.showinfo("Erfolg", "Datei erfolgreich entschlüsselt.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Entschlüsselung: {e}")





if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()