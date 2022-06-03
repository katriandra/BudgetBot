button_list=["Доходы", "Расходы", "Записать в гугл таблицы", "Запись из гугл таблиц", "Записать сумму", "Посмотреть сумму за все время"]
from keyboa import Keyboa
from db import *
from bot import *
from quickstart import *
buffer = {}

@bot.message_handler(commands=['start'])
def start_menu(message, caption = "Привет! Я тут слежу за твоими финансами и отправляю их в гугл таблицы!"):
    bot.delete_message(message.from_user.id, message.id)
    bot.send_message(message.from_user.id, caption, reply_markup=keyb_gen(button_list[:4]))
    check_user(message)
    buffer.update({message.from_user.id: {"step 1":"","step 2":""}})
@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    if call.data in dict_to_callback.keys():
        dict_to_callback[call.data](call)
    else:
        buffer[call.from_user.id]["step 2"] = call.data
        bot.send_message(call.from_user.id, "Что будем делать?",
                         reply_markup=keyb_gen(button_list[4:6]))

@bot.message_handler(content_types=['text'])
def check_answer(message):
    data = load_json()
    try:
        if "ID" in message.text:
            data[str(message.from_user.id)]['idsheets'] = message.text.replace("ID","")
            dump_json(data)
            start_menu(message, caption="Теперь вы в базе данных! Если хотите внести значения в таблицу, отправьте сообщение ЗАПИСЬ <расходы> <доходы>!")

        elif "ЗАПИСЬ" in message.text:
            load_to_spreadsheets(Check_DB(message),message.text.split())

        elif data[str(message.from_user.id)]['Расходы']['Добавить статью расходов']:
            data[str(message.from_user.id)]['Расходы']['Добавить статью расходов'] = False
            data[str(message.from_user.id)]['Расходы'][message.text.upper()] = {"edit": False, "amount": 0}
            dump_json(data)
            start_menu(message,caption="Статья расходов успешно добавлена")

        elif data[str(message.from_user.id)]['Доходы']['Добавить статью доходов']:
            data[str(message.from_user.id)]['Доходы']['Добавить статью доходов'] = False
            data[str(message.from_user.id)]['Доходы'][message.text.upper()] = {"edit": False, "amount": 0}
            dump_json(data)
            start_menu(message,caption="Статья доходов успешно добавлена")

        elif data[str(message.from_user.id)][buffer[message.from_user.id]["step 1"]][buffer[message.from_user.id]["step 2"]]["edit"]:
            data[str(message.from_user.id)][buffer[message.from_user.id]["step 1"]][buffer[message.from_user.id]["step 2"]]["edit"] = False
            data[str(message.from_user.id)][buffer[message.from_user.id]["step 1"]][buffer[message.from_user.id]["step 2"]]["amount"] = message.text
            dump_json(data)
            start_menu(message,caption="Сумма записана!")
    except:
        pass
def Income(call):
    buffer[call.from_user.id]["step 1"] = call.data
    data = load_json()
    bot.edit_message_text("Добавь свою статью доходов",call.from_user.id, call.message.id,
                     reply_markup=keyb_gen([key for key,value in data[str(call.from_user.id)]['Доходы'].items()]))

def Expenses(call):
    buffer.update({call.from_user.id: {"step 1": call.data}})
    data = load_json()
    bot.edit_message_text("Добавь свою статью расходов",call.from_user.id, call.message.id,
                     reply_markup=keyb_gen([key for key,value in data[str(call.from_user.id)]['Расходы'].items()]))

def AddExpenses(call):
    bot.edit_message_text("Напиши сюда какую статью расходов хочешь добавить",call.from_user.id, call.message.id)
    data = load_json()
    data[str(call.from_user.id)]['Расходы']['Добавить статью расходов'] = True
    dump_json(data)

def AddIncome(call):
    bot.edit_message_text("Напиши сюда какую статью доходов хочешь добавить",call.from_user.id, call.message.id)
    data = load_json()
    data[str(call.from_user.id)]['Доходы']['Добавить статью доходов'] = True
    dump_json(data)

def AddAmount(call):
    data = load_json()
    data[str(call.from_user.id)][buffer[call.from_user.id]["step 1"]][buffer[call.from_user.id]["step 2"]]["edit"] = True
    dump_json(data)
    bot.edit_message_text("Напиши сюда сумму", call.from_user.id, call.message.id)

def FALamount(call):
    data = load_json()
    amount = data[str(call.from_user.id)][buffer[call.from_user.id]["step 1"]][buffer[call.from_user.id]["step 2"]]["amount"]
    bot.edit_message_text(f"Вы потратили/заработали по статье *{buffer[call.from_user.id]['step 2'].upper()} {amount}* рублей",call.from_user.id, call.message.id,parse_mode="Markdown")

def WriteSheets(call):
    Check_DB(call)
    bot.edit_message_text("Если хотите внести значения в таблицу, отправьте сообщение ЗАПИСЬ <расходы> <доходы>!",call.from_user.id, call.message.id, parse_mode="Markdown")
def History(call):
    Check_DB(call)
    bot.edit_message_text('\n'.join(" ".join(i) for i in get_from_spreadsheets(Check_DB(call))['values'] if i != []),call.from_user.id, call.message.id)

dict_to_callback={'Доходы':Income,'Расходы':Expenses,'Запись из гугл таблиц': History, "Добавить статью расходов": AddExpenses, "Добавить статью доходов": AddIncome,"Записать сумму": AddAmount, "Посмотреть сумму за все время":FALamount,"Записать в гугл таблицы": WriteSheets}

def keyb_gen(button_list):
    keyboard = Keyboa(items=button_list, copy_text_to_callback=True, items_in_row=2)
    return keyboard()
bot.infinity_polling()