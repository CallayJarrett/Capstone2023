import time
import pyautogui as pi
import os
import pyperclip
import subprocess

def open_photoshop_cs6(photoshop_path): #python function to open the photoshop appliciton and the picture in the application
    
    try:
        os.startfile(photoshop_path)
        time.sleep(5)  # Wait for Photoshop to open (adjust this time if necessary)
    except FileNotFoundError:
        print("Error: Photo File not found.") #if the file path is incorrect then this error is thrown
    except Exception as e:
        print("An error occurred:", str(e)) #any other errors are thrown here

        

def execute_script(script_path): #this script is ran when the app in open 
    # Press 'File'
    pi.hotkey('alt', 'f') #open the file path
    time.sleep(5)
    
    for _ in range(19): #press down arrow unitl you get to the scripts option
        pi.press('down')
        time.sleep(0.1)
    
    time.sleep(1)
    pi.press('right')#press right arrow to get the script options
    time.sleep(2)

    for _ in range(12):
        pi.press('down')#press down to get to the browse option to choose a jsx script
        time.sleep(0.3)
    
    pi.press('enter')
    pi.write("C" + script_path)#open and execute the jsx file
    pi.press('enter')
    
    time.sleep(5)
    pi.press('enter')#close the alert window

def run_photoshop_script(photoshop_path, script_path):
    command = f'"{photoshop_path}" "{script_path}"'
    completed_process = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if completed_process.returncode == 0:
        print("Photoshop script applied successfully.")
    else:
        print("An error occurred while applying the Photoshop script.")
        print("Error message:", completed_process.stderr)



if __name__ == "__main__":
    #photo_path = input("Enter the fule path of your photo: ")
    #sc_path =  input("Enter the file path of your extendscript file: ")
    photo_path = "C:\\Users\\Gabriel Scott\\OneDrive\\Pictures\\Saved Pictures\\chello.jpeg"
    sc_path = "C:\\Users\\Gabriel Scott\OneDrive\\Desktop\\COMP3901\\opal.jsx"
    

    open_photoshop_cs6(photo_path)
    time.sleep(10)
    execute_script(sc_path)