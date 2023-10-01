import subprocess
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import tkinter as tk



def monitor_url_and_prompt(browser):
    """
    Monitor the browser URL for changes. If a change is detected, prompt the user to activate the script.
    Returns True if the user wants to activate the script, False otherwise.
    """
    current_url = browser.current_url
    while True:
        # If the URL has changed, ask the user if they want to activate the script
        if browser.current_url != current_url:
            current_url = browser.current_url
            # Extract the candidate's name
            try:
                name_element = browser.find_element(By.XPATH, "//div[contains(@class, 'artdeco-entity-lockup__title')]")
                candidate_name = name_element.text.strip()
            except NoSuchElementException:
                candidate_name = 'Unknown Profile'

            decision = input(f"URL changed to profile of {candidate_name}. \nActivate on this profile? (y/n): ")
            if decision.lower() == 'y':
                return True
        time.sleep(2)  # Check every 2 seconds

def get_output_language():
    """
    Prompt the user for the desired output language: Swedish or English.
    Returns 'swedish' or 'english' based on the user's choice.
    """
    while True:
        lang_choice = input("Do you want the output in Swedish (s) or English (e)? ").lower()
        if lang_choice == 's':
            return 'swedish'
        elif lang_choice == 'e':
            return 'english'
        else:
            print("Invalid choice. Please enter 's' for Swedish or 'e' for English.")


def open_independent_message_window(message, candidate_name):
    def on_close():
        # Simply destroy the window, the clipboard content will be preserved
        root.destroy()

    root = tk.Tk()
    root.title(f"Message for: {candidate_name}")

    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.insert(tk.INSERT, message)
    text_widget.pack(expand=True, fill=tk.BOTH)
    
    # Set the initial window size
    root.geometry("430x500")  # width x height
    
    # Create an auxiliary Tkinter instance to hold the clipboard content after the main window is closed
    aux_clipboard = tk.Tk()
    aux_clipboard.withdraw()  # Hide the auxiliary window

    def preserve_clipboard():
        content = aux_clipboard.clipboard_get()
        aux_clipboard.clipboard_clear()
        aux_clipboard.clipboard_append(content)
        aux_clipboard.update()  # Update the auxiliary Tkinter instance to keep the clipboard content

    root.protocol("WM_DELETE_WINDOW", on_close)  # Bind the on_close method to window close event
    root.bind('<Escape>', lambda event: on_close())  # Bind the on_close method to Escape key event
    root.bind('<Destroy>', lambda event: preserve_clipboard())  # Bind the preserve_clipboard method to Destroy event
    
    root.mainloop()




def open_notepad_with_message(message):
    """
    Open Notepad and paste the generated message.
    """
    with open('temp_message.txt', 'w') as file:
        file.write(message)
    
    subprocess.run(['notepad.exe', 'temp_message.txt'])