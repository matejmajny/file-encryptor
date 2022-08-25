from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
filename=''
keyname =''


def encrypt(directory):
    print(directory)
    splitted = directory.split(f"/")[-1]
    key = Fernet.generate_key()
    ch = "/"
    cd_dir = ''.join(directory.rpartition(ch)[:2])
    os.chdir(cd_dir)

    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)

    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
 
    fernet = Fernet(key)

    with open(splitted, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(splitted, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)



def decrypt(directory, decrypt_key):
    key_dir = ''.join(decrypt_key.rpartition("/")[:2])
    os.chdir(key_dir)
    key_name = decrypt_key.split(f"/")[-1]


    with open(key_name, 'rb') as filekey:
        key = filekey.read()

    # Decrypt shit (idk what im doing)

    splitted = directory.split(f"/")[-1]
    cd_dir = ''.join(directory.rpartition("/")[:2])
    os.chdir(cd_dir)
    
    fernet = Fernet(key)

    with open(splitted, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(splitted, 'wb') as dec_file:
        dec_file.write(decrypted)



def select_file():
    dir = "C:\\Users" if os.name == "nt" else "/home"
    global filename

    filetypes = (
        ('All files', '*.*'),
        ('Text files (.txt)', '*.txt')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=dir,
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
    
def select_key():
    dir = "C:\\Users" if os.name == "nt" else "/home"
    global keyname

    filetypes = (
        ('Key files (.key)', '*.key'),
        ('All files', '*.*')
    )

    keyname = fd.askopenfilename(
        title='Open a decrypt key',
        initialdir=dir,
        filetypes=filetypes)

    showinfo(
        title='Selected Key',
        message=keyname
    )


# GUI code

def StartButton():
    selection = value_inside.get()

    if selection == "Encrypt":
        if filename == "":
            showinfo(
                title='Error!',
                message="Choose file what you want encrypt!"
            )
        else:
            encrypt(filename)
            showinfo(
                title='Succesful!',
                message="Succesfully encrypted the file!"
            )

        
    elif selection == "Decrypt":
        print(keyname)
        print(filename)
        if filename == "" or keyname == "":
            showinfo(
            title='Error!',
            message="Choose key or/and file for decryption!"
            )
        else: 
            try:
                decrypt(filename, keyname)
            except:
                showinfo(
                title='Error!',
                message="Most likely you entered wrong key or file what is:\n\n-encrypted with another algorithm\n-not encrypted"
            )
            else:
                showinfo(
                    title='Succesful!',
                    message="Succesfully decrypted the file!"
                )
    else:
        showinfo(
        title='Error!',
        message="Choose if you want decrypt or encrypt!"
    )

        

root = tk.Tk()
root.title("File en/decrypter")
canvas1 = tk.Canvas(root, width=300, height=300)
canvas1.pack()

# Selection menu

options = ["Encrypt", "Decrypt", "Select mode"]
value_inside = tk.StringVar(root)
value_inside.set(options[2])
variable = tk.StringVar()
option_menu = tk.OptionMenu(root, value_inside, *options)
option_menu.config(bg="orange", fg="black", width=30)
canvas1.create_window(150, 235, window=option_menu)

# Start buttons

button1 = tk.Button(root, text="Start! ", command=StartButton, width=30, fg="white", bg="green")
canvas1.create_window(150, 200, window=button1)

button2 = tk.Button(root, text="Select the file", command=select_file, width=15, fg="white", bg="blue")
canvas1.create_window(80, 150, window=button2)

button2 = tk.Button(root, text="Select the key", command=select_key, width=15, fg="white", bg="blue")
canvas1.create_window(230, 150, window=button2)

# Text

label2 = tk.Label(root, text="File En/Decrypter")
label2.config(font=("helvetica", 20))
canvas1.create_window(150, 50, window=label2)

root.mainloop()