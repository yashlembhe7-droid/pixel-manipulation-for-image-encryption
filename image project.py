import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


# ---------------- WINDOW ----------------

window = tk.Tk()
window.geometry("1400x900")
window.title("Image Encryption & Decryption")
window.configure(bg="#0a0e27")


# ---------------- COLORS ----------------

BG = "#0a0e27"
CARD = "#141821"
BLUE = "#1a2332"
CYAN = "#00d9ff"
GREEN = "#00ff00"
ORANGE = "#ff8000"
YELLOW = "#ffff00"
RED = "#ff0055"
WHITE = "#ffffff"


# ---------------- VARIABLES ----------------

image_path = None
original_image = None
encrypted_image = None

panelA = None
panelB = None
status_label = None



# ---------------- STATUS ----------------

def update_status(text):
    status_label.config(text=text)



# ---------------- OPEN IMAGE ----------------

def open_img():

    global image_path, original_image

    file = filedialog.askopenfilename(
        filetypes=[
            ("Image Files","*.jpg *.png *.jpeg")
        ]
    )

    if file:

        image_path = file

        original_image = cv2.imread(file)

        show_image(original_image,panelA)

        show_image(original_image,panelB)

        update_status("Image loaded successfully")



# ---------------- SHOW IMAGE ----------------

def show_image(img, panel):

    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    img = Image.fromarray(img)

    img.thumbnail((450,350))

    img = ImageTk.PhotoImage(img)

    panel.config(image=img)
    panel.image = img



# ---------------- ENCRYPT ----------------

def encrypt():

    global encrypted_image

    if original_image is None:

        messagebox.showwarning(
            "Warning",
            "Select image first"
        )
        return


    encrypted_image = cv2.bitwise_xor(
        original_image,
        255
    )


    show_image(
        encrypted_image,
        panelB
    )


    update_status("Image encrypted")



# ---------------- DECRYPT ----------------

def decrypt():

    global encrypted_image


    if encrypted_image is None:

        messagebox.showwarning(
            "Warning",
            "Encrypt image first"
        )

        return


    decrypted = cv2.bitwise_xor(
        encrypted_image,
        255
    )


    show_image(
        decrypted,
        panelB
    )


    update_status("Image decrypted")



# ---------------- SAVE ----------------

def save_image():

    if encrypted_image is None:

        messagebox.showwarning(
            "Warning",
            "Nothing to save"
        )

        return


    file = filedialog.asksaveasfilename(
        defaultextension=".png"
    )


    if file:

        cv2.imwrite(
            file,
            encrypted_image
        )

        update_status("Image saved")



# ---------------- RESET ----------------

def reset():

    if original_image is not None:

        show_image(
            original_image,
            panelB
        )

        update_status(
            "Reset complete"
        )



# ---------------- UI ----------------


header = tk.Frame(
    window,
    bg=BLUE,
    height=120
)

header.pack(fill="x")


tk.Label(
    header,
    text="🔐 Image Encryption & Decryption",
    font=("Segoe UI",32,"bold"),
    fg=CYAN,
    bg=BLUE
).pack(pady=15)



# IMAGE AREA

content = tk.Frame(
    window,
    bg=BG
)

content.pack(
    expand=True,
    fill="both",
    padx=30,
    pady=20
)



left = tk.Frame(
    content,
    bg=CARD,
    bd=2,
    relief="ridge"
)

left.pack(
    side="left",
    expand=True,
    fill="both",
    padx=20
)


right = tk.Frame(
    content,
    bg=CARD,
    bd=2,
    relief="ridge"
)

right.pack(
    side="right",
    expand=True,
    fill="both",
    padx=20
)



tk.Label(
    left,
    text="Original Image",
    font=("Segoe UI",18,"bold"),
    bg=CARD,
    fg=CYAN
).pack()



panelA = tk.Label(
    left,
    bg=CARD
)

panelA.pack(
    expand=True
)




tk.Label(
    right,
    text="Encrypted / Decrypted",
    font=("Segoe UI",18,"bold"),
    bg=CARD,
    fg=ORANGE
).pack()



panelB = tk.Label(
    right,
    bg=CARD
)

panelB.pack(
    expand=True
)



# BUTTONS


buttons = tk.Frame(
    window,
    bg=BLUE,
    height=80
)

buttons.pack(
    fill="x"
)



def btn(text,cmd,color):

    tk.Button(
        buttons,
        text=text,
        command=cmd,
        font=("Segoe UI",13,"bold"),
        bg=color,
        fg="black",
        padx=20,
        pady=10
    ).pack(
        side="left",
        padx=20,
        pady=15
    )



btn("📂 Select",open_img,CYAN)
btn("🔐 Encrypt",encrypt,GREEN)
btn("🔓 Decrypt",decrypt,ORANGE)
btn("↺ Reset",reset,YELLOW)
btn("💾 Save",save_image,CYAN)
btn("❌ Exit",window.destroy,RED)



# STATUS


status_label = tk.Label(
    window,
    text="Ready",
    bg=CARD,
    fg=GREEN,
    font=("Segoe UI",12)
)

status_label.pack(
    fill="x"
)



window.mainloop()