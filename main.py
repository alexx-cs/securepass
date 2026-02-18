import customtkinter as ctk
import random
import string
import json
import os

# ==========================
# CONFIGURAÇÕES INICIAIS
# ==========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

HISTORY_FILE = "password_history.json"
password_history = []

# ==========================
# FUNÇÃO: Calcular força
# ==========================
def calculate_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    return score


def update_strength_bar(password):
    score = calculate_strength(password)
    strength_bar.set(score / 4)

    if score <= 1:
        strength_label.configure(text="Strength: Weak", text_color="red")
    elif score == 2:
        strength_label.configure(text="Strength: Medium", text_color="orange")
    elif score == 3:
        strength_label.configure(text="Strength: Strong", text_color="yellow")
    else:
        strength_label.configure(text="Strength: Very Strong", text_color="green")


# ==========================
# GERAR SENHA
# ==========================
def generate_password():
    try:
        length = int(length_entry.get())
    except ValueError:
        result_entry.delete(0, "end")
        result_entry.insert(0, "Invalid length")
        return

    characters = string.ascii_lowercase

    if uppercase_var.get():
        characters += string.ascii_uppercase
    if numbers_var.get():
        characters += string.digits
    if symbols_var.get():
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))

    result_entry.delete(0, "end")
    result_entry.insert(0, password)

    update_strength_bar(password)


# ==========================
# COPIAR PARA ÁREA DE TRANSFERÊNCIA
# ==========================
def copy_to_clipboard():
    password = result_entry.get()
    app.clipboard_clear()
    app.clipboard_append(password)


# ==========================
# SALVAR HISTÓRICO
# ==========================
def save_password():
    password = result_entry.get()

    if password and password != "Invalid length":
        password_history.append(password)

        if len(password_history) > 10:
            password_history.pop(0)

        save_history_to_file()
        update_history_display()


def save_history_to_file():
    with open(HISTORY_FILE, "w") as file:
        json.dump(password_history, file)


def load_history_from_file():
    global password_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            password_history = json.load(file)


def update_history_display():
    history_box.configure(state="normal")
    history_box.delete("1.0", "end")

    for pwd in password_history:
        history_box.insert("end", pwd + "\n")

    history_box.configure(state="disabled")


# ==========================
# INTERFACE
# ==========================
app = ctk.CTk()
app.title("SecurePass Pro")
app.geometry("520x700")

title = ctk.CTkLabel(app, text="🔐 SecurePass Pro",
                     font=("Arial", 22, "bold"))
title.pack(pady=20)

length_label = ctk.CTkLabel(app, text="Password Length")
length_label.pack()

length_entry = ctk.CTkEntry(app, width=200)
length_entry.insert(0, "12")
length_entry.pack(pady=10)

uppercase_var = ctk.BooleanVar()
numbers_var = ctk.BooleanVar()
symbols_var = ctk.BooleanVar()

ctk.CTkCheckBox(app, text="Include Uppercase", variable=uppercase_var).pack(pady=5)
ctk.CTkCheckBox(app, text="Include Numbers", variable=numbers_var).pack(pady=5)
ctk.CTkCheckBox(app, text="Include Symbols", variable=symbols_var).pack(pady=5)

generate_button = ctk.CTkButton(app,
                                text="Generate Password",
                                command=generate_password)
generate_button.pack(pady=15)

result_entry = ctk.CTkEntry(app, width=350)
result_entry.pack(pady=10)

copy_button = ctk.CTkButton(app,
                            text="Copy to Clipboard",
                            command=copy_to_clipboard)
copy_button.pack(pady=5)

save_button = ctk.CTkButton(app,
                            text="Save Password",
                            command=save_password)
save_button.pack(pady=10)

strength_label = ctk.CTkLabel(app, text="Strength: -")
strength_label.pack(pady=5)

strength_bar = ctk.CTkProgressBar(app, width=300)
strength_bar.set(0)
strength_bar.pack(pady=10)

history_label = ctk.CTkLabel(app, text="Last 10 Saved Passwords")
history_label.pack(pady=15)

history_box = ctk.CTkTextbox(app, width=400, height=150)
history_box.pack()
history_box.configure(state="disabled")

load_history_from_file()
update_history_display()

app.mainloop()

