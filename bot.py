import telebot
from telebot import types

bot = telebot.TeleBot("1814312326:AAHGhtyj8WD9tYKe9F8h9tJyQwpLWyUbpt0")
global mas
mas = []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stic = open('sticker1.webp', 'rb')
    bot.send_sticker(message.chat.id, stic)
    bot.send_message(message.chat.id,
                     'Ну привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>. ' \
                     'С моей помощью Вы сможете узнать тип своего телосложения, а также параметры своего тела.'.format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)
    bot.send_message(message.from_user.id, 'Сколько Вам лет?')
    bot.register_next_step_handler(message, get_Age)


def get_Age(message):
    global Age
    Age = message.text
    if is_digit(Age) is True and Age[0] is not '-':
        mas.append(float(Age))
        bot.send_message(message.from_user.id, 'Ваш рост в см?')
        bot.register_next_step_handler(message, get_Height)
    else:
        wrong(message)
        bot.register_next_step_handler(message, get_Age)


def get_Height(message):
    global Height
    Height = message.text
    if is_digit(Height) is True and Height[0] is not '-':
        mas.append(float(Height))
        bot.send_message(message.from_user.id, 'Ваш вес в кг?')
        bot.register_next_step_handler(message, get_Weight)
    else:
        wrong(message)
        bot.register_next_step_handler(message, get_Height)


def get_Weight(message):
    global Weight
    Weight = message.text
    if is_digit(Weight) is True and Weight[0] is not '-':
        mas.append(float(Weight))
        bot.send_message(message.from_user.id, 'Ваш обхват грудной клетки в см?')
        bot.register_next_step_handler(message, get_Girth)
    else:
        wrong(message)
        bot.register_next_step_handler(message, get_Weight)


def get_Girth(message):
    global Girth
    Girth = message.text
    if is_digit(Girth) is True and Girth[0] is not '-':
        mas.append(float(Girth))
        bot.send_message(message.from_user.id, '💪 Ваше телосложение по индексу Пинье:\n')
        bot.send_message(message.from_user.id, ans_Pin(mas[1], mas[2], mas[3]))
        bot.send_message(message.from_user.id, '💪 Ваши параметры по индексу Кетле:\n')
        bot.send_message(message.from_user.id, ans_Ket(mas[1], mas[2]))
        goodbye(message)
    else:
        wrong(message)
        bot.register_next_step_handler(message, get_Girth)


def wrong(message):
    bot.send_message(message.from_user.id, 'Введите целое или дробное число!\n\n Например "23" или "181.5"')
    stic = open('angry.webp', 'rb')
    bot.send_sticker(message.chat.id, stic)


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def ans_Pin(a, b, c):
    res = a - (b + c)
    if res < 10:
        return 'Вы - эндоморф.\n\n Имеете гиперстетическое телосложение. \n\n Возможен избыточный вес.'
    elif 10 <= res < 30:
        return 'Вы - мезоморф.\n\n Имеете нормостетическое телосложение.\n\n Такое телосложение является нормальным.'
    elif res > 30:
        return 'Вы - эктоморф.\n\n Имеете гипостетическое телосложение. \n\n Возможна худощавость.'


def ans_Ket(a, b):
    res = b / ((a / 100) ** 2)
    if res < 18.5:
        return 'У Вас дефицит массы тела!\n\n Низкий риск ожирения, ' \
               'зато для остальных заболеваний Вы легкая мишень!\n\n Желатиельно проконсультироваться со специалистом.'
    elif 18.5 <= res < 24.9:
        return 'Поздравляю, у Вас нормальная масса тела!' \
               '\n\n Также Вы не входите в группу людей с повышенным риском ожирения.'
    elif 24.9 <= res < 29.9:
        return 'У Вас избыточная масса тела!\n\n Повышенный риск ожирения. ' \
               '\n\n Желательно проконсультироваться с диетологом.'
    elif 29.9 <= res < 34.9:
        return 'У Вас ожирение 1 степени!\n\n Высокий риск дальнейшего ожирения ' \
               'и других сопутствующих болезней. \n\n Желательно проконсультироваться с диетологом.'
    elif 34.9 <= res < 40:
        return 'У Вас ожирение 2 степени!\n\n Очень высокий риск дальнейшего ожирения ' \
               'и других сопутствующих болезней. \n\n Желательно проконсультироваться с диетологом.'
    elif res >= 40:
        return 'У Вас ожирение 3 степени!\n\n Чрезвычайно высокий риск дальнейшего ожирения ' \
               'и других сопутствующих болезней. \n\n Обязательно проконсультируйтесь с диетологом.'


def goodbye(msg):
    mas.clear()
    bot.send_message(msg.from_user.id,
                     'Надеюсь был полезен! \n\n Также если вы считаете, что я что-то вывожу неправильно, перезапустите меня❤️'
                     '\n\n Если снова понадоблюсь, напишите /start')
    stic = open('bye.webp', 'rb')
    bot.send_sticker(msg.chat.id, stic)


bot.polling()