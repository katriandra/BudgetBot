import json
from bot import bot

def load_json():
    try:
        with open('DB.json','r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        data = {}
        dump_json(data)
        return load_json()
def dump_json(data):
    with open('DB.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def Check_DB(call):
    try:
        data = load_json()
        return data[str(call.from_user.id)]['idsheets']
    except KeyError:
        bot.send_photo(call.from_user.id, 'https://i.ibb.co/SBy7JDN/imgonline-com-ua-2to1-aqf-VQIOs-QVre-Djfh.png',"Вас нет в базе данных.\nДля того, чтобы воспользоваться ботом, сделайте две вещи:\n1.Откройте доступ к таблице по этому аккаунту `acc-637@python-351705.iam.gserviceaccount.com`\n2.Скопируйте id документа и отправте сюда с меткой ID",parse_mode='Markdown')

def check_user(message):
    data = load_json()
    try:
        data[str(message.from_user.id)]['Доходы']
    except:
        data.update({str(message.from_user.id):{'Доходы':{'Добавить статью доходов': False},'Расходы':{'Добавить статью расходов':False},"idsheets":""}})
        dump_json(data)
