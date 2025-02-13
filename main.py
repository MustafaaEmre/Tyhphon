from tkinter import *
from tkinter import messagebox
import base64

window = Tk()
window.title("Secret Notes")
window.config(padx=50,pady=50)


#functions

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def save_notes():
    title = user_title.get()
    message = user_secret.get("1.0",END)
    master_key = master_key_entry.get()


    if len(title) == 0 or len(message) == 0 or len(master_key) == 0:
        messagebox.showinfo(title="Error", message="Please enter all info")
    else:
        #encryption
        message_ecrypted = encode(master_key,message)

        try:
            with open("mysecretnotes.txt","a") as data_file:
                data_file.write(f"\n{title}\n{message_ecrypted}")
        except:
            with open("mysecretnotes.txt","w") as data_file:
                data_file.write(f"\n{title}\n{message_ecrypted}")
        finally:
            user_title.delete(0,END)
            user_secret.delete("1.0",END)
            master_key_entry.delete(0,END)

def decrypt_notes():
    message_encrypted = user_secret.get("1.0",END)
    master_secret = master_key_entry.get()

    if len(message_encrypted) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Error",message="Please enter all info")
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)
            user_secret.delete("1.0", END)
            user_secret.insert("1.0", decrypted_message)
        except:
            messagebox.showinfo(title="Error",message="Please enter encrypted info")


#ui

photo = PhotoImage(file="images.png")
photo_label = Label(image=photo)
photo_label.pack()

title_label = Label(text="Enter your title")
title_label.pack()

user_title = Entry(width=20)
user_title.pack()

secret_label = Label(text="Enter your secret")
secret_label.pack()

user_secret = Text(width=20,height=10)
user_secret.pack()

master_key_label = Label(text="Enter master key")
master_key_label.pack()

master_key_entry = Entry(width=20)
master_key_entry.pack()

save_encrypt_button = Button(text="Save & Encrypt",command=save_notes)
save_encrypt_button.pack()

decrypt_button = Button(text="Decrypt",command=decrypt_notes)
decrypt_button.pack()


window.mainloop()
