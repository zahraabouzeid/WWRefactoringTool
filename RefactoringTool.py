import linecache
from tqdm import tqdm
from termcolor import colored

fixInsight = open("FixInsight.txt")
print('Reading FixInsight Log: ')
lst = []

for Line in tqdm(fixInsight):
    Line = Line.strip().split(" ")
    uName = Line[2][:Line[2].index("(")]
    uLine = int(Line[2][Line[2].index("(") + 1 :Line[2].index(")")])
    uParameter = Line[10].strip("'")
    print()
    print(f"Current Unit: {uName} \nCurrent Line: {uLine} \nCurrent Parameter: {uParameter}")

    path = r"C:\Users\zahra\Documents\GitHub\WWRefactoringTool"
    currentUnit = path + "\\" + uName
    print('Reading Unit: ')

    uParameter = uParameter + ": string"
    cParameter = "const " + uParameter
    try:
        getLine = linecache.getline(currentUnit, uLine)
        getLine = getLine[getLine.index(".") + 1 : getLine.index(")")]
        changeLine = getLine.replace(uParameter, cParameter)
        print (f"Replacing {getLine} with {changeLine}")
        with open(currentUnit, 'r+', encoding='utf8') as fHandle:
            base = fHandle.read()
            changed = base.replace(getLine, changeLine)
            fHandle.seek(0)
            fHandle.write(changed)
            fHandle.truncate()
            fHandle.close()
            linecache.clearcache()
    except:
        print(colored(f"Error in {uName}", "red"))
        lst.append(uName)

print("\nReplacing finished with", colored(f"Errors in {len(lst)} Unit(s):", "red"))

if len(lst) > 0:
    for _ in lst:
        print(colored(_ , "red"))