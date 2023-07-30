import pyautogui
import time

def run_as_admin(application_path):
    # Open the Start menu or the application launcher
    pyautogui.press('win')

    # Wait for the Start menu or the application launcher to open
    time.sleep(1)

    # Search for the application in the Start menu or the application launcher
    pyautogui.write(application_path)

    # Wait for the search results to appear
    time.sleep(1)
    #pyautogui.rightClick()

    #pyautogui.rightClick()

    screen_width, screen_height = pyautogui.size()

    # Calculate the position of the Windows button on the taskbar
    windows_button_x = int(screen_width * 0.03)
    windows_button_y = int(screen_height - (screen_height * 0.03))

    # Move the cursor to the Windows button
    pyautogui.moveTo(windows_button_x, windows_button_y)

    time.sleep(1)

    # Move the mouse to the first search result
    pyautogui.move(120, -845)
    pyautogui.click()

    pyautogui.moveTo(windows_button_x, windows_button_y)
    pyautogui.move(120, -720)
    pyautogui.click()


    # Wait for the right-click context menu to appear
    

    #Move the mouse to the "Run as administrator" option
    #pyautogui.moveTo(30, 30)

    # Perform a left-click on the "Run as administrator" option
    #pyautogui.click()

    # Wait for the application to launch with administrative privileges
    #time.sleep(8)
    #pyautogui.moveTo(850, 500)
    #time.sleep(5)
    #pyautogui.click()
    time.sleep(7)
    pyautogui.hotkey('ctrl', 'o')
    
    
    
# Specify the application path
application_path = "Photoshop CS6"

# Call the function to run the application as administrator
run_as_admin(application_path)

#timpe.sleep(10)

#pyautogui.hotkey('ctrl', 'o')
#time.sleep(3) 