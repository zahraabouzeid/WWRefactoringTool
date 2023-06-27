import re

searchResults = open(r"C:\Users\zahra\Documents\MyWorkspace\OnGetEdit\SearchResults.txt", "r")

for Line in searchResults:
    pas = re.search(".*.pas", Line).group()
    dfm = pas.strip(".pas") + ".dfm"
    grd = re.search("prc(.*?)Get", Line).group().strip("prc").strip("Get")

    # print(pas)
    # print(dfm)
    # print(grd)

    # prcGetEdit = re.search('".*"', Line).group().strip('"').strip("procedure").strip()
    prcGetEdit = f"prc{grd}GetEditText(Sender: TObject; ACol, ARow: Integer; const Value: string);"
    prcSetEdit = f"prc{grd}SetEditText(Sender: TObject; ACol, ARow: Integer; const Value: string);"
 
    GetEditEvent = prcGetEdit.replace(prcGetEdit[prcGetEdit.index("Get"): ], "WWOnGetEditText(Sender: TObject; _objGridCol: TwwGridCol, _iItemIndex: Integer; const Value: string);")
    SetEditEvent = prcSetEdit.replace(prcSetEdit[prcSetEdit.index("Set"): ], "WWOnSetEditText(Sender: TObject; _objGridCol: TwwGridCol, _iItemIndex: Integer; const Value: string);")

    # print(prcGetEdit)

    pasPath = r"C:\Users\zahra\Documents\MyWorkspace\OnGetEdit" + "\\" + pas
    dfmPath = r"C:\Users\zahra\Documents\MyWorkspace\OnGetEdit" + "\\" + dfm
    # print(pasPath)
    # print(dfmPath)

    # Open the dfm and make changes
    with open(dfmPath, 'r+', encoding = "utf8") as dfmHandle:
        # Events
        OnSetEdit = f"OnSetEditText = {grd}SetEditText"
        WWOnSetEdit = f"WWOnSetEditText = {grd}WWOnSetEditText"

        OnGetEdit = f"OnGetEditText = {grd}GetEditText"
        WWOnGetEdit = f"WWOnSetEditText = {grd}WWOnGetEditText"

        base = dfmHandle.read()
        changed = base.replace(OnSetEdit, WWOnSetEdit).replace(OnGetEdit, WWOnGetEdit)

        dfmHandle.seek(0)
        dfmHandle.write(changed)

    # Open the unit and change the procedure
    with open(pasPath, 'r+', encoding = "utf8") as pasHandle:
        base = pasHandle.read()
        changed = base.replace(prcGetEdit, GetEditEvent).replace(prcSetEdit, SetEditEvent)

        pasHandle.seek(0)
        pasHandle.write(changed)

    # Open the unit and change the aCol and aRow
    with open(pasPath, 'r+', encoding='utf8') as pasHandle:
        base = pasHandle.read()
        start = 0
        for Line in base:
            start += 1
            if GetEditEvent in Line:
                break

        end = None
        for j in range(start, len(base)):
            if "procedure " in base[j] or "function " in base[j]:
                end = j
                break
        
        implementation = base[start:end]
        for Line in implementation:
            if "aRow" in Line:
                aRow = re.search(".*=.*\.*\[.*\(aRow\)]", Line).group()
                iItemIndex = aRow[ :aRow.index("[") + 1] + "_iItemIndex" + aRow[aRow.index("]"): ] 
                editedImplementation = Line.replace(aRow, iItemIndex)
            elif "aCol" in Line:
                Col = re.search("'.*'", Line).strip("'").group()
                editedImplementation = Line.replace(f"aCol = fctgetColNum('{Col}')", f"_objGridCol = '{Col}'")
        
        changed = base.replace(implementation, editedImplementation)
        pasHandle.seek(0)
        pasHandle.write(base)