import time
import logging
import telegram
import dk_token as dk
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from telegram import Bot, Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_BOT_TOKEN = dk.TOKEN
TELEGRAM_CHAT_ID = dk.CHAT_ID
PHOTO_PATH = './venv/img/screenshot.png'

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


# Selenium config
driver_options = Options()
driver_options.add_argument('--headless')
driver_options.add_argument('--no-sandbox')
#driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=driver_options)
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://mcdonalds.fast-insight.com/voc/es/es')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Command handlers
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def captura(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    driver.save_screenshot("./venv/img/screenshot.png")
    time.sleep(2)
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(PHOTO_PATH, 'rb'))

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def get_id(update: Update, context: CallbackContext) -> None:
    """Get id"""
    update.message.reply_text(update.message.chat_id)

def ticket(update: Update, context: CallbackContext) -> None:
    """Get ticket and write"""
    num_ticket = update.message.text.split(' ')[1]
    # update.message.reply_text(num_ticket)
    get_id = driver.find_element_by_id('receiptCode')
    slow_typing(get_id, num_ticket)

    time.sleep(1)

    submit = driver.find_element_by_xpath('//*[@id="welcomeMessage"]/div[4]/button')
    submit.click()
    

def slow_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(0.1)

def ticket_code():
    ci = driver.find_element_by_id('receiptCode')
    slow_typing(ci, 'CCJHCQ-RMMZCQ-C7CKC9')


def reset():
    driver.close
    time.sleep(1)
    driver.get('https://mcdonalds.fast-insight.com/voc/es/es')




def ci():
    ci = driver.find_element_by_id('numberCID')
    slow_typing(ci, 'ci_number')

def db():
    daybirth = driver.find_element_by_name('dateBirth[day]')
    slow_typing(daybirth, 'xx')

def mb():
    monthbirth = Select(driver.find_element_by_id('mes'))
    monthbirth_selected = monthbirth.select_by_visible_text("noviembre")

def yb():
    daybirth = driver.find_element_by_name('dateBirth[year]')
    slow_typing(daybirth, 'xxxx')

def sb():
    submit = driver.find_element_by_id('btnCheckData')
    submit.click()
    



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(dk.TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("captura", captura))
    dispatcher.add_handler(CommandHandler("getid", get_id))
    dispatcher.add_handler(CommandHandler("ticket", ticket))
    dispatcher.add_handler(CommandHandler("reset", reset))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

