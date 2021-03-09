import json
import pathlib
import aiogram
import configparser
import logging
import emailsender
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.files   import JSONStorage

confparser:configparser.ConfigParser = configparser.ConfigParser()
confparser.read('config.ini')

bot_token = confparser['credentials']['bot_token']

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)


logging_middleware                               = LoggingMiddleware()
bot               :aiogram.Bot                   = aiogram.Bot(token = bot_token)

json_storage_path = pathlib.Path('./states/users_states.json')
if not json_storage_path.exists():
    json.dump(dict(empty = "empty"), open(json_storage_path, 'w'))

dispatcher        :aiogram.dispatcher.Dispatcher = aiogram.dispatcher.Dispatcher(bot     = bot,
                                                                                 storage = JSONStorage(json_storage_path))
dispatcher.middleware.setup(logging_middleware)

granted_mobile_phones = confparser['access']['granted_mobile_phones'].split(',')
granted_mobile_phones = list(map(lambda phone: phone.strip(), granted_mobile_phones))

mail_login    = confparser['mail']['from_email']
mail_password = confparser['mail']['from_email_password']
to_email      = confparser['mail']['to_email']
emails_sender = emailsender.EmailSender(mail_login, mail_password)

# You can send max 100 emails per day
# This dalay was calculated to prevent errors
sending_emails_delay = 24 * 60 * 60 / 95