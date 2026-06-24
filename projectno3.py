import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets
import pyperclip
from PIL import Image, ImageDraw, ImageTk
import io


# ---------------- Password Logic ---------------- #

def check_password_strength(password):

    strength = 0

    lower = upper = number = space = special = 0

    for char in password:

        if char in string.ascii_lowercase:
            lower += 1

        elif char in string.ascii_uppercase:
            upper += 1

        elif char in string.digits:
            number += 1

        elif char == " ":
            space += 1

        else:
            special += 1


    strength += (lower > 0)
    strength += (upper > 0)
    strength += (number > 0)
    strength += (space > 0)
    strength += (special > 0)


    if strength == 1:
        remark = "Very weak password"

    elif strength == 2:
        remark = "Weak password"

    elif strength == 3:
        remark = "Average password"

    elif strength == 4:
        remark = "Strong password"

    else:
        remark = "Very strong password 🔐"


    result = f"""
Password Analysis

Lowercase letters : {lower}
Uppercase letters : {upper}
Numbers           : {number}
Spaces            : {space}
Special chars     : {special}

Password Score : {strength}/5

Status:
{remark}
"""

    return result, strength



def check_password():

    password = password_entry.get()

    result, strength = check_password_strength(password)


    output.config(state="normal")
    output.delete("1.0","end")
    output.insert("end",result)
    output.config(state="disabled")


    progress["value"] = strength * 20


    if strength < 3:
        progress.configure(style="Red.Horizontal.TProgressbar")

    elif strength < 5:
        progress.configure(style="Orange.Horizontal.TProgressbar")

    else:
        progress.configure(style="Green.Horizontal.TProgressbar")



def generate_password():

    password = ''.join(
        secrets.choice(
            string.ascii_letters +
            string.digits +
            string.punctuation
        )
        for _ in range(12)
    )

    password_entry.delete(0,"end")
    password_entry.insert(0,password)



def copy_password():

    password = password_entry.get()

    if password:

        pyperclip.copy(password)

        status.config(
            text="✔ Password copied to clipboard"
        )

    else:

        messagebox.showwarning(
            "Empty",
            "Generate password first"
        )



def clear():

    password_entry.delete(0,"end")

    output.config(
        state="normal"
    )

    output.delete(
        "1.0",
        "end"
    )

    output.config(
        state="disabled"
    )

    progress["value"]=0





# Color Palette
DARK_BG = "#0a0e27"
CARD_BG = "#111827"
INPUT_BG = "#1a1f3a"
ACCENT_CYAN = "#00d9ff"
ACCENT_PURPLE = "#b537f2"
ACCENT_BLUE = "#2563eb"
SUCCESS_GREEN = "#10b981"
WARNING_ORANGE = "#f59e0b"
DANGER_RED = "#ef4444"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#a0aec0"
BORDER_COLOR = "#1e293b"

# Global variables for UI elements
password_visible = False
strength_labels = ["Very Weak", "Weak", "Average", "Strong", "Very Strong"]


def create_gradient_image(width, height, color1, color2):
    """Create a gradient image for backgrounds"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Convert hex to RGB
    c1 = tuple(int(color1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    c2 = tuple(int(color2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    for y in range(height):
        ratio = y / height
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return ImageTk.PhotoImage(img)


def toggle_password_visibility():
    """Toggle show/hide password"""
    global password_visible
    password_visible = not password_visible
    
    if password_visible:
        password_entry.config(show="")
        eye_button.config(text="👁 Hide")
    else:
        password_entry.config(show="●")
        eye_button.config(text="👁 Show")


def on_button_enter(event):
    """Hover effect for buttons"""
    event.widget.config(relief="raised", bd=2)


def on_button_leave(event):
    """Remove hover effect"""
    event.widget.config(relief="flat", bd=0)


def update_strength_display(strength):
    """Update strength meter label and styling"""
    labels = ["Very Weak", "Weak", "Average", "Strong", "Very Strong"]
    colors_hex = [DANGER_RED, WARNING_ORANGE, "#fbbf24", SUCCESS_GREEN, "#22d3ee"]
    
    strength_label.config(text=labels[strength - 1] if 1 <= strength <= 5 else "Unknown")
    
    # Update progress bar color
    if strength <= 1:
        progress.configure(style="Danger.Horizontal.TProgressbar")
    elif strength == 2:
        progress.configure(style="Warning.Horizontal.TProgressbar")
    elif strength == 3:
        progress.configure(style="Info.Horizontal.TProgressbar")
    elif strength == 4:
        progress.configure(style="Success.Horizontal.TProgressbar")
    else:
        progress.configure(style="Excellent.Horizontal.TProgressbar")


def check_password():
    password = password_entry.get()
    result, strength = check_password_strength(password)
    
    output.config(state="normal")
    output.delete("1.0", "end")
    output.insert("end", result)
    output.config(state="disabled")
    
    progress["value"] = strength * 20
    update_strength_display(strength)
    
    status.config(text="✔ Password analyzed")


def generate_password():
    password = ''.join(
        secrets.choice(
            string.ascii_letters +
            string.digits +
            string.punctuation
        )
        for _ in range(12)
    )
    
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    password_visible = False
    password_entry.config(show="●")
    eye_button.config(text="👁 Show")
    check_password()


def copy_password():
    password = password_entry.get()
    
    if password:
        pyperclip.copy(password)
        status.config(text="✔ Password copied to clipboard!")
        root.after(2000, lambda: status.config(text="Ready"))
    else:
        messagebox.showwarning("Empty", "Generate or enter a password first")


def clear():
    password_entry.delete(0, "end")
    password_visible = False
    password_entry.config(show="●")
    eye_button.config(text="👁 Show")
    
    output.config(state="normal")
    output.delete("1.0", "end")
    output.config(state="disabled")
    
    progress["value"] = 0
    strength_label.config(text="—")
    status.config(text="Ready")


# ============= MAIN WINDOW SETUP =============
root = tk.Tk()
root.title("🔐 Cyber Password Strength Checker")
root.geometry("900x750")
root.resizable(False, False)
root.configure(bg=DARK_BG)

# Styling
style = ttk.Style()
style.theme_use("clam")

# Configure progress bar styles
style.configure("Danger.Horizontal.TProgressbar", background=DANGER_RED, troughcolor=INPUT_BG, lightcolor=DANGER_RED, darkcolor=DANGER_RED, thickness=12, borderwidth=0)
style.configure("Warning.Horizontal.TProgressbar", background=WARNING_ORANGE, troughcolor=INPUT_BG, lightcolor=WARNING_ORANGE, darkcolor=WARNING_ORANGE, thickness=12, borderwidth=0)
style.configure("Info.Horizontal.TProgressbar", background="#fbbf24", troughcolor=INPUT_BG, lightcolor="#fbbf24", darkcolor="#fbbf24", thickness=12, borderwidth=0)
style.configure("Success.Horizontal.TProgressbar", background=SUCCESS_GREEN, troughcolor=INPUT_BG, lightcolor=SUCCESS_GREEN, darkcolor=SUCCESS_GREEN, thickness=12, borderwidth=0)
style.configure("Excellent.Horizontal.TProgressbar", background=ACCENT_CYAN, troughcolor=INPUT_BG, lightcolor=ACCENT_CYAN, darkcolor=ACCENT_CYAN, thickness=12, borderwidth=0)


# ============= HEADER SECTION =============
header_frame = tk.Frame(root, bg=DARK_BG, height=80)
header_frame.pack(fill="x", padx=0, pady=0)
header_frame.pack_propagate(False)

logo_label = tk.Label(
    header_frame,
    text="🔐",
    font=("Segoe UI", 48, "bold"),
    bg=DARK_BG,
    fg=ACCENT_CYAN
)
logo_label.pack(pady=(15, 5))

title_label = tk.Label(
    header_frame,
    text="Password Security Checker",
    font=("Segoe UI", 28, "bold"),
    bg=DARK_BG,
    fg=TEXT_PRIMARY
)
title_label.pack()

subtitle_label = tk.Label(
    header_frame,
    text="Generate & Analyze Strong Passwords",
    font=("Segoe UI", 11),
    bg=DARK_BG,
    fg=TEXT_SECONDARY
)
subtitle_label.pack()


# ============= MAIN CARD CONTAINER =============
main_container = tk.Frame(root, bg=DARK_BG)
main_container.pack(expand=True, fill="both", padx=30, pady=20)

# Glassmorphic card
card = tk.Frame(
    main_container,
    bg=CARD_BG,
    relief="flat",
    bd=0,
    highlightthickness=2,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT_CYAN
)
card.pack(expand=True, fill="both", padx=0, pady=0)

# Add internal padding
card_content = tk.Frame(card, bg=CARD_BG)
card_content.pack(fill="both", expand=True, padx=30, pady=30)


# ============= PASSWORD INPUT SECTION =============
input_label = tk.Label(
    card_content,
    text="Password",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_SECONDARY
)
input_label.pack(anchor="w", pady=(0, 8))

# Input container with buttons
input_frame = tk.Frame(card_content, bg=CARD_BG)
input_frame.pack(fill="x", pady=(0, 15))

password_entry = tk.Entry(
    input_frame,
    show="●",
    font=("Segoe UI", 13),
    bg=INPUT_BG,
    fg=TEXT_PRIMARY,
    insertbackground=ACCENT_CYAN,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT_CYAN
)
password_entry.pack(side="left", fill="both", expand=True, padx=(0, 8), ipady=10)

eye_button = tk.Button(
    input_frame,
    text="👁 Show",
    command=toggle_password_visibility,
    font=("Segoe UI", 10, "bold"),
    bg=INPUT_BG,
    fg=ACCENT_CYAN,
    activebackground="#1a1f3a",
    activeforeground=ACCENT_CYAN,
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=10
)
eye_button.pack(side="left")
eye_button.bind("<Enter>", on_button_enter)
eye_button.bind("<Leave>", on_button_leave)

# Bind real-time checking
password_entry.bind("<KeyRelease>", lambda e: check_password())


# ============= ACTION BUTTONS =============
buttons_label = tk.Label(
    card_content,
    text="Actions",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_SECONDARY
)
buttons_label.pack(anchor="w", pady=(15, 10))

button_frame = tk.Frame(card_content, bg=CARD_BG)
button_frame.pack(fill="x", pady=(0, 20))

def create_modern_button(parent, text, command, bg_color, fg_color=TEXT_PRIMARY, icon=""):
    """Create a modern styled button"""
    btn = tk.Button(
        parent,
        text=f"{icon} {text}",
        command=command,
        font=("Segoe UI", 11, "bold"),
        bg=bg_color,
        fg=fg_color,
        activebackground=bg_color,
        activeforeground=fg_color,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=12
    )
    btn.pack(side="left", padx=5, fill="both", expand=True)
    btn.bind("<Enter>", on_button_enter)
    btn.bind("<Leave>", on_button_leave)
    return btn


create_modern_button(button_frame, "Check", check_password, ACCENT_BLUE, TEXT_PRIMARY, "🔍")
create_modern_button(button_frame, "Generate", generate_password, SUCCESS_GREEN, TEXT_PRIMARY, "⚡")
create_modern_button(button_frame, "Copy", copy_password, ACCENT_PURPLE, TEXT_PRIMARY, "📋")
create_modern_button(button_frame, "Clear", clear, DANGER_RED, TEXT_PRIMARY, "🗑")


# ============= STRENGTH METER =============
meter_label = tk.Label(
    card_content,
    text="Password Strength",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_SECONDARY
)
meter_label.pack(anchor="w", pady=(15, 10))

meter_frame = tk.Frame(card_content, bg=CARD_BG)
meter_frame.pack(fill="x", pady=(0, 15))

progress = ttk.Progressbar(
    meter_frame,
    length=500,
    mode="determinate",
    value=0
)
progress.pack(fill="x", pady=(0, 8))

strength_label = tk.Label(
    meter_frame,
    text="—",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_BG,
    fg=ACCENT_CYAN
)
strength_label.pack(anchor="w")


# ============= OUTPUT SECTION =============
output_label = tk.Label(
    card_content,
    text="Analysis Result",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_SECONDARY
)
output_label.pack(anchor="w", pady=(15, 10))

output = tk.Text(
    card_content,
    height=10,
    width=70,
    font=("Consolas", 10),
    bg=INPUT_BG,
    fg=ACCENT_CYAN,
    insertbackground=ACCENT_CYAN,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT_CYAN,
    state="disabled",
    wrap="word"
)
output.pack(fill="both", expand=True, pady=(0, 20))


# ============= STATUS BAR =============
status_bar = tk.Frame(root, bg=BORDER_COLOR, height=40)
status_bar.pack(fill="x", side="bottom")
status_bar.pack_propagate(False)

status = tk.Label(
    status_bar,
    text="Ready",
    font=("Segoe UI", 10),
    bg=BORDER_COLOR,
    fg=ACCENT_CYAN,
    anchor="w",
    padx=30
)
status.pack(fill="both", expand=True)


# ============= START APP =============
root.mainloop()