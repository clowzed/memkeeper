import peewee
import datetime
import pprint
import pathlib

storages_directory = pathlib.Path('./storages')
storages_directory.mkdir(parents = True, exist_ok = True)

users_database_file  = storages_directory.joinpath('users.db')
if not users_database_file.exists():
    users_database_file.touch()

media_groups_database_file = storages_directory.joinpath('media_groups.db')
if not media_groups_database_file.exists():
    media_groups_database_file.touch()



users_database        = peewee.SqliteDatabase(users_database_file)
media_groups_database = peewee.SqliteDatabase(media_groups_database_file)

no_mobile_phone = 'no mobile phone'
no_caption = ' '


class model_helper:
    def representation(self):
        result_string = str()
        model_data    = self.__dict__['__data__']
        return pprint.pformat(model_data, indent = 4)

    @classmethod
    def unique_id(cls):
        return len(cls.select())

class users(peewee.Model, model_helper):
    id              = peewee.IntegerField()
    chat_id         = peewee.IntegerField()
    mobile_phone    = peewee.CharField(default = no_mobile_phone)
    can_send_emails = peewee.BooleanField(default = False)
    sent_emails     = peewee.IntegerField(default = 0)
    sent_photos     = peewee.IntegerField(default = 0)

    class Meta:
        database = users_database


class media_group_files(peewee.Model, model_helper):
    media_group_id  = peewee.IntegerField()
    file_id         = peewee.IntegerField()
    is_video        = peewee.BooleanField(default = False)
    is_photo        = peewee.BooleanField(default = False)
    is_document     = peewee.BooleanField(default = False)
    is_audio        = peewee.BooleanField(default = False)
    is_voice        = peewee.BooleanField(default = False)
    is_animation    = peewee.BooleanField(default = False)
    was_loaded      = peewee.BooleanField(default = False)
    was_sent        = peewee.BooleanField(default = False)
    caption         = peewee.CharField()

    class Meta:
        database = media_groups_database

    @classmethod
    def get_unique_groups_ids(cls):
        res = set()
        for group in cls.select().group_by(cls.media_group_id):
            res.add(group.media_group_id)
        return res

    @classmethod
    def get_files_by_group_id(cls, group_id):
        yield from cls.select().where(cls.media_group_id == group_id)

    @classmethod
    def get_caption_of(cls, group_id):
        caption = no_caption
        for file in cls.get_files_by_group_id(group_id):
            file_caption = file.caption
            if file_caption != no_caption:
                caption = file_caption
        return caption



users.create_table()
media_group_files.create_table()