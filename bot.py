import pandas
import telebot
from OOPparser import *

class KivanoBot:
    help_text = '''
    /categories - для просмотра всех категорий
    /product {название продукта} для просотра информации о данном товаре
    '''
    __data = pandas.read_csv('kivano.csv')
    ads_set = set(__data.category.to_list())
    product_set = set(__data.title)

    def show(self, args):
        if len(args) <= 0:
            return '\n'.join(self.ads_set).replace('category\n', '')
        else:
            ad = f"{args}"
            if ad not in self.ads_set:
                return f'Товара с названием {args} не существует'
            else:
                new_ad = self.__data[self.__data.category == ad]
                new_ad = new_ad[['title', 'link']][:10].to_string()
                return new_ad

    def show_product(self, text):
        if text not in self.product_set:
            return f'Продукта с названием {text} не существует'
        else:
            result = self.__data[self.__data.title == text]
            result = result[['title', 'category', 'link']].to_string()
            return result


TOKEN = '1899148636:AAF_8nCWM6disG84rsKEMplHrm-xLgLwRrY'

bot = telebot.TeleBot(TOKEN)
kbot = KivanoBot()


@bot.message_handler(commands=['start', 'help'])
def show(message):
    bot.send_message(message.chat.id, kbot.help_text)


@bot.message_handler(commands=['categories'])
def fractions(message):
    args = message.text[12:]
    bot.send_message(message.chat.id, kbot.show(args))


@bot.message_handler(commands=['product'])
def deputy(message):
    args = message.text[8:]
    bot.send_message(message.chat.id, kbot.show_product(args))


if __name__ == '__main__':
    bot.polling()