# First Pybot development attemp mixing commands, echobot and other tutorials

import os
import sys
# logging allows to see what the bot is doing in the console
import logging
# Constants allow me to use the token in a safe environmente but we I could also use a enviroment variable
# import CompaConstants as keys  
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import CompaResponses as R

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# here create a enviroment variable to avoid sharing the token
#TOKEN = os.getenv("TOKEN")
#use pipenv shell in the console to create the file, get a Pipfile
#to create the variable go to a new terminal a type "set TOKEN=(paste botdad token)"
#print(TOKEN) to verify is the correct number

# Def is use to define the function to be executed when the commands / are send.
# Define la función que se va a ejecutar cuando entra el comando start
def start(update, context):
    bot = context.bot
    userName = update.effective_user["first_name"]
    update.message.reply_text(f"Hola {userName}, cómo va compa (UwU)")

def cancel(update, context):
    update.message.reply_text("Vemos neas (°-°).|.")
# the logger info is very important to keep track of what the users ask to the bot
def getBotInfo(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f'El Usuario {userName} ha solicitado información sobre el Bot')
    bot.sendMessage(
        chat_id=chatId, 
        parse_mode="HTML",
        text=f'Hola soy un Bot creado para el <b>grupo de programación de MYEF Telegram</b>'
    )
# Previous parse_mode its use to add Format to the text, such as Bold, Italic, 

# welcome message command
def welcomeMsg(update, context):
    bot = context.bot
    chatId = update.message.chat_id 
    updateMsg = getattr(update, "message", None)
    for user in updateMsg.new_chat_members:
        userName = user.first_name
    # logger to get notify that a new user enter the group 
    logger.info(f'El usuario {userName} ha ingresado al grupo')
    
    bot.sendMessage(
        chat_id = chatId,
        parse_mode='HTML',
        text=f'<b>Bienvenido al grupo {userName}</b> \nCreí que no serías capaz de resolver el chaptcha :u'
    )

# goodbye message command no esta funcionando
def byeMsg(update, context):
    bot = context.bot
    chatId = update.message.chat_id 
    updateMsg = getattr(update, "message", None) #obtain message info, can be use for several things
    for user in updateMsg.left_chat_member:
        userName = user.first_name
    # logger to get notify that a new user enter the group 
    logger.info(f'El usuario {userName} ha dejado el grupo')
    
    bot.sendMessage(
        chat_id = chatId,
        parse_mode='HTML',
        text=f'<b>Adiós {userName}</b> \nNadie te va a extrañar'
    )
    
# message deletion based on word filtering control creates conflict with responses

def deleteMessage(bot, chatId, messageId, userName):
    try:
        bot.delete_message(chatId, messageId)
      #  logger.info(f'El mensaje de {userName} se eliminó porque contenía una palabra de la lista')
    except Exception as e:
        print(e)

def control(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    updateMsg = getattr(update, "message", None) #be creative, use this to do this with the message
    messageId = updateMsg.message_id
    userName = update.effective_user["first_name"]
    text = update.message.text #register in the logger the text sent by user
   # logger.info(f'El usuario {userName} ha enviando un nuevo mensaje al grupo {chatId}')
 # for each text split para palabras compuestas como que gonorrea :v con boolean
    badWords = ["puta", "Viva Uribe", "gonorrea"]

    if text in badWords:
        deleteMessage(bot, chatId, messageId, userName)
        bot.sendMessage(
            chat_id=chatId,
            text=f'El mensaje de {userName} ha sido eliminado porque contenía una palabra prohíbida'
        )
    else:
        handle_message(update, context)
   #elif. can I use Elif to include something from a variable such as handle_message?
# Preset responses messages
# responses using else solves the issue


def handle_message(update, context):
    text_responses = str(update.message.text).lower()
    response = R.sample_responses(text_responses)

    update.message.reply_text(response)

def  error(update, context):
    print(f"Update {update} caused error {context.error}")

# Echo command from the echobot example on Github
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

# Simple answer to noncommand text (didn't work)
#def hola(update: Update, context: CallbackContext) -> None:
 #   """offers help."""
 #   update.message.reply_text("hola compita")

# Conversation example from github, its failing to show the Identidad Response

IDENTIDAD = range(1)


def Saludo(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [["bot", "humano", "otro"]]

    update.message.reply_text(
        'Hola! Mi nombre es CompaBot. Cómo sería?.'
        'Usa /detener para detenerme.\n\n'
        'Eres un Bot o Humano?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return IDENTIDAD

def Identidad(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Identidad de %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ya veo! Yo soy un bot programado en Python',
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END

def detener(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Usuario %s ha cancelado la conversación.", user.first_name)
    update.message.reply_text(
        'Adios! Hablaremos en otra ocasión.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

#Bloque de ejecución principal start the bot
if __name__ == "__main__":

# create a variable to obtain the bot info, requires the to previous EnvFunction
    #myBot = telegram.Bot(token = TOKEN)
   # print(myBot)

# Updater para saber las peticiones de los usuarios al bot (al mandar comandos, mensajes, botones, etc),
    updater = Updater(token="1618914785:AAFZ9NAzNs5jb9NG6woiFCGaxKAJz7bA1Es", use_context=True)

# the alternative to the above is the following
# updater = Updater(myBot.token, use_context=True)

# Dispatcher se encarga de enviar las acciones cuando entra algo por el updater, # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # add handler permite que el bot este escuchando, ciclo infinito para revisar si el usuario envia petición
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cancel", cancel))
    # command to obtain bot's info
    dp.add_handler(CommandHandler("botInfo", getBotInfo))
    # command to give welcome message
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeMsg))
    # command to give goodbye message
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, byeMsg))
    # message deletion
   # dp.add_handler(MessageHandler(Filters.text, control))

# Dispatcher for the Responses
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

# on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # answer to command /hola not working
    #dp.add_handler(MessageHandler(Filters.text & ~Filters.command, hola))

 # Add conversation handler with the states Identidad
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('saludo', Saludo)],
        states={
            Identidad: [MessageHandler(Filters.regex('^(bot|humano|otro)$'), Identidad)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

# Start the Bot
    updater.start_polling()
    updater.idle()




