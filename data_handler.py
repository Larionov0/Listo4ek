data = {}
units_data = {}
weapons_data = {}
uncode_data = {
    "вљЄ": "⚪",
    "вЁ‡": "⨇",
    "б—ќ": "ᗝ"
}

with open("WavesDATA.csv") as f:
    header = f.readline()
    for line in f:
        line_list = line.split(", ")
        line_list[0], line_list[1] = int(line_list[0]), int(line_list[1])
        if line_list[0] in data:
            data[line_list[0]][line_list[1]] = {
                "reward":[],
                "enemies":[]
            }
        else:
            data[line_list[0]] = {
                line_list[1]:{
                    "reward":[],
                    "enemies":[]
                    }
            }
        reward = line_list[2].split("|")

        for i in range(len(reward)):
            set = reward[i]
            data[line_list[0]][line_list[1]]["reward"].append([])
            squads = set.split(" + ")
            for j in range(len(squads)):
                squad = squads[j]
                data[line_list[0]][line_list[1]]["reward"][i].append([])
                for point in squad.split("_"):
                    data[line_list[0]][line_list[1]]["reward"][i][j].append(point)

        enemies = line_list[3].rstrip().split("|")
        for i in range(len(enemies)):
            set = enemies[i]
            data[line_list[0]][line_list[1]]["enemies"].append([])
            squads = set.split(" + ")
            for j in range(len(squads)):
                squad = squads[j]
                data[line_list[0]][line_list[1]]["enemies"][i].append([])
                for point in squad.split("_"):
                    data[line_list[0]][line_list[1]]["enemies"][i][j].append(point)

                count_price = data[line_list[0]][line_list[1]]["enemies"][i][j][0]
                if "$" in count_price:
                    count_price = count_price.split("$")
                    data[line_list[0]][line_list[1]]["enemies"][i][j] = [count_price[0], count_price[1], data[line_list[0]][line_list[1]]["enemies"][i][j][1]]  #
                else:
                    data[line_list[0]][line_list[1]]["enemies"][i][j].insert(1,"0")




for p in data:
    print("---=",p, "lvl")
    for l in data[p]:
        print(l,data[p][l])
"""
---= 1 lvl
1 {'reward': [[['10', 'soldiers']], [['1', 'turrets'], ['2', 'soldiers']]], 'enemies': [[['3-5', '10', 'soldiers'], ['0-1', '20', 'turrets']]]}
2 {'reward': [[['2', 'turrets']]], 'enemies': [[['5-8', '10', 'soldiers'], ['1-2', '20', 'turrets']]]}
3 {'reward': [[['100', 'coins']]], 'enemies': [[['1', 0, 'tank']]]}
---= 2 lvl
1 {'reward': [[['3', 'turrets']], [['1', 'tank']]], 'enemies': [[['3-6', '10', 'soldiers'], ['1-3', '20', 'turrets'], ['1', '50', 'tank ']], [[' 30', '10', 'soldiers'], ['1', '20', 'turret']]]}
"""


with open("UnitsDATA.csv") as f:
    header = f.readline()
    for line in f:
        line = line.split(", ")
        units_data[line[0]] = {
            "hp":int(line[1]),
            "move":int(line[2]),
            "armor":line[4].split(";"),
            "weapons":{},
            "pay":int(line[5])
        }
        weapons = line[3].split(" + ")
        for weapon in weapons:
            weapon = weapon.split("_")
            units_data[line[0]]["weapons"][weapon[1]] = int(weapon[0])


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