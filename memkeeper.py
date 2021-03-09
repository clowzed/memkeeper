import aiogram

from handlers import *
from misc     import dispatcher, sending_emails_delay

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_later(sending_emails_delay, repeat_sending_emails, send_emails, loop)
    aiogram.executor.start_polling(dispatcher, skip_updates = False)
