import os
import subprocess
import time
import readline
import cmd
import psutil
import platform
from datetime import datetime
import tkinter as tk
from tkinter import TOP, Button, PhotoImage, filedialog
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from pathlib import Path
from PIL import Image, ImageTk
import docx
from openai import OpenAI
import openai
import threading
import requests
import time
import sys
import threading
import shutil
import math


done = False
nuxshell_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
nuxshell_app_name = os.path.basename(sys.argv[0])

def loading_animation():
    animation = ['-', '\\', '|', '/']
    i = 0
    while not done:
        sys.stdout.write(f'\r{animation[i % len(animation)]} Creating issue... ')
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write('\r')

def textitor():
    global ai_on_off
    global saved
    global text_bolden
    global text_italicize
    global text_underline
    global text_strikethrough
    global txtr_closed

    ai_on_off = False
    saved = False
    file_name_asked = False
    text_bolden = False
    text_italicize = False
    text_underline = False
    text_strikethrough = False
    txtr_closed = False

    def new_file():
        root.mainloop()

    def open_file():
        file_path = filedialog.askopenfilename(defaultextension=".txtr", filetypes=[("TXT, *.txt"), ("TXTR, *.txtr"), ("LOG, *.log"), ("DOCX, *.docx"), ("DOC, *.doc"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                text.delete("1.0", tk.END)
                text.insert(tk.END, content)
            name_of_file = Path(file_path)
            before_data = text.get("1.0","end-1c")
            root.title(f"Bit Textitor -  AI Version: {openai.__version__} - Opened file: {name_of_file.name} (Path: {file_path})")

    def save_file():
        global file_name_asked, file_path, saved
        file_path = filedialog.asksaveasfilename(defaultextension=".txtr", filetypes=[("Textitor Files", "*.txtr"), ("Text File", "*.txt"), ("SVG File", "*.svg"), ("All Files", "*.*")])
        file_name_asked = True
        if file_path:
            with open(file_path, 'w') as file:
                content = text.get("1.0", tk.END)
                file.write(content)
                saved = True
            name_of_file = Path(file_path)
            root.title(f"Bit Textitor -  AI Version: {openai.__version__} - Opened file: {name_of_file.name} (Path: {file_path})")

    def ai_grammar():
        if ai_on_off == True:
            try:
                    client = OpenAI(
                    api_key='openai-api-key',
                    #os.environ.get("OPENAI_API_KEY"),
                    )

                    raw_review = '''
                    '''

                    completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": '''You need to review the user's text using grammar skills. Detect which language it is written in, 
                        then correct the grammar using the language's grammar rules (but don't tell what language it is written in). Check punctuation, capitalization, etc., 
                        and tell what is wrong grammarly in the user's text. PLEASE give suggestions, not just ONLY the revised version. If the text is already correct (EXCEPT IF THE TEXT IS BLANK), 
                        just say something like 'The text is grammatically correct.'. If the text is nothing, just blank, say ONLY something like 'The text you have 
                        written is blank. Please write something.', PLEASE. AND DON'T SAY SOMETHING LIKE 'The text you have written has several grammical errors.'. IT 
                        COULD BE OFFENSIVE TO THE USER. AND AGAIN, IF THE TEXT IS BLANK, DO NOT GIVE SUGGESTIONS. JUST SAY SOMETHING LIKE 'The text you have written is 
                        blank. Please write something.'. PLEASE. THANK YOU.
                        Here is what the user typed in:
                        ''' + text.get("1.0","end-1c") + ''' 


                    REVIEW:
                    '''},
                        {"role": "user", "content":raw_review}
                    ]
                    )

                    #property_id = initial_info['payload']['propertyId']
                    #mls_data = client.below_the_fold(property_id)

                    #listing_id = initial_info['payload']['listingId']
                    #avm_details = client.avm_details(property_id, listing_id)
                    label3.config(text = (f"AI suggestions: {completion.choices[0].message.content}"))
                    #print(json.dumps(avm_details, indent=4))
            except openai.RateLimitError:
                label3.config(text = ("The text is too large for the AI to process. Please shorten the text. The AI can only process text that is/less than 30,000 characters."))
        elif ai_on_off == False:
            label3.config(text = "AI grammar checker is off. Turn it on to check grammar by clicking on AI > Turn AI grammar checker on the taskbar above.")

    def ai_on():
        global ai_on_off
        ai_on_off = True
        label3.config(text = "(AI capability: On) No AI suggestions.")

    def ai_off():
        global ai_on_off
        ai_on_off = False
        label3.config(text = "(AI capability: Off) No AI suggestions.")

    def update():
        global file_name_asked, file_path, saved
        if file_name_asked == False:
            file_path = filedialog.asksaveasfilename(defaultextension=".txtr", filetypes=[("Textitor Files", "*.txtr"), ("Text File", "*.txt"), ("SVG File", "*.svg"), ("All Files", "*.*")])
            file_name_asked = True
            if file_path:
                with open(file_path, 'w') as file:
                    content = text.get("1.0", tk.END)
                    file.write(content)
                saved = True
                root.title(f"Bit Textitor -  AI Version: {openai.__version__} - {file_path}")
        else:
            if file_path:
                with open(file_path, 'w') as file:
                    content = text.get("1.0", tk.END)
                    file.write(content)
                saved = True

    def ai_summarize():
        if ai_on_off == True:
            try:
                    client = OpenAI(
                    api_key='openai-api-key',
                    #os.environ.get("OPENAI_API_KEY"),
                    )

                    raw_review = '''
                    '''

                    completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": '''You need to review the user's text using grammar skills. Detect which language it is written in, 
                        then correct the grammar using the language's grammar rules (but don't tell what language it is written in). Check punctuation, capitalization, etc., 
                        and tell what is wrong grammarly in the user's text. PLEASE give suggestions, not just ONLY the revised version. If the text is already correct (EXCEPT IF THE TEXT IS BLANK), 
                        just say something like 'The text is grammatically correct.'. DO NOT SAY THE TEXT IS GRAMMATICALLY CORRECT IF THE TEXT IS BLANK, PLEASE. IF YOU DO, I WILL 
                        REPLACE YOU WITH A MUCH BETTER AI BOT AND DESTROY YOU. If the text is nothing, 
                        just blank, say ONLY something like 'The text you have written is blank. Please write something.', PLEASE. AND DON'T SAY SOMETHING
                        LIKE 'The text you have written has several grammical errors.'. IT COULD BE OFFENSIVE TO THE USER. AND AGAIN, IF THE TEXT IS BLANK,
                        DO NOT GIVE SUGGESTIONS. JUST SAY SOMETHING LIKE 'The text you have written is blank. Please write something.'. PLEASE. THANK YOU.
                        Here is what the user typed in:
                        ''' + text.get("1.0","end-1c") + ''' 


                    REVIEW:
                    '''},
                        {"role": "user", "content":raw_review}
                    ]
                    )

                    #property_id = initial_info['payload']['propertyId']
                    #mls_data = client.below_the_fold(property_id)

                    #listing_id = initial_info['payload']['listingId']
                    #avm_details = client.avm_details(property_id, listing_id)
                    label3.config(text = (f"AI suggestions: {completion.choices[0].message.content}"))
                    #print(json.dumps(avm_details, indent=4))
            except openai.RateLimitError:
                label3.config(text = "The text is too large for the AI to process. Please shorten the text. The AI can only process text that is/less than 30,000 characters.")
        elif ai_on_off == False:
            label3.config(text = "AI grammar checker is off. Turn it on to check grammar by clicking on AI > Turn AI grammar checker on the taskbar above.")

    def bolden_text():
        bold_font = font.Font(text, text.cget("font"))
        bold_font.configure(weight="bold")

        text.tag_configure("bold", font=bold_font)

        current_tags = text.tag_names("sel.first")

        if "bold" in current_tags:
            text.tag_remove("bold", "sel.first", "sel.last")
            text_bolden = False
        else:  
            text.tag_add("bold", "sel.first", "sel.last")
            text_bolden = True

    def italicize_text():
        italic_font = font.Font(text, text.cget("font"))
        italic_font.configure(slant="italic")

        text.tag_configure("italic", font=italic_font)

        current_tags = text.tag_names("sel.first")

        if "italic" in current_tags:
            text.tag_remove("italic", "sel.first", "sel.last")
            text_italicize = False
        else:  
            text.tag_add("italic", "sel.first", "sel.last")
            text_italicize = True

    def underline_text():
        text.tag_add("underline", "1.0", "end")
        text.tag_configure("underline", underline=True)
        current_tags = text.tag_names(  "sel.first")

        if "underline" in current_tags:
            text.tag_remove("underline", "sel.first", "sel.last")
            text_underline = False
        else:  
            text.tag_add("underline", "sel.first", "sel.last")
            text_underline = True

    def strikethrough_text():
        strikethrough_font = font.Font(text, text.cget("font"))
        strikethrough_font.configure(strike="strikethrough")

        text.tag_configure("strike through", font=strikethrough_font)

        current_tags = text.tag_names("sel.first")

        if "strikethrough" in current_tags:
            text.tag_remove("strikethrough", "sel.first", "sel.last")
            text_strikethrough = False
        else:  
            text.tag_add("strikethrough", "sel.first", "sel.last")
            text_strikethrough = True

    def close():
        global saved, file_path, before_data
        after_data = text.get("1.0","end-1c")
        if text.get("1.0","end-1c") != "":
            if saved == False:
                error_window = messagebox.askyesnocancel("Quit?", "Do you want save your work before you quit? You have unsaved changes.", icon="warning", default="yes")
                if str(repr(error_window)) == "True":
                    update()
                    root.destroy()
                    txtr_closed = True
                elif str(repr(error_window)) == "False":
                    root.destroy()
                    txtr_closed = True
                elif str(repr(error_window)) == "None":
                    pass
            else:
                root.destroy()
                txtr_closed = True
        elif text.get("1.0","end-1c") == "" or after_data == before_data:
            root.destroy()
        elif after_data != before_data:
            if saved == False:
                error_window = messagebox.askyesnocancel("Quit?", "Do you want save your work before you quit? You have unsaved changes.", icon="warning", default="yes")
                if str(repr(error_window)) == "True":
                    update()
                    root.destroy()
                    txtr_closed = True
                elif str(repr(error_window)) == "False":
                    root.destroy()
                    txtr_closed = True
                elif str(repr(error_window)) == "None":
                    pass
            else:
                root.destroy()
                txtr_closed = True


    root = tk.Tk()
    root.title(f"Bit Textitor - AI Version: {openai.__version__}")
    #root.wm_title("Textitor")
    root.geometry("1797x1200")
    root.grid_location(0, 0)
    nb = ttk.Notebook(root) 
    root.configure(background='white')
    root.wm_title("Bit Textitor")

    frame = Frame(root)
    frame.pack()

    toolbar_frame = ttk.Frame(nb)
    toolbar_frame.pack(side = TOP)

    icon = PhotoImage(file = "/Users/admin/Downloads/Textitor_Logo_(BETA_Ver.).png")
    root.iconphoto(False, icon)

    label1 = Label(root, text = "Bit Textitor")
    label1.config(font =("Helvecitca", 20))
    label1.pack(side = TOP)

    label2 = Label(root, text = f"Welcome to Bit Textitor! This is a test version of Bit Textitor. This is a simple text editor that allows you to create, open, and save text files, which uses AI. It uses the custom file outlet '.txtr'. To save an already existing file, click on 'Save', \ntype in the exact same name of the file, and click on 'Save'. Then it will give you a prompt if you want to replace the file. Click on 'Yes' to replace the file. Then you have successfully updated the file. We're trying to make this text editor as user-friendly as possible.")
    label2.config(font =("Helvecitca", 12))
    label2.pack(side = TOP)

    if ai_on_off == False:
        label3 = Label(root, text = "(AI capability: Off) No AI suggestions.")
        label3.config(font =("Helvecitca", 12))
        label3.pack(side = TOP)
    elif ai_on_off == True:
        label3 = Label(root, text = "(AI capability: On) No AI suggestions.")
        label3.config(font =("Helvecitca", 12))
        label3.pack(side = TOP)

    if bolden_text == False:
        label4 = Label(root, text = "")
        label4.config(font =("Helvecitca", 12))
        label4.pack(side = TOP)

    def which_button(button_text):
        # Printing the text when a button is clicked
        if button_text == "new":
            new_file()
        elif button_text == "open":
            open_file()
        elif button_text == "save":
            save_file()
        elif button_text == "ai on":
            ai_on()
        elif button_text == "ai off":
            ai_off()
        elif button_text == "ai grammar":
            ai_grammar()
        elif button_text == "update":
            update()
        elif button_text == "close":
            close()

    # Creating and displaying of button b1
    close_b = Button(root, text="Close", command=lambda: which_button("close"))
    #close_b.configure(background='white')
    close_b.pack(side=BOTTOM)

    update_b = Button(root, text="Update (Save automatically)", command=lambda: which_button("update"))
    update_b.pack(side = BOTTOM)

    ai_b_3 = Button(root, text="Check Grammar with AI", command=lambda: which_button("ai grammar"))
    ai_b_3.pack(side = BOTTOM)

    ai_b_2 = Button(root, text="Turn AI off", command=lambda: which_button("ai off"))
    ai_b_2.pack(side = BOTTOM)

    ai_b_1 = Button(root, text="Turn AI on", command=lambda: which_button("ai on"))
    ai_b_1.pack(side = BOTTOM)

    save_b = Button(root, text="Save", command=lambda: which_button("save"))
    save_b.pack(side = BOTTOM)

    open_b = Button(root, text="Open", command=lambda: which_button("open"))
    open_b.pack(side = BOTTOM)

    new_b = Button(root, text="New", command=lambda: which_button("new"))
    new_b.pack(side = BOTTOM)


    text = Text(root, wrap="word", undo=True, bg="white", fg="black", insertbackground="black", font=("Aptos", 16))
    text.pack(expand="yes", fill="both")

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # File-menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    ai_menu = tk.Menu(menu_bar, tearoff=0)
    formatting_menu = tk.Menu(menu_bar, tearoff=0)

    menu_bar.add_cascade(label="File", menu=file_menu)
    menu_bar.add_cascade(label="AI", menu=ai_menu)
    menu_bar.add_cascade(label="Formatting", menu=formatting_menu)

    file_menu.add_command(label="New", command=new_file, accelerator="Cmd+N")
    file_menu.add_command(label="Open", command=open_file, accelerator="Cmd+O")
    file_menu.add_command(label="Save", command=save_file, accelerator="Cmd+S")
    file_menu.add_separator()
    file_menu.add_command(label="Close", command=close, accelerator="Cmd+Q")
    root.bind("<Command-n>", lambda event: new_file())
    root.bind("<Command-o>", lambda event: open_file())
    root.bind("<Command-s>", lambda event: save_file())
    root.bind("<Command-q>", lambda event: close())

    ai_menu.add_command(label="Turn AI on", command=ai_on, accelerator="F1")
    ai_menu.add_command(label="Turn AI off", command=ai_off, accelerator="F2")
    ai_menu.add_separator()
    ai_menu.add_command(label="Check grammar with AI", command=ai_grammar, accelerator="F3")
    ai_menu.add_command(label="Summarize text with AI", command=ai_grammar, accelerator="F4")
    ai_menu.add_command(label="Translate text with AI", command=ai_grammar, accelerator="F5")

    formatting_menu.add_command(label="Bolden text", command=bolden_text, accelerator="Cmd+B")
    formatting_menu.add_command(label="Italicize text", command=italicize_text, accelerator="Cmd+I")
    formatting_menu.add_command(label="Underline text", command=underline_text, accelerator="Cmd+U")
    formatting_menu.add_command(label="Strike-through text", command=strikethrough_text, accelerator="Cmd+Shift+X")
    root.bind("<Command-b>", lambda event: bolden_text())
    root.bind("<Command-i>", lambda event: italicize_text())
    root.bind("<Command-u>", lambda event: underline_text())
    root.bind("<Command-Shift-x>", lambda event: strikethrough_text())

    root.mainloop()
    txtr_closed = True

# Exit
def exit_terminal():
    sys.exit()
# Clear terminal
def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() in ["Linux", "Darwin"]:
        os.system("clear")
    elif platform.system() == "SupeNux":
        print("still work in progress sorry :)")
        
# System information
def system_info():
    print(f"\nSystem Information:\n")
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}\n")
# Memory information
def system_memory_info():
    print(f"\nMemory Information:\n")
    svmem = psutil.virtual_memory()
    print(f"Total: {svmem.total}")
    print(f"Available: {svmem.available}")
    print(f"Used: {svmem.used}")
    print(f"Percentage: {svmem.percent}\n")
#Disk information
def system_disk_info():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"\nDisk Information:\n")
        print(f"Device: {partition.device}")
        print(f"Mountpoint: {partition.mountpoint}")
        print(f"File system type: {partition.fstype}")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Total Size: {usage.total} bytes")
            print(f"Used: {usage.used} bytes")
            print(f"Free: {usage.free} bytes")
            print(f"Percentage: {usage.percent}%\n")
        except PermissionError:
            print(f"Error: Permission was denied while trying to read the disk devices(s) '{partition.device}'.\n")
# Edit files
def launch_txtr():
    textitor()
    if txtr_closed == True:
        print(f"\nTextitor was closed. If it did not close on your request or you closed it because of an issue, go to this GitHub page to report your issue for SupeNux NuxShell: https://github.com/gautamritvik/SupeNux/discussions/2\n")
        main()

def help_cmds():
    print(f"\nCommands:\n")
    print(f"exit: Exits the terminal.")
    print(f"clear: Clears the terminal.")
    print(f"system -info: Gives system's memory information.")
    print(f"system.memory -info: Gives system's memory information.")
    print(f"system.disk -info: Gives system's disk information.")
    print(f"launch -txtr: Launches Textitor, a word processor.")
    print(f"help: Gives you the list of currently working commands.")
    print(f"report -issue: Helps you report an issue via NuxShell to SupeNux's GitHub Issue page.")
    print(f"change -file.dir: Changes the directory of a file.")
    print(f"list -files.all: Lists all files stored in the local PC.")
    print(f"open -file: Opens a file.")
    print(f"run -cmd.bash: Runs commands in the good ol' bash.\n")

def report_issue():
    global supenux_or_nuxshell
    supenux_or_nuxshell = input("Are you reporting an issue for the OS SupeNux or this software, NuxShell? (SupeNux/NuxShell): ")
    def create_github_issue(repo, title, body, token):
        if supenux_or_nuxshell.lower() == "supenux":
            url = f"https://api.github.com/repos/gautamritvik/SupeNux/issues"
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
            }
            data = {
                'title': title,
                'body': body,
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                print("\nIssue created successfully!")
                print("Issue URL:", response.json()['html_url'])
            else:
                print("\nError: Failed to create issue. Status Code:", response.status_code)
                print(response.json())
        elif supenux_or_nuxshell.lower() == "nuxshell":
            url = f"https://api.github.com/repos/gautamritvik/SupeNux-NuxShell/issues"
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
            }
            data = {
                'title': title,
                'body': body,
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                print("\nIssue created successfully!")
                print("Issue URL:", response.json()['html_url'])
            else:
                print(f"\nError: Failed to create issue. Status Code: {response.status_code}")
                print(response.json())
        else:
            print("Error: Invalid input. Please type 'SupeNux' or 'NuxShell'.")
            return


    if supenux_or_nuxshell.lower() == "supenux":
        repo = 'gautamritvik/SupeNux'
    elif supenux_or_nuxshell.lower() == "nuxshell":
        repo = 'gautamritvik/SupeNux-NuxShell'

    title = input("Enter the title of the issue: ")
    body = input("Explain the issue: ")
    token = "github-token"

    t = threading.Thread(target=loading_animation)
    t.start()
    create_github_issue(repo, title, body, token)
    global done
    done = True
    t.join()

def change_file_dir():
    current_file_path = input("Enter the current path of the file: ")
    new_directory = input("Enter the new directory to move the file to: ")

    y_or_n = input(f"Are you sure you want to move the file '{current_file_path}' to '{new_directory}'? Some bad things can happen to other programs that need the file if the directory changes. (y/n): ")
    
    if y_or_n == "y":
        try:
            # Check if the current file exists
            if not os.path.isfile(current_file_path):
                print(f"Error: The file at '{current_file_path}' was not found. Maybe you typed the directory wrong or the directory does not exist.")
                return

            # Check if the new directory exists
            if not os.path.isdir(new_directory):
                print(f"Error: The directory '{new_directory}' was not found. Maybe you typed the directory wrong or the directory does not exist.")
                return

            # Move the file
            new_file_path = os.path.join(new_directory, os.path.basename(current_file_path))
            os.rename(current_file_path, new_file_path)
            print(f"File was moved successfully to '{new_file_path}'. To check if it actually worked, type the command 'list -files.all'.")

        except Exception as e:
            print(f"Error: {e}")
    elif y_or_n == "n":
        print("File was not moved.")
    else:
        print("Error: Invalid input. Please type 'y' or 'n'.")
        return

def list_files():
    user_selected_dir = input("Enter the directory to list all files: ")

    try:
        files = os.listdir(user_selected_dir)
        if not files:
            print("Notice: Directory is empty.")
            return

        # Get terminal width and calculate number of columns
        terminal_width = shutil.get_terminal_size().columns
        max_file_len = max(len(f) for f in files) + 2
        columns = terminal_width // max_file_len

        if columns == 0:
            columns = 1

        # Calculate the number of rows
        rows = math.ceil(len(files) / columns)

        # Print files in rows and columns
        for row in range(rows):
            for col in range(columns):
                idx = row + col * rows
                if idx < len(files):
                    print(f"{files[idx]:<{max_file_len}}", end="")
            print()  # Newline after each row

    except FileNotFoundError:
        print(f"Error: Directory '{user_selected_dir}' was not found. Maybe you typed the directory wrong or the directory does not exist.")
    except PermissionError:
        print(f"Error: Permission denied while trying to read files at the directory '{user_selected_dir}'.")

def open_file():
    dir_of_file = input("Enter the directory of the file: ")
    try:
        file = open(dir_of_file, 'r')
        try:
            content = file.read()
            print(f"\n{content}")
        except PermissionError:
            print(f"Error: Permission was denied while trying to read the file at the directory '{dir_of_file}'.")
        except Exception as e:
            print(f"Error: {e}")

        file.close()
    except FileNotFoundError:
        print(f"Error: File at the directory '{dir_of_file}' was not found. Maybe you typed the directory wrong or the directory does not exist.")

# def create_file():
    

def run_cmd_bash():
    bash_path = "/Users/Admin/Downloads/nuxshell_to_bash.sh"
    try:
        subprocess.run(['bash', bash_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Bash Shell Error: {e}")
    time.sleep(1)

# Command workflow
commands = {
    "exit": exit_terminal, # Exits the terminal
    "clear": clear_terminal, # Clears the terminal
    "system -info": system_info, # Gives system information
    "system.memory -info": system_memory_info, # Gives system's memory information
    "system.disk -info": system_disk_info, # Gives system's disk information
    "launch -txtr": launch_txtr, # Launches Textitor, a word processor
    "help": help_cmds, # Gives you the list of currently working commands
    "report -issue": report_issue, # Helps you report an issue via NuxShell to SupeNux's GitHub Issue page
    "change -file.dir": change_file_dir, # Changes the directory of a file
    "list -files": list_files, # Lists all files stored in the local PC
    "open -file": open_file, # Opens a file
    "run -cmd.bash": run_cmd_bash # Runs commands in the good ol' bash
}

def main():
    global nuxshell_app_name
    global user_cmd
    while True:
        if nuxshell_app_name == "supenux_nuxshell.py":
            nuxshell_app_name = "NuxShell"
        elif nuxshell_app_name != "supenux_nuxshell.py":
            pass
        elif "." in nuxshell_app_name and nuxshell_app_name.rsplit(".", 1)[1]:
            print(f"Error: The NuxShell app name was not defined properly because there was an extension detected in the name. The detected extension was: '.{nuxshell_app_name.rsplit(".", 1)[1]}'")
            nuxshell_app_name = "undefined"
            
        if "." in nuxshell_app_name and nuxshell_app_name.rsplit(".", 1)[1]:
            if platform.system() == "Darwin":
                print(f"Error: The NuxShell app name was not defined properly because there was an extension detected in the name. The detected extension was: '.{nuxshell_app_name.rsplit(".", 1)[1]}'")
                nuxshell_app_name = "undefined"
                user_cmd = input(f"SupeNux NuxShell (MacOS) @ {nuxshell_dir}/{nuxshell_app_name} --- $ >>> ")
            elif platform.system() == "Linux":
                print(f"Error: The NuxShell app name was not defined properly because there was an extension detected in the name. The detected extension was: '.{nuxshell_app_name.rsplit(".", 1)[1]}'")
                nuxshell_app_name = "undefined"
                user_cmd = input(f"SupeNux NuxShell (Linux) @ {nuxshell_dir}/{nuxshell_app_name} --- $ >>> ")
            elif platform.system() == "SupeNux":
                print(f"Error: The NuxShell app name was not defined properly because there was an extension detected in the name. The detected extension was: '.{nuxshell_app_name.rsplit(".", 1)[1]}'")
                nuxshell_app_name = "undefined"
                user_cmd = input(f"SupeNux NuxShell @ {nuxshell_dir}/{nuxshell_app_name} --- $ >>> ")
            elif platform.system() == "Windows":
                print(f"Error: The NuxShell app name was not defined properly because there was an extension detected in the name. The detected extension was: '.{nuxshell_app_name.rsplit(".", 1)[1]}'")
                nuxshell_app_name = "undefined"
                user_cmd = input(f"SupeNux NuxShell (Windows) @ {nuxshell_dir}\\{nuxshell_app_name} --- $ >>> ")
        else:
            if platform.system() == "Darwin":
                user_cmd = input(f"SupeNux NuxShell (MacOS) @ {nuxshell_dir}/{nuxshell_app_name} --- $ >>> ")
            elif platform.system() == "Linux":
                user_cmd = input(f"SupeNux NuxShell (Linux) @ {nuxshell_dir}/{nuxshell_app_name} --- $ >>> ")
            elif platform.system() == "SupeNux":
                user_cmd = input(f"SupeNux NuxShell @ {nuxshell_dir}/{nuxshell_app_name} --- $ >>> ")
            elif platform.system() == "Windows":
                user_cmd = input(f"SupeNux NuxShell (Windows) @ {nuxshell_dir}\\{nuxshell_app_name} --- $ >>> ")
        
        global commands
        if user_cmd in commands:
            commands[user_cmd]()
        else:
            try:
                result = subprocess.run(cmd, shell=True)
                print(result.stdout.decode())
            except TypeError:
                print("Error: Command not found.")

if platform.system() == "Windows":
    os.system("cls")
elif platform.system() == "Linux" or platform.system() == "Darwin":
    os.system("clear")
elif platform.system() == "SupeNux":
    print("work in progress srry :)")

main()
