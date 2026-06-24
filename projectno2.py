import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np


# Create main window
window = Tk()
window.geometry("1400x900")
window.title("Image Encryption & Decryption")
window.resizable(True, True)

# Define color scheme - Dark cybersecurity theme
COLOR_BG = "#0a0e27"
COLOR_DARK_BLUE = "#1a2332"
COLOR_CARD = "#141821"
COLOR_NEON_CYAN = "#00d9ff"
COLOR_NEON_GREEN = "#00ff00"
COLOR_NEON_ORANGE = "#ff8000"
COLOR_NEON_YELLOW = "#ffff00"
COLOR_NEON_RED = "#ff0055"
COLOR_TEXT = "#ffffff"
COLOR_TEXT_SECONDARY = "#a0a0a0"

# Configure main window
window.configure(bg=COLOR_BG)

# Configure TTK style
style = ttk.Style()
style.theme_use('clam')
style.configure('Dark.TFrame', background=COLOR_BG, relief='flat')
style.configure('Card.TFrame', background=COLOR_CARD, relief='flat', borderwidth=2)
style.configure('Dark.TLabel', background=COLOR_BG, foreground=COLOR_TEXT, font=('Segoe UI', 10))


image_path = None
original_image = None
encrypted_image = None
key = None
panelA = None
panelB = None
status_label = None


def openfilename():
    return filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )


def open_img():

    global image_path, original_image, panelA, panelB

    image_path = openfilename()

    if image_path:

        img = Image.open(image_path)
        original_image = img

        img = img.resize((350,350))
        img_tk = ImageTk.PhotoImage(img)


        if panelA is None:

            panelA = tk.Label(frame_left_card, image=img_tk, bg=COLOR_CARD)
            panelA.image = img_tk
            panelA.grid(row=0, column=0, padx=10, pady=10)


            panelB = tk.Label(frame_right_card, image=img_tk, bg=COLOR_CARD)
            panelB.image = img_tk
            panelB.grid(row=0, column=0, padx=10, pady=10)

        else:

            panelA.configure(image=img_tk)
            panelA.image = img_tk

            panelB.configure(image=img_tk)
            panelB.image = img_tk

        update_status("✓ Image loaded successfully")

    else:
        messagebox.showwarning("Warning","No image selected")


# ---------------- Encryption -----------------

def encrypt():

    global encrypted_image,key


    if image_path is None:
        messagebox.showwarning("Warning","Select image first")
        return


    img = cv2.imread(image_path,0)


    img = img.astype(float)/255


    h,w = img.shape


    key = np.random.rand(h,w)+0.1


    encrypted_image = img/key



    encrypted_save = np.uint8(
        np.clip(encrypted_image*255,0,255)
    )


    cv2.imwrite(
        "encrypted.jpg",
        encrypted_save
    )


    show = Image.open("encrypted.jpg")
    show = show.resize((350,350))
    show = ImageTk.PhotoImage(show)

    panelB.configure(image=show)
    panelB.image = show

    update_status("🔒 Image encrypted successfully")

    messagebox.showinfo(
        "Success",
        "Image Encrypted"
    )



# ---------------- Decryption -----------------


def decrypt():

    global encrypted_image,key


    if encrypted_image is None:

        messagebox.showwarning(
            "Warning",
            "Encrypt image first"
        )
        return



    output = encrypted_image * key


    output = np.uint8(
        np.clip(output*255,0,255)
    )


    cv2.imwrite(
        "decrypted.jpg",
        output
    )


    img = Image.open("decrypted.jpg")
    img = img.resize((350,350))

    img = ImageTk.PhotoImage(img)


    panelB.configure(image=img)
    panelB.image = img

    update_status("🔓 Image decrypted successfully")

    messagebox.showinfo(
        "Success",
        "Image Decrypted"
    )



# ---------------- Save -----------------


def save_image():

    file = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[
            ("JPEG","*.jpg")
        ]
    )


    if file:

        img = cv2.imread("decrypted.jpg")
        cv2.imwrite(file,img)

        update_status(f"💾 Image saved to {file}")

        messagebox.showinfo(
            "Saved",
            "Image saved successfully"
        )



# ---------------- Reset -----------------


def reset():

    global original_image


    if original_image:

        img = original_image.resize((350,350))

        img = ImageTk.PhotoImage(img)

        panelB.configure(image=img)
        panelB.image = img

        update_status("↺ Image reset to original")

    else:

        messagebox.showwarning(
            "Warning",
            "No image"
        )



# ============= STATUS BAR FUNCTION =============
def update_status(message):
    global status_label
    status_label.config(text=message)


# ============= BUTTON HOVER EFFECTS =============
def on_button_enter(btn, color):
    btn.config(bg=color, relief="sunken")

def on_button_leave(btn, color):
    btn.config(bg=color, relief="raised")


# ============= UI LAYOUT WITH GRID =============

# Main frame with grid geometry
main_frame = ttk.Frame(window, style='Dark.TFrame')
main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=0)
main_frame.rowconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=0)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# ============= HEADER SECTION =============
header_frame = tk.Frame(main_frame, bg=COLOR_DARK_BLUE, height=100)
header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
header_frame.grid_propagate(False)

# Title
title_label = tk.Label(
    header_frame,
    text="🔐 Image Encryption & Decryption",
    font=("Segoe UI", 32, "bold"),
    fg=COLOR_NEON_CYAN,
    bg=COLOR_DARK_BLUE
)
title_label.grid(row=0, column=0, padx=20, pady=15)

# Subtitle
subtitle_label = tk.Label(
    header_frame,
    text="Secure Image Protection Tool",
    font=("Segoe UI", 12),
    fg=COLOR_TEXT_SECONDARY,
    bg=COLOR_DARK_BLUE
)
subtitle_label.grid(row=1, column=0, padx=20, pady=0)

# ============= CONTENT SECTION =============
content_frame = ttk.Frame(main_frame, style='Dark.TFrame')
content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)
content_frame.rowconfigure(0, weight=1)

# LEFT CARD - Original Image
left_card_frame = tk.Frame(content_frame, bg=COLOR_DARK_BLUE, bd=2, relief="solid")
left_card_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=0)

left_title = tk.Label(
    left_card_frame,
    text="📷 Original Image",
    font=("Segoe UI", 14, "bold"),
    fg=COLOR_NEON_CYAN,
    bg=COLOR_DARK_BLUE
)
left_title.pack(pady=10, padx=10)

frame_left_card = tk.Frame(left_card_frame, bg=COLOR_CARD, bd=1, relief="solid")
frame_left_card.pack(padx=10, pady=10)

# RIGHT CARD - Encrypted/Decrypted Image
right_card_frame = tk.Frame(content_frame, bg=COLOR_DARK_BLUE, bd=2, relief="solid")
right_card_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=0)

right_title = tk.Label(
    right_card_frame,
    text="🔒 Encrypted/Decrypted Image",
    font=("Segoe UI", 14, "bold"),
    fg=COLOR_NEON_ORANGE,
    bg=COLOR_DARK_BLUE
)
right_title.pack(pady=10, padx=10)

frame_right_card = tk.Frame(right_card_frame, bg=COLOR_CARD, bd=1, relief="solid")
frame_right_card.pack(padx=10, pady=10)

# ============= BUTTONS SECTION =============
button_frame = tk.Frame(main_frame, bg=COLOR_DARK_BLUE, height=90)
button_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
button_frame.grid_propagate(False)

# Button styling function
def create_modern_button(parent, text, command, emoji, bg_color, row, col):
    btn = tk.Button(
        parent,
        text=f"{emoji} {text}",
        command=command,
        font=("Segoe UI", 11, "bold"),
        bg=bg_color,
        fg="#000000" if bg_color in [COLOR_NEON_YELLOW] else "#ffffff",
        bd=0,
        relief="raised",
        padx=15,
        pady=12,
        cursor="hand2",
        activebackground=bg_color,
        activeforeground="#000000" if bg_color in [COLOR_NEON_YELLOW] else "#ffffff"
    )
    btn.grid(row=row, column=col, padx=8, pady=5)
    
    # Hover effects
    btn.bind("<Enter>", lambda e: on_button_enter(btn, bg_color))
    btn.bind("<Leave>", lambda e: on_button_leave(btn, bg_color))
    
    return btn

# Create buttons
btn_select = create_modern_button(button_frame, "Select Image", open_img, "📂", COLOR_NEON_CYAN, 0, 0)
btn_encrypt = create_modern_button(button_frame, "Encrypt", encrypt, "🔐", COLOR_NEON_GREEN, 0, 1)
btn_decrypt = create_modern_button(button_frame, "Decrypt", decrypt, "🔓", COLOR_NEON_ORANGE, 0, 2)
btn_reset = create_modern_button(button_frame, "Reset", reset, "↺", COLOR_NEON_YELLOW, 0, 3)
btn_save = create_modern_button(button_frame, "Save Image", save_image, "💾", COLOR_NEON_CYAN, 0, 4)
btn_exit = create_modern_button(button_frame, "Exit", window.destroy, "❌", COLOR_NEON_RED, 0, 5)

# ============= STATUS BAR =============
status_frame = tk.Frame(main_frame, bg=COLOR_CARD, height=40, bd=1, relief="sunken")
status_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
status_frame.grid_propagate(False)

status_label = tk.Label(
    status_frame,
    text="Ready",
    font=("Segoe UI", 10),
    fg=COLOR_NEON_GREEN,
    bg=COLOR_CARD
)
status_label.pack(side="left", padx=15, pady=8)


window.mainloop()