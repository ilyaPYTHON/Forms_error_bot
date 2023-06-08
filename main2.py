import telebot
from telebot import * 
from bs4 import BeautifulSoup as bs
import threading, requests
import phonenumbers
from phonenumbers import geocoder, carrier
import requests
import time

ID = '6069852039'
#osnova 6263167061:AAEzI8sRYcSXGGS6zywkU2wBjgoUPpx-XjI
#test 5815802755:AAHsvfyMba2S4qrU2KvpWJRU4wLD-B_Ym0g
bot = TeleBot('6263167061:AAEzI8sRYcSXGGS6zywkU2wBjgoUPpx-XjI')

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=False, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Надіслати нікнейм')
    itembtn2 = types.KeyboardButton('👨🏻‍💻Пошук по IP👨🏻‍💻')
    itembtn3 = types.KeyboardButton('Пошук по user ID')
    itembtn4 = types.KeyboardButton('☎️Пошук по номеру телефону☎️')
    itembtn5 = types.KeyboardButton('Пошук по ІПН')
    itembtn6 = types.KeyboardButton('🟢Чек онлайн🟢')
    keyboard.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    bot.send_message(message.chat.id, '''👋 Привіт! 👋
        Це бот для боротьби з російсько-пропагандитськими аккаунтами в TikTok і не тільки)''', reply_markup=keyboard)
    bot.register_next_step_handler(message, buttonhandler)

@bot.message_handler(content_types='text')
def buttonhandler(message):
    if message.text == 'Надіслати нікнейм':
        bot.send_message(message.chat.id, 'Введіть нікнейм: \n Застереження! Приймаються лише аккаунти на яких є відео з лицем автора аккаунта') 
        bot.register_next_step_handler(message, step1)
    elif message.text == '👨🏻‍💻Пошук по IP👨🏻‍💻':
        bot.send_message(message.chat.id, 'Введіть IP за яким бажаєте почати пошук:') 
        bot.register_next_step_handler(message, step2)
    elif message.text == 'Пошук по user ID':
        bot.send_message(message.chat.id, 'Введіть ID юзера і ви отримаєте посилання на його аккаунт') 
        bot.register_next_step_handler(message, step3)
    elif message.text == '☎️Пошук по номеру телефону☎️':
        bot.send_message(message.chat.id, 'Надішліть номер телефону за яким бажаєте почати пошук \nPs: введіть у форматі +38000000000')
        bot.register_next_step_handler(message, step4) 
    elif message.text == 'Пошук по ІПН':
        bot.send_message(message.chat.id, 'Надішліть ІПН за яким ви бажаєте почати пошук \n ВАЖЛИВО! Вписуйте число без відступів!')
        bot.register_next_step_handler(message, step5)
    elif message.text == '🟢Чек онлайн🟢':
        bot.send_message(message.chat.id, 'Працюю))))')
    else: 
        bot.send_message(message.id, "Помилка!")
  
def step1(message):
    id_user = f"```\n{message.from_user.id}\n```"
    nickname = f"```\n{message.text}\n```"
    get = (f'Отримані данні:' + '\nID: ' + id_user + '\nНік: ' + nickname)
    bot.send_message(ID, get, parse_mode='Markdown')
    bot.reply_to(message, f'Дякую за допомогу на кіберфронті України😉!')
  
def step2(message):
        ip = message.text
        res = requests.get('https://ipinfo.io/' + ip + '/json')
        r = res.json()
        if 'country' in r:
            country2 = ('\n[Країна] : ' + r['country']) 
        else:
            country2 = '\n[Країна] : невідомо'
        if 'region' in r:
            region2 = ('\n[Регіон] : ' + r['region'])
        else:
            region2 = '\n[Регіон] : невідомо'
        if 'city' in r:
            city2 = ('\n[Місто] : ' + r['city'])
        else:
            city2 = '\n[Місто] : невідомо'
        if 'loc' in r:
            loc2 = ('\n[Місцезнаходження] : ' + r['loc'])
        else:
            loc2 = '\n[Місцезнаходження] : невідомо'
        if 'org' in r:
            org2 = ('\n[Провайдер] : ' + r['org'])
        else:
            org2 = '\n[Провайдер] : невідомо'
        if 'timezone' in r:
            timezone2 = ('\n[Часовий пояс] : ' + r['timezone'])
        else:
            timezone2 = '\n[Часовий пояс] : невідомо'
        if 'postal' in r:
            postal2 = ('\n[Почтовий індекс] : ' + r['postal'])
        else:
            postal2 = '\n[Почтовий індекс] : невідомо'
            info = country2 + region2 + city2 + loc2 + org2 + timezone2 + postal2
            bot.reply_to(message, info)
            
def step3(message):
    user_id = message.text
    final_id = ("tg://openmessage?user_id=" + user_id)
    bot.reply_to(message, final_id)
  
def step4(message):
    phone_number = message.text
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        country = geocoder.description_for_number(parsed_number, 'en')
        service_provider = carrier.name_for_number(parsed_number, 'en')
        information1_number = ('[Country] : ' + country)
        information2_number = ('\n[Service provider] : ' + service_provider)
        information3_number = ('\n Viber: ' + 'msng.link/o?' + phone_number + '=vi')
        information4_number = ('\n Telegram: ' + 't.me/' + phone_number)
        information5_number = ('\n Whatsapp: ' + 'msng.link/o?' + phone_number + '=wa')
        information_social_number = information3_number + information4_number + information5_number
        information_global_number = information1_number + information2_number 
        information_number = information_global_number + information_social_number
        bot.reply_to(message, information_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        bot.reply_to(message,'Номер не вірний')

def step5(message):
    ipn_number = message.text
    k = len(ipn_number)
    k_number = 10
    if k == k_number:
        ipn_url = 'https://deltasoft.dp.ua/service/inn/?inn=' + ipn_number
        headers = {
            'headers':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        res = requests.post(ipn_url, headers=headers)
        soup = bs(res.text, "html.parser")
        vacancies_names = soup.find_all('p',class_='person')
        for name in vacancies_names:
            bot.send_message(message.chat.id, name.text.strip())
    else:
        bot.send_message(message.chat.id, 'Помилка')


bot.infinity_polling()