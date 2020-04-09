# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:01:04 2020

@author: pepeb
"""


# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:58:22 2020

@author: pepeb
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
 
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from DataFunction import *
import numpy as np
import io
import requests
import pandas as pd
try:
    import databaseconfig as cfg
except:
        try:
            import sampleconfig as cfg
        except:
            print('\n I need a config file with the token information \n')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Oli, soy el coronabot. Tengo los datos de fallecidos y contagiados por'+
    ' comunidad de españa y simplemente me tienes que decir que quieres visualizar. Para entendernos ' +
    'necesitaria que me dijeras si quieres los datos diarios/totales, muertos/contagiados y para que comunidad/comunidades '+
    'te gustaria visualizarlo. Me da igual el orden y si hay palabras de por medio. Un ejemplo: \n '+
    'Por favor, me das la cifra diaria de muertos en madrid, aragon y cataluña?')
    
    
  
         
def HereIam(update, context):
    """Send a message when the command /start is issued."""
    update.send_photo(photo=open('Ploteo.png', 'rb'))

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    
    
   
    
    
    txt = update.message.text


    
 
    if (tipo(txt)) and (diarioortotal(txt)) and comunidad(txt):

        ploteame(tipo(txt), comunidad(txt), diarioortotal(txt))
      
        pic = "Ploteo.png"
        context.bot.send_photo(update.message.chat.id , open(pic,'rb'))
    else:
        update.message.reply_text('No te he entendido') 
        logger.info('My Application is launched', extra={'bot': True})
    
        

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(cfg.mysql['token'], use_context=True)

    
    
    
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("test", HereIam))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()