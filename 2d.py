data = {}
weapons_data = {}
uncode_data = {
    "вљЄ": "⚪",
    "вЁ‡": "⨇",
    "б—ќ": "ᗝ"
}

with open("WeaponsDATA.csv") as f:
    header = f.readline()
    for line in f:
        line = line.rstrip()
        line = line.split(", ")
        if line[6] in uncode_data:
            line[6] = uncode_data[line[6]]
        weapons_data[line[0]] = {
            "place": line[1],
            "damage": line[2],
            "type": line[3],
            "control": line[4],
            "effects": line[5].split(";"),
            "symbol": line[6]
        }


with open("UnitsDATA2.csv") as file:
    file.readline()
    for line in file:
        line = line.rstrip()
        lst = line.split(", ")
        data[lst[0]] = {
            "hp": int(lst[1]),
            "move": int(lst[2]),
            "lenwig": [int(string) for string in lst[3].split(";")],
            "weapons": [row.split(";") for row in lst[4].split("/")],
            "armor": [int(string) for string in lst[5].split(";")],
            "pay": int(lst[6])
        }

for unit in data:
    print("-"*20 + unit + ":")
    for par in data[unit]:
        if par == "weapons":
            print("---- WEAPONS:")
            for row in data[unit]["weapons"]:
                print("| ", end="")
                for weapon in row:
                    if weapon == "":
                        text = " "
                    else:
                        text = weapons_data[weapon]["symbol"]
                    print(text, end=" ")
                print("|")
        else:
            print(par + " :  ", data[unit][par])

input()