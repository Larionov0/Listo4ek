import telebot
from telebot import types
import emoji
from data_handler import data as waves_data, units_data, weapons_data
from random import choice, randint
from funks import *


delete_data = {}

def add_delete_message(chat_id,message_id):
    if chat_id in delete_data:
        delete_data[chat_id].append(message_id)
    else:
        delete_data[chat_id] = [message_id]


data = {
    000000: {
        "name": "Larko",
        "lvl": 10,
        "coins": 0,
        "armament": {
            "active": {
                "location": {
                    "soldiers": 100,
                    "turrets": 10,
                    "tanks": 16,
                    }
                },
            "passive": {
                "soldiers": 100,
                "turrets": 10,
                "tanks": 16,
                }
        },
        "location": "wasteland",
        "action": None
    },
    "count_of_lands":0
}
bot = telebot.TeleBot("625314496:AAEQ_L7mcsmhdB8DytiMXfEc3CAGEJaI_iE")

@bot.message_handler(commands = ["start"])
def start(message):
    add_delete_message(message.chat.id, bot.send_message(message.chat.id, "😃🥳😈👾💣⚙💥\nHello, ۞today you will play the best game ever!").message_id)
    if message.chat.id in data:
        menu(message.chat.id)
    else:
        data[message.chat.id] = "creating"
        id = bot.send_message(message.chat.id, "Please input your name:").message_id
        add_delete_message(message.chat.id,id)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=["help"])
def help(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('message Larko',url = 'https://t.me/Larko_0'))
    bot.send_message(message.chat.id,
                     "Please, tell me about your problem",
                     reply_markup=keyboard)


@bot.message_handler(func = lambda call: True, content_types = ['text'])
def text_callback(message):
    chat_id = message.chat.id
    for chat in delete_data:
        for i in range(len(delete_data[chat])):
            id = delete_data[chat][0]
            bot.delete_message(chat,id)
            delete_data[chat].remove(id)
    bot.delete_message(chat_id,message.message_id)
    if chat_id in data:
        if data[chat_id] == "creating":
            location = "wasteland " + str(data["count_of_lands"])
            data["count_of_lands"] += 1
            data[chat_id] = {
                "name":message.text,
                "lvl":1,
                "wave":1,
                "coins":100,
                "armament": {
                    "active": {
                        location: {
                            "soldiers": {"hp":[],"count":3},
                        },
                    },
                    "passive": {
                        "soldiers": 5,
                        "turrets": 1,
                    }
                },
                "location": location,
                "locations": [location],
                "action": "start",
            }
            menu(chat_id)

        elif data[chat_id]["action"] == "wave - count shot":
            num = num_validator(message.text)
            if num != False:
                if num > data[chat_id]["attack points"][data[chat_id]["choosed armament"]]:
                    num = data[chat_id]["attack points"][data[chat_id]["choosed armament"]]
                num1 = num
                while num > 0 and data[chat_id]["target"] in data[chat_id]["enemies"]:
                    enemies = data[chat_id]["enemies"]
                    armament = data[chat_id]["choosed armament"]
                    for weapon in units_data[armament]["weapons"]:
                        for temp in range(units_data[armament]["weapons"][weapon]):
                            one_shot(chat_id, weapon)
                    num -= 1
                data[chat_id]["attack points"][data[chat_id]["choosed armament"]] -= num1 - num
                check_after_shot(chat_id)

            else:
                id = bot.send_message(chat_id,"Please input correct number").message_id
                add_delete_message(chat_id,id)
        elif data[chat_id]["action"] == "set armament":
            num = num_validator(message.text)
            if num!=False:
                set_armament(chat_id,data[chat_id]["target"],num)
                menu(chat_id)
            else:
                add_delete_message(chat_id, bot.send_message(chat_id,"Please input correct number:").message_id)


@bot.callback_query_handler(lambda call: True)
def get_callback(call):
    chat_id = call.message.chat.id
    if chat_id not in data:
        return
    player = data[chat_id]
    for chat in delete_data:
        for i in range(len(delete_data[chat])):
            id = delete_data[chat][0]
            bot.delete_message(chat,id)
            delete_data[chat].remove(id)
    bot.delete_message(chat_id,call.message.message_id)

    if data[chat_id]["action"] == "Pick menu: Wave, Map, Set":
        if call.data == "WAVE":
            bot.answer_callback_query(call.id)
            data[chat_id]["action"] = "wave"
            wawe = waves_data[player["lvl"]][player["wave"]]
            enemies = choice(wawe["enemies"])
            data[chat_id]["enemies"] = {}
            for enemy in enemies:
                data[chat_id]["enemies"][enemy[-1]] = {}
                for i in range(2):      #pick count and coins
                    if "-" in enemy[i]:
                        coins = enemy[i].split("-")
                        coins = randint(int(coins[0]),int(coins[1]))
                    else:
                        coins = int(enemy[i])
                    point = ["count","coins"][i]
                    data[chat_id]["enemies"][enemy[-1]][point] = coins
                if data[chat_id]["enemies"][enemy[-1]]["count"] <= 0:
                    data[chat_id]["enemies"].pop(enemy[-1])
                else:
                    data[chat_id]["enemies"][enemy[-1]]["hp"] = []
            data[chat_id]["reward"] = {}

            wave_func(chat_id)

        elif call.data == "SET ARMAMENT":
            data[chat_id]["action"] = "set armament"
            keyboard = types.InlineKeyboardMarkup()
            for unit in data[chat_id]["armament"]["passive"]:
                keyboard.add(types.InlineKeyboardButton("{} x {}".format(unit,data[chat_id]["armament"]["passive"][unit]),callback_data=unit))
            keyboard.add(types.InlineKeyboardButton("Cancel",callback_data="CANCEL"))
            bot.send_message(chat_id,"Pick units:",reply_markup=keyboard)

        elif call.data == "MAP":
            keyboard = types.InlineKeyboardMarkup()

            keyboard.add(types.InlineKeyboardButton())

    elif call.data == "loose":
        bot.answer_callback_query(chat_id)

    elif data[chat_id]["action"] == "set armament":
        if call.data == "CANCEL":
            return menu(chat_id)
        elif call. data == "set armament - 1":
            set_armament(chat_id,data[chat_id]["target"],1)
            menu(chat_id)
        elif call.data == "set armament - count":
            add_delete_message(chat_id, bot.send_message(chat_id, "Please input count of units to set:").message_id)
        elif call.data == "set armament - all":
            set_armament(chat_id, data[chat_id]["target"], data[chat_id]["armament"]["passive"][data[chat_id]["target"]])
            menu(chat_id)
        elif call.data == "set armament - cancel":
            menu(chat_id)
        else:
            data[chat_id]["target"] = call.data
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton("1", callback_data="set armament - 1"),
                types.InlineKeyboardButton("Input count", callback_data="set armament - count"),
            )
            keyboard.row(
                types.InlineKeyboardButton("All", callback_data="set armament - all"),
                types.InlineKeyboardButton("Cancel", callback_data="set armament - cancel"),
            )
            bot.send_message(chat_id,"How many units want you to set?🔥",reply_markup=keyboard)

    elif data[chat_id]["action"].startswith("wave - "):
        if data[chat_id]["action"] == "wave - pick armament":
            if call.data != "cancel":
                print(1)
                bot.answer_callback_query(call.id)
                unit = call.data
                data[chat_id]["choosed armament"] = unit
                choose_target_class(chat_id)
            else:
                wave_menu(chat_id)

        elif data[chat_id]["action"] == "wave - pick enemy":
            bot.answer_callback_query(call.id)
            if call.data != "cancel":
                keyboard = types.InlineKeyboardMarkup()
                keyboard.row(
                    types.InlineKeyboardButton("😐 SINGLE SHOT",callback_data="SINGLE"),
                    types.InlineKeyboardButton("😈 CHOOSE COUNT of shots",callback_data = "COUNT")
                )
                keyboard.row(
                    types.InlineKeyboardButton("😱 SHOOT TO KILL",callback_data="KILL"),
                    types.InlineKeyboardButton("🥺 CANCEL",callback_data = "CANCEL")
                )
                data[chat_id]["action"] = "wave - pick shot option"
                data[chat_id]["target"] = call.data
                bot.send_message(chat_id,text = "{} -> {}\nChoose way to destroy:".format(data[chat_id]["choosed armament"],data[chat_id]["target"]),reply_markup=keyboard)
            else:
                wave_menu(chat_id)

        elif data[chat_id]["action"] == "wave - pick shot option":
            if call.data != "CANCEL":
                bot.answer_callback_query(call.id)
                shot(chat_id, call.data)
            else:
                choose_target_class(chat_id)

        elif data[chat_id]["action"] == "wave - enemies turn ends":
            bot.answer_callback_query(call.id)
            wave_func(chat_id)


def choose_target_class(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    for enemy in data[chat_id]["enemies"]:
        enemy_dict = data[chat_id]["enemies"][enemy]
        keyboard.add(types.InlineKeyboardButton("{} x {}            💚 {} / {}     🛡 {}".format(enemy, enemy_dict["count"], ";".join([str(hp) for hp in enemy_dict["hp"]]),
                                                          units_data[enemy]["hp"],";".join(units_data[enemy]["armor"])), callback_data=enemy))
    keyboard.add(types.InlineKeyboardButton("cancel",callback_data="cancel"))
    data[chat_id]["action"] = "wave - pick enemy"
    bot.send_message(chat_id, text="Good! (Armament: {} (x{} left))\n Now choose class of enemies armament to 🗡destroy it:".format(data[chat_id]["choosed armament"],
                                                                                                                                  data[chat_id]["attack points"][data[chat_id]["choosed armament"]]),
                     reply_markup=keyboard)


def level_reward(chat_id):
    coins = (data[chat_id]["lvl"]) * 50
    data[chat_id]["coins"] += coins
    add_delete_message(chat_id, bot.send_message(chat_id, "😁☝NEW LEVEL : {}\n\n💰 + {}".format(data[chat_id]["lvl"], coins)).message_id)


def victory(chat_id):
    data[chat_id].pop("attack points")
    data[chat_id].pop("choosed armament")
    data[chat_id].pop("target")
    data[chat_id].pop("enemies")
    data[chat_id].pop("reward")
    data[chat_id]["action"] = "wave - victory"

    rewards = choice(waves_data[data[chat_id]["lvl"]][data[chat_id]["wave"]]["reward"])
    add_delete_message(chat_id, bot.send_message(chat_id, "🥳Victoryy!!!\n🎁 REWARD 🎁").message_id)
    for reward in rewards:
        if reward[1] == "coins":
            data[chat_id]["coins"] += int(reward[0])
            add_delete_message(chat_id, bot.send_message(chat_id, "You got {} 💸".format(reward[0])).message_id)
        else:
            add_delete_message(chat_id, bot.send_message(chat_id, "👍 You got {} {}".format(reward[0],reward[1])).message_id)
            if reward[1] in data[chat_id]["armament"]["passive"]:
                data[chat_id]["armament"]["passive"][reward[1]] += int(reward[0])
            else:
                data[chat_id]["armament"]["passive"][reward[1]] = int(reward[0])

    if data[chat_id]["wave"]+1 in waves_data[data[chat_id]["lvl"]]:
        data[chat_id]["wave"] += 1
    else:
        data[chat_id]["lvl"] += 1
        level_reward(chat_id)
        data[chat_id]["wave"] = 1
    sum = 0
    for unit in data[chat_id]["armament"]["active"][data[chat_id]["location"]]:
        sum += units_data[unit]["pay"] * data[chat_id]["armament"]["active"][data[chat_id]["location"]][unit]["count"]
    add_delete_message(chat_id, bot.send_message(chat_id,"You need to pay {} $".format(sum)).message_id)
    data[chat_id]["coins"] -= sum
    menu(chat_id)


def enemies_turn(chat_id,start = True):
    if start:
        add_delete_message(chat_id,    bot.send_message(chat_id, "-----=== Enemies turn😡: ").message_id   )
        data[chat_id]["attack points"] = {}
        for unit in data[chat_id]["enemies"]:
            data[chat_id]["attack points"][unit] = data[chat_id]["enemies"][unit]["count"]

    for enemy in data[chat_id]["enemies"]:
        if enemy not in data[chat_id]["attack points"]:
            continue
        location = data[chat_id]["location"]
        target = choice(list(data[chat_id]["armament"]["active"][location].keys()))
        data[chat_id]["target"] = target
        player_armament = data[chat_id]["armament"]["active"][location]
        while data[chat_id]["attack points"][enemy] > 0 and target in player_armament:
            for weapon in units_data[enemy]["weapons"]:
                for temp in range(units_data[enemy]["weapons"][weapon]):
                    one_shot(chat_id, weapon, mode = "enemies")
            data[chat_id]["attack points"][enemy] -= 1
        if data[chat_id]["attack points"][enemy] == 0:
            data[chat_id]["attack points"].pop(enemy)
        if check_after_shot(chat_id, "enemies") == False:
            return


def set_armament(chat_id, unit, count):
    if count > data[chat_id]["armament"]["passive"][unit]:
        count = data[chat_id]["armament"]["passive"][unit]
    data[chat_id]["armament"]["passive"][unit] -= count
    location = data[chat_id]["location"]
    if data[chat_id]["armament"]["passive"][unit] == 0:
        data[chat_id]["armament"]["passive"].pop(unit)
    if unit in data[chat_id]["armament"]["active"][location]:
        data[chat_id]["armament"]["active"][location][unit]["count"] += count
    else:
        data[chat_id]["armament"]["active"][location][unit] = {
            "hp":[],
            "count":count
        }


def loose(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("OK :(", callback_data="loose"))
    bot.send_message(chat_id, "You loose(", reply_markup=keyboard)
    data.pop(chat_id)


def check_after_shot(chat_id, mode = "player"):
    if mode == "player":
        if len(data[chat_id]["enemies"].keys()) == 0:
            victory(chat_id)
        elif not any([data[chat_id]["attack points"][unit] > 0 for unit in data[chat_id]["attack points"]]):
            data[chat_id]["action"] = "wave - enemies turn"
            data[chat_id]["attack points"] = {}
            enemies_turn(chat_id)
        elif data[chat_id]["attack points"][data[chat_id]["choosed armament"]] > 0:
            choose_target_class(chat_id)
        else:
            wave_menu(chat_id)
    elif mode == "enemies":
        location = data[chat_id]["location"]
        if len(data[chat_id]["armament"]["active"][location].keys()) == 0:
            loose(chat_id)
            return False
        elif not any([data[chat_id]["attack points"][unit] > 0 for unit in data[chat_id]["attack points"]]):
            data[chat_id]["action"] = "wave - enemies turn ends"
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("OK",callback_data="OK"))
            bot.send_message(chat_id,"OK? :)", reply_markup=keyboard)
        else:
            enemies_turn(chat_id, False)
            return False


def shot(chat_id, option):
    if data[chat_id]["attack points"][data[chat_id]["choosed armament"]] > 0:
        data[chat_id]["action"] = "wave - shot"
        if option == "SINGLE":
            data[chat_id]["attack points"][data[chat_id]["choosed armament"]] -= 1
            enemies = data[chat_id]["enemies"]
            armament = data[chat_id]["choosed armament"]
            for weapon in units_data[armament]["weapons"]:
                for temp in range(units_data[armament]["weapons"][weapon]):
                    one_shot(chat_id, weapon)
            check_after_shot(chat_id)
        elif option == "COUNT":
            data[chat_id]["action"] = "wave - count shot"
            id = bot.send_message(chat_id, "Input count ({} left):".format(data[chat_id]["attack points"][data[chat_id]["choosed armament"]])).message_id
            add_delete_message(chat_id,id)
        elif option == "KILL":
            while data[chat_id]["attack points"][data[chat_id]["choosed armament"]] > 0 and data[chat_id]["target"] in data[chat_id]["enemies"]:
                enemies = data[chat_id]["enemies"]
                armament = data[chat_id]["choosed armament"]
                for weapon in units_data[armament]["weapons"]:
                    for temp in range(units_data[armament]["weapons"][weapon]):
                        one_shot(chat_id, weapon)
                data[chat_id]["attack points"][data[chat_id]["choosed armament"]] -= 1
            check_after_shot(chat_id)
    else:
        add_delete_message(chat_id, bot.send_message(chat_id,"😭Count of loaded {} = 0".format(data[chat_id]["choosed armament"])).message_id)
        wave_menu(chat_id)


def one_shot(chat_id, weapon, mode = "player"):
    if mode == "player":
        enemies = data[chat_id]["enemies"]
    elif mode == "enemies":
        enemies = data[chat_id]["armament"]["active"][data[chat_id]["location"]]

    if weapons_data[weapon]["control"] == "on":
        target = data[chat_id]["target"]
        target_index = enemies[target]["count"] - 1
    elif weapons_data[weapon]["control"] == "off":
        target = choice([key for key in enemies.keys() if enemies[key]["count"] != 0])
        target_index = randint(0,enemies[target]["count"] - 1)

    hp = units_data[target]["hp"]
    armor = units_data[target]["armor"][["physical","magic","fire"].index(weapons_data[weapon]["type"])]
    if "-" in armor:
        armor = armor.split("-")
        armor = randint(int(armor[0]),int(armor[1]))
    else:
        armor = int(armor)
    damage = weapons_data[weapon]["damage"]
    if "-" in damage:
        damage = damage.split("-")
        damage = randint(int(damage[0]),int(damage[1]))
    else:
        damage = int(damage)
    if target_index < enemies[target]["count"] - len(enemies[target]["hp"]):
        target_hp = hp - (damage - armor)
        if target_hp > 0:
            id = bot.send_message(chat_id,"{} ranen by {} ({} / {})".format(target, weapon, target_hp, units_data[target]["hp"])).message_id
            add_delete_message(chat_id, id)

            enemies[target]["hp"].insert(0,target_hp)
        else:
            kill(chat_id,weapon,target,enemies,mode)
            check_effects(chat_id,weapon,target,"post kill",mode,-target_hp)
    else:
        target_index = enemies[target]["count"] - target_index - 1
        enemies[target]["hp"][target_index] -= (damage - armor)
        if enemies[target]["hp"][target_index] <= 0:
            kill(chat_id, weapon, target, enemies, mode)
            target_hp = -enemies[target]["hp"][target_index]
            enemies[target]["hp"].pop(target_index)

            check_effects(chat_id,weapon,target,"post kill",mode,target_hp)
        else:
            id = bot.send_message(chat_id,"{} ranen by {} ({} / {})".format(target, weapon, enemies[target]["hp"][target_index], units_data[target]["hp"])).message_id
            add_delete_message(chat_id, id)

    print(enemies)
    if enemies[target]["count"] <= 0:
        enemies.pop(target)


def check_effects(chat_id,weapon,target,clss,mode = "player", stock_dmg = False):
    if clss == "post kill":
        if "full damage" in weapons_data[weapon]["effects"] and stock_dmg > 0:
            weapons_data["splinter"] = {
            "place":"0",
            "damage":str(stock_dmg),
            "type":weapons_data[weapon]["type"],
            "control":weapons_data[weapon]["control"],
            "effects":weapons_data[weapon]["effects"]
            }
            print(weapons_data["splinter"])
            if check_after_shot(chat_id,mode) == False:
                return
            one_shot(chat_id,"splinter",mode)


def kill(chat_id, weapon, target, enemies, mode = "player"):
    text = "{} 🤯killed by {}".format(target, weapon)
    if mode == "player":
        coins = data[chat_id]["enemies"][target]["coins"]
        data[chat_id]["coins"] += coins
        text += "  (+{}$  now {})".format(coins, data[chat_id]["coins"])
    id = bot.send_message(chat_id, text).message_id
    add_delete_message(chat_id, id)
    enemies[target]["count"] -= 1


def wave_start(chat_id):
    data[chat_id]["attack points"] = {}
    location = data[chat_id]["location"]
    for unit in data[chat_id]["armament"]["active"][location]:
        if any(["first blood" in weapons_data[weapon]["effects"] for weapon in units_data[unit]["weapons"]]):
            data[chat_id]["attack points"][unit] = data[chat_id]["armament"]["active"][location][unit]["count"]

    wave_menu(chat_id)


def wave_func(chat_id):
    data[chat_id]["attack points"] = {}
    location = data[chat_id]["location"]
    for unit in data[chat_id]["armament"]["active"][location]:
        data[chat_id]["attack points"][unit] = data[chat_id]["armament"]["active"][location][unit]["count"]

    wave_menu(chat_id)


def wave_menu(chat_id):
    text = "Your enemies 😡 :\n"
    for enemy in data[chat_id]["enemies"]:
        text += "{} : {}    💚 {} / {}     🛡 {}\n".format(enemy, data[chat_id]["enemies"][enemy]["count"],";".join([str(hp) for hp in data[chat_id]["enemies"][enemy]["hp"]]),
        units_data[enemy]["hp"], ";".join(units_data[enemy]["armor"]))


    add_delete_message(chat_id,     bot.send_message(chat_id, text).message_id)

    keyboard = types.InlineKeyboardMarkup()
    location = data[chat_id]["location"]
    for unit in data[chat_id]["attack points"]:
        text = "{} x{}".format(unit, data[chat_id]["attack points"][unit])
        if data[chat_id]["armament"]["active"][location][unit]["hp"] != []:
            text += "    💚 "
            for hp in data[chat_id]["armament"]["active"][location][unit]["hp"]:
                text += " {};".format(hp)
            text = text[:-1] + " / " + str(units_data[unit]["hp"])
        min_dmg = sum([int(units_data[unit]["weapons"][weapon]*(weapons_data[weapon]["damage"].split("-")[0])) for weapon in units_data[unit]["weapons"]])
        max_dmg = sum([int(units_data[unit]["weapons"][weapon] * (weapons_data[weapon]["damage"].split("-")[-1])) for weapon in units_data[unit]["weapons"]])
        text += "   {} - {}⚔".format(min_dmg, max_dmg)
        keyboard.add(types.InlineKeyboardButton(text, callback_data=unit))
    keyboard.add(types.InlineKeyboardButton("cancel", callback_data="cancel"))
    data[chat_id]["action"] = "wave - pick armament"
    bot.send_message(chat_id, "Pick armament for destroy:", reply_markup=keyboard)


def menu(id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.row(
        types.InlineKeyboardButton("🤜Fight wave {} . {}".format(data[id]["lvl"],data[id]["wave"]), callback_data = "WAVE"),
        types.InlineKeyboardButton("👁Watch map", callback_data = "MAP")
    )
    keyboard.row(
        types.InlineKeyboardButton("🙄Set armament".format(data[id]["lvl"], data[id]["wave"]),
                                   callback_data="SET ARMAMENT"),
    )
    text = "Mr👁️‍🗨️ --={}=--\n".format(data[id]["name"])
    for key in data[id]:
        if key == "":
            pass
        elif key != 'name':
            if type(data[id][key]) == dict:
                text += "\n---- {}:\n".format(key)
                for key1 in data[id][key]:
                    if key1 == "active":
                        text += "-- active:\n"
                        location = data[id]["location"]
                        for unit in data[id]["armament"]["active"][location]:
                            text += "     {} - {}".format(unit, data[id]["armament"]["active"][location][unit]["count"])
                            if data[id]["armament"]["active"][location][unit]["hp"] != []:
                                text += "    💚 "
                                for hp in data[id]["armament"]["active"][location][unit]["hp"]:
                                    text += " {};".format(hp)
                                text = text[:-1] + " / " + str(units_data[unit]["hp"]) + "\n"
                            else:
                                text += "\n"
                    else:
                        if type(data[id][key][key1]) == dict:
                            text += "-- {}:\n".format(key1)
                            for key2 in data[id][key][key1]:
                                text += "      {} - {}\n".format(key2, data[id][key][key1][key2])
                        else:
                            text += "{} - {}\n".format(key1, data[id][key][key1])
            else:
                if key == "coins":
                    text += "\n💰{} - {}\n".format(key, data[id][key])
                else:
                    text += "\n{} - {}\n".format(key, data[id][key])
    data[id]["action"] = "Pick menu: Wave, Map, Set"
    bot.send_message(id, text=text,
    reply_markup = keyboard)


bot.polling(none_stop=True)
