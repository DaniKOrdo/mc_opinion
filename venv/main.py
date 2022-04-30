from ast import arguments
from operator import truediv
import time
import logging
import telegram
import dk_token as dk
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from telegram import Bot, Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TELEGRAM_BOT_TOKEN = dk.TOKEN
TELEGRAM_CHAT_ID = dk.CHAT_ID
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

#TODO Poner tambien la hora y minutos para que no se sobreescriban
# dd/mm/YY
today = date.today()
actual_date = today.strftime("%d-%m-%Y")

# Selenium config
driver_options = Options()
#driver_options.add_argument('--headless')
# 375 667
driver_options.add_argument('--no-sandbox')
driver_options.add_argument("--incognito")
driver_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
#driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=driver_options)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
driver.get('https://mcdonalds.fast-insight.com/voc/es/es')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Command handlers
# Start
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

# Bot Check
def bot_check(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot ✅')

# Get id 
def get_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.chat_id)

# Captura de pantalla
def captura(update: Update, context: CallbackContext) -> None:
    PHOTO_PATH = './venv/img/screenshot' + actual_date + '.png'
    driver.save_screenshot(PHOTO_PATH)
    time.sleep(2)
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(PHOTO_PATH, 'rb'))

# Generar ticket
def ticket(update: Update, context: CallbackContext) -> None:
    """Get ticket and write"""
    num_ticket = update.message.text.split(' ')[1]
    # update.message.reply_text(num_ticket)
    get_id = driver.find_element('id', 'receiptCode')
    slow_typing(get_id, num_ticket)

    time.sleep(1)

    submit = driver.find_element('xpath', '//*[@id="welcomeMessage"]/div[4]/button')
    submit.click()

    time.sleep(2)

    driver.get(driver.current_url)


    # Questions
    question_1 = driver.find_element('xpath', '//*[@id="0"]/div[5]/div[1]')
    question_1.click()

    question_2 = driver.find_element('xpath', '//*[@id="8"]/div[5]/div[1]')
    question_2.click()
    
    question_3 = driver.find_element('xpath', '//*[@id="10"]/div[5]/div[1]')
    question_3.click()

    # Scroll 1

    question_4 = driver.find_element('xpath', '//*[@id="12"]/div[5]/div[1]')
    question_4.click()

    actions = ActionChains(driver)
    actions.move_to_element(question_4).perform()
    
    question_5 = driver.find_element('xpath', '//*[@id="47"]/div[5]/div[1]')
    question_5.click()

    actions = ActionChains(driver)
    actions.move_to_element(question_5).perform()
    
    question_6 = driver.find_element('xpath', '//*[@id="55"]/div[5]/div[1]')
    question_6.click()
    
    question_7 = driver.find_element('xpath', '//*[@id="14"]/div[5]/div[1]')
    question_7.click()
    
    question_8 = driver.find_element('xpath', '//*[@id="6"]/div[5]/div[1]')
    question_8.click()
    
    question_9 = driver.find_element('xpath', '//*[@id="94"]/div[5]/div[1]')
    question_9.click()
    
    question_10 = driver.find_element('xpath', '//*[@id="85"]/div[5]/div[2]')
    question_10.click()
    
    question_11 = driver.find_element('xpath', '//*[@id="35"]/div[5]/div[1]')
    question_11.click()
    
    question_12 = driver.find_element('xpath', '//*[@id="22"]/div[5]/div[2]')
    question_12.click()
    
    question_13 = driver.find_element('xpath', '//*[@id="23"]/div[5]/div[2]')
    question_13.click()
    
    question_14 = driver.find_element('xpath', '//*[@id="24"]/div[5]/div[4]')
    question_14.click()
    
    question_15 = driver.find_element('xpath', '//*[@id="48"]/div[5]/div[2]')
    question_15.click()
    
    question_16 = driver.find_element('xpath', '//*[@id="50"]/div[5]/div[2]')
    question_16.click()

    time.sleep(2)
    
    

# Escritura del bot mas lenta
def slow_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(0.1)

# Reiniciar chrome
def reset_chrome(pdate: Update, context: CallbackContext) -> None:
    driver.close
    time.sleep(1)
    driver.get('https://mcdonalds.fast-insight.com/voc/es/es')



# Recursos
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
    dispatcher.add_handler(CommandHandler("bot", bot_check))
    dispatcher.add_handler(CommandHandler("captura", captura))
    dispatcher.add_handler(CommandHandler("getid", get_id))
    dispatcher.add_handler(CommandHandler("ticket", ticket))
    dispatcher.add_handler(CommandHandler("reset", reset_chrome))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()