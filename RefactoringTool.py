import linecache
from tqdm import tqdm
from termcolor import colored

fixInsight = open(r"C:\Users\zahra\Documents\GitHub\WWRefactoringTool\FixInsight.txt", "r")
print('Reading FixInsight Log: ')
lst = []
dic = {}

for Line in tqdm(fixInsight):
    Line = Line.strip().split(" ")
    uName = Line[2][:Line[2].index("(")]
    uLine = int(Line[2][Line[2].index("(") + 1 :Line[2].index(")")])
    uParameter = Line[10].strip("'")

    print("\nCurrent Unit:", colored(uName, "cyan"), "\nCurrent Line:", colored(uLine, "cyan"), "\nCurrent Parameter:", colored(uParameter, "cyan"))

    path = r"C:\Users\zahra\Documents\GitHub\WWRefactoringTool"
    currentUnit = path + "\\" + uName

    uParameter = uParameter + ": string"
    cParameter = "const " + uParameter
    try:
        getLine = linecache.getline(currentUnit, uLine)
        getLine = getLine[getLine.index(".") + 1 : getLine.index(uParameter) + len(uParameter)]
        changeLine = getLine.replace(uParameter, cParameter)
        with open(currentUnit, 'r+', encoding = "utf8") as fHandle:
            base = fHandle.read()
            changed = base.replace(getLine, changeLine)
            _ = changed.count(changeLine)

            if _ % 2 != 0:
                dic[uName] = _

            fHandle.seek(0)
            fHandle.write(changed)
            fHandle.close()
            linecache.clearcache()

        print(colored("Successfully changed", "green"))
    except:
        print(colored(f"Error in {uName}", "red"))
        lst.append(uName)

if len(lst) > 0:
    print("\nReplacing finished with", colored(f"Errors in {len(lst)} Unit(s)", "red"))
    for _ in lst:
        print(colored(_ , "red"))
else:
    print(colored("\nReplacing done successfully.\n", "green"))

if len(dic) > 0:
    print(colored("\nWarning: ", "yellow"))
    print("You must check these Units: ")
    for key, value in dic.items():
        print(colored(f"{key} : {value}", "yellow"))

input("\nPress Enter to exit...")
