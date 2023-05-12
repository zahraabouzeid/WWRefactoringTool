import pyautogui
import time 
import pyperclip
from termcolor import colored

lst = []
fixInsight = open(r"C:\Users\zahra\Documents\GitHub\WWRefactoringTool\FixInsight.txt", "r")

for Line in fixInsight:
    try:
        # Getting the name of the unit, line and parameter
        Line = Line.strip().split(" ")
        uName = Line[2][:Line[2].index("(")]
        uLine = int(Line[2][Line[2].index("(") + 1 :Line[2].index(")")])
        uParameter = Line[10].strip("'")
        print("\nCurrent Unit:", colored(uName, "yellow"), "\nCurrent Line:", colored(uLine, "yellow"), "\nCurrent Parameter:", colored(uParameter, "yellow"))

        uParameter = uParameter + ": string"
        cParameter = "const " + uParameter

        # Wait to focus the window
        time.sleep(10)

        # Opening the Unit
        pyautogui.hotkey("ctrl", "f12")
        time.sleep(5)
        pyautogui.typewrite(uName)
        pyautogui.press("enter")

        # Searching for the line
        pyautogui.hotkey("alt", "g")
        time.sleep(5)
        pyautogui.typewrite(uLine)
        pyautogui.press("enter")

        # Selecting and copying the implementation
        pyautogui.press("home")
        pyautogui.hotkey("shift", "end")
        pyautogui.hotkey("ctrl", "c")

        # Replacing the parameter in the implementation
        selectedLine = pyperclip.paste()
        modifiedLine = selectedLine.replace(uParameter, cParameter, 1)
        pyperclip.copy(modifiedLine)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(5)

        # Navigating to declaration
        pyautogui.hotkey("ctrl", "shift", "up")

        # Selecting and copying the declaration
        pyautogui.press("home")
        pyautogui.hotkey("shift", "end")
        pyautogui.hotkey("shift", "down")
        pyautogui.hotkey("shift", "down")
        pyautogui.hotkey("ctrl", "c")

        # Replacing the parameter in the declaration
        selectedLine = pyperclip.paste()
        modifiedLine = selectedLine.replace(uParameter, cParameter, 1)
        pyperclip.copy(modifiedLine)
        pyautogui.hotkey("ctrl", "v")

        # Saving the file
        pyautogui.hotkey("ctrl", "s")
        print(colored("Done", "green"))
        
    except:
        lst.append(uName)

if len(lst) > 0:
    print(colored("\nErrors occured in: ", "red"))
    for _ in lst:
        print(colored(_, "red"))

input("\nPress Enter to exit...")
