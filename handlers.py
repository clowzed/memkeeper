import asyncio
import datetime
import pathlib
from   pprint import pprint

import aiogram
import peewee

from messages import errors      as errors_messages
from messages import prompts     as prompts_messages
from messages import information as information_messages

from misc import (bot,
                  to_email,
                  mail_login,
                  dispatcher,
                  emails_sender,
                  mail_password,
                  sending_emails_delay,
                  granted_mobile_phones)

from states.users_states import users_states
from storages.databases  import (media_group_files,
                                 no_caption,
                                 no_mobile_phone,
                                 users)


def handle_user(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    if not users.select().where(users.chat_id == message.chat.id).exists():
        new_user = users.create(id      = users.unique_id(),
                                chat_id = message.chat.id)
        new_user.save()
        return new_user
    else:
        return users.get(users.chat_id == message.chat.id)

def strip_mobile_phone(mobile_phone):
    return "".join([str(num) for num in mobile_phone if num.isdigit()])

def check_access_by_mobile_phone(message):
    if message.contact:
        mobile_phone = message.contact.phone_number
        mobile_phone = strip_mobile_phone(mobile_phone)
        return mobile_phone in granted_mobile_phones and message.contact.user_id == message.from_user.id
    else:
        user = handle_user(message, None)
        mobile_phone = user.mobile_phone
        mobile_phone = strip_mobile_phone(mobile_phone)
        return mobile_phone in granted_mobile_phones

async def return_to_homepage(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    await state.finish()
    await state.set_state(users_states.homepage)
    user = handle_user(message, state)
    if user.mobile_phone == no_mobile_phone or not check_access_by_mobile_phone(message):
        keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1, one_time_keyboard = True)
        keyboard.add(aiogram.types.KeyboardButton(prompts_messages.ask_mobile_phone, request_contact = True))
        await message.answer(information_messages.start_message, reply_markup = keyboard)
    else:
        await message.answer(information_messages.start_message, reply_markup = aiogram.types.ReplyKeyboardRemove())

async def accure_message_locking(message: aiogram.types.Message, state:aiogram.dispatcher.FSMContext, for_seconds:int = 2,
                                                                                                      step       :int = 1):
    current_data  = await state.get_data()
    current_state = await state.get_state()

    await state.set_state(users_states.locked)

    my_message = await message.answer(information_messages.locking_accured_for.format(seconds = for_seconds))

    while for_seconds:
        await asyncio.sleep(step)
        for_seconds -= step
        await my_message.edit_text(text = information_messages.locking_accured_for.format(seconds = for_seconds))

    await state.set_state(current_state)
    await state.update_data(**current_data)
    await my_message.delete()

@dispatcher.message_handler(commands = ['start'], state = '*')
async def start(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    user = handle_user(message, state)
    current_state = await state.get_state()
    if current_state == users_states.locked:
        message.delete()
    else:
        await return_to_homepage(message, state)

@dispatcher.message_handler(content_types = ['contact'], state = users_states.homepage)
async def handle_user_contact(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    user = handle_user(message, state)
    if message.contact:
        user.mobile_phone    = message.contact.phone_number
        user.can_send_emails = check_access_by_mobile_phone(message)
        if user.can_send_emails:
            await message.answer(information_messages.phone_was_granted)
        else:
            await message.answer(information_messages.phone_was_not_granted)
        user.save()
        await accure_message_locking(message, state)

@dispatcher.message_handler(lambda message: check_access_by_mobile_phone(message), content_types = aiogram.types.ContentTypes.PHOTO, state = users_states.homepage)
async def handle_photo(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    media_group_id = message.media_group_id or media_group_files.unique_id()
    photo_data = message.photo.pop()
    photo_size = photo_data.file_size
    photo_id   = photo_data.file_id
    caption    = message.caption or no_caption

    photo_size_limit_in_bytes = 10 * 1024 * 1024 # 10 mb is a limit of aiogram bot.get_file
    if photo_size >= photo_size_limit_in_bytes:
        await message.answer_photo(photo = photo_id, caption = errors_messages.photo_is_too_large)
    else:
        new_media_group_file = media_group_files.create(media_group_id = media_group_id,
                                                        file_id        = photo_id,
                                                        is_photo       = True,
                                                        caption        = caption)
        new_media_group_file.save()

@dispatcher.message_handler(lambda message: check_access_by_mobile_phone(message), content_types = aiogram.types.ContentTypes.VIDEO, state = users_states.homepage)
async def handle_video(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    media_group_id = message.media_group_id or media_group_files.unique_id()
    video       = message.video
    video_size  = video.file_size
    video_id    = video.file_id
    video_max_size = 10 * 1024 * 1024
    caption = message.caption or no_caption

    if video_size > video_max_size:
        await message.answer_video(video_id, caption = errors_messages.video_is_too_large)
    else:
        new_media_group_file = media_group_files.create(media_group_id = media_group_id,
                                                        file_id        = video_id,
                                                        is_video       = True,
                                                        caption        = caption)
        new_media_group_file.save()

@dispatcher.message_handler(lambda message: check_access_by_mobile_phone(message), content_types = aiogram.types.ContentTypes.DOCUMENT, state = users_states.homepage)
async def handle_document(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    media_group_id = message.media_group_id or media_group_files.unique_id()
    document       = message.document
    document_size  = document.file_size
    document_id    = document.file_id
    document_max_size = 10 * 1024 * 1024
    caption = message.caption or no_caption

    if document_size > document_max_size:
        await message.answer_document(document_id, caption = errors_messages.document_is_too_large)
    else:
        new_media_group_file = media_group_files.create(media_group_id = media_group_id,
                                                        file_id        = document_id,
                                                        is_document    = True,
                                                        caption        = caption)
        new_media_group_file.save()

@dispatcher.message_handler(lambda message: check_access_by_mobile_phone(message), content_types = aiogram.types.ContentTypes.AUDIO, state = users_states.homepage)
async def handle_audio(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    media_group_id = message.media_group_id or media_group_files.unique_id()
    audio          = message.audio
    audio_size     = audio.file_size
    audio_id       = audio.file_id
    audio_max_size = 10 * 1024 * 1024
    caption        = message.caption or no_caption

    if audio_size > audio_max_size:
        await message.answer_audio(audio_id, caption = errors_messages.audio_is_too_large)
    else:
        new_media_group_file = media_group_files.create(media_group_id = media_group_id,
                                                        file_id        = audio_id,
                                                        is_audio       = True,
                                                        caption        = caption)
        new_media_group_file.save()

@dispatcher.message_handler(lambda message: check_access_by_mobile_phone(message), content_types = aiogram.types.ContentTypes.ANIMATION, state = users_states.homepage)
async def handle_animation(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    media_group_id = message.media_group_id or media_group_files.unique_id()
    animation          = message.animation
    animation_size     = animation.file_size
    animation_id       = animation.file_id
    animation_max_size = 10 * 1024 * 1024
    caption        = message.caption or no_caption

    if animation_size > animation_max_size:
        await message.answer_animation(animation_id, caption = errors_messages.animation_is_too_large)
    else:
        new_media_group_file = media_group_files.create(media_group_id = media_group_id,
                                                        file_id        = animation_id,
                                                        is_animation   = True,
                                                        caption        = caption)
        new_media_group_file.save()

@dispatcher.message_handler(lambda message: check_access_by_mobile_phone(message), content_types = aiogram.types.ContentTypes.VOICE, state = users_states.homepage)
async def handle_voice(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    media_group_id = message.media_group_id or media_group_files.unique_id()
    voice          = message.voice
    voice_size     = voice.file_size
    voice_id       = voice.file_id
    voice_max_size = 10 * 1024 * 1024
    caption        = message.caption or no_caption

    if voice_size > voice_max_size:
        await message.answer_voice(voice_id, caption = errors_messages.voice_is_too_large)
    else:
        new_media_group_file = media_group_files.create(media_group_id = media_group_id,
                                                        file_id        = voice_id,
                                                        is_voice       = True,
                                                        caption        = caption)
        new_media_group_file.save()

@dispatcher.message_handler(lambda message: not check_access_by_mobile_phone(message), content_types = aiogram.types.ContentTypes.ANY, state = users_states.homepage)
async def access_not_granted(message:aiogram.types.Message, state:aiogram.dispatcher.FSMContext):
    await message.answer(errors_messages.acess_not_granted)
    await return_to_homepage(message, state)
    await message.delete()

async def send_email(group_id, caption, files):
    subject = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    files_directory = pathlib.Path(str(group_id))
    files_directory.mkdir(parents = True, exist_ok = True)

    downloaded_paths = list()
    for file in files:
        file_from_server = await bot.get_file(file.file_id)
        file_name        = pathlib.Path(file_from_server.file_path).name
        save_file_as     = files_directory.joinpath(file_name)

        await bot.download_file(file_from_server.file_path, save_file_as)
        downloaded_paths.append(save_file_as)
        file.was_loaded = True
        file.was_sent   = True
        file.save()
    await emails_sender.send_message(to_email, subject, caption, downloaded_paths)

async def send_emails():
    for group_id in media_group_files.get_unique_groups_ids():
        files   = list(media_group_files.get_files_by_group_id(group_id))
        files   = list(filter(lambda file: not file.was_sent, files))
        if files and group_id:
            caption = media_group_files.get_caption_of(group_id)
            await send_email(group_id, caption, files)
        elif files and not group_id:
            for file in files:
                caption = file.caption
                attach = [file]
                await send_email(group_id, caption, attach)

def repeat_sending_emails(coro, loop):
    asyncio.ensure_future(coro(), loop = loop)
    loop.call_later(sending_emails_delay, repeat_sending_emails, coro, loop)
