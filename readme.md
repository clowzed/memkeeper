<h1 align = "center">
Memory keeper
<h1>

<h1 align = "center">
Basic idea
</h1>
<p align = "center">
My girlfriend suggested me an idea of creating an email for a child and send all photos, videos and documents related to the child there. 
Then, after 18 years of collecting photos and videos give a password to your child amd all together see how he/she was growing.
</p>
<h1 align = "center">
Description
</h1>
<p align = "center">
This is a telegram bot for resending all media to a certain email address.
</p>

# Seettings
### 1) Create an email address at gmail
### 2) Go to settings of YOUR EMAIL and allow access from unknown applications
### 3) Open 'config.ini' and set:
```ini
[credentials]
bot_token = ?

[mail]
to_email            = ?
from_email          = ?
from_email_password = ?

[access]
granted_mobile_phones = phone1, phone2, phone3
```

# Installation and run
```bash
git clone https://github.com/clowzed/memorykeeper.git
cd memorykeeper
pipenv install
pipenv shell
python memorykeeper.py
```
