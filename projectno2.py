import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


window = Tk()
window.geometry("1000x700")
window.title("Image Encryption Decryption")


image_path = None
original_image = None
encrypted_image = None
key = None
panelA = None
panelB = None


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

            panelA = Label(window,image=img_tk)
            panelA.image = img_tk
            panelA.place(x=50,y=300)


            panelB = Label(window,image=img_tk)
            panelB.image = img_tk
            panelB.place(x=600,y=300)

        else:

            panelA.configure(image=img_tk)
            panelA.image = img_tk

            panelB.configure(image=img_tk)
            panelB.image = img_tk


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

    else:

        messagebox.showwarning(
            "Warning",
            "No image"
        )



# ---------------- UI -----------------


Label(
    window,
    text="Image Encryption\nDecryption",
    font=("Arial",40),
    fg="magenta"
).place(x=330,y=20)


Button(
    window,
    text="Choose",
    command=open_img,
    font=("Arial",20),
    bg="orange"
).place(x=50,y=120)


Button(
    window,
    text="Encrypt",
    command=encrypt,
    font=("Arial",20),
    bg="lightgreen"
).place(x=150,y=620)



Button(
    window,
    text="Decrypt",
    command=decrypt,
    font=("Arial",20),
    bg="orange"
).place(x=450,y=620)



Button(
    window,
    text="Reset",
    command=reset,
    font=("Arial",20),
    bg="yellow"
).place(x=750,y=620)



Button(
    window,
    text="Save",
    command=save_image,
    font=("Arial",20),
    bg="cyan"
).place(x=850,y=120)



Button(
    window,
    text="EXIT",
    command=window.destroy,
    font=("Arial",20),
    bg="red"
).place(x=880,y=20)



window.mainloop()