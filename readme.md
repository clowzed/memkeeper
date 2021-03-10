<h1 align="center">
    Memory keeper
</h1>

<div align="center">
    <img align="center" src='growing.webp'></img>
</div>


<h1 align="center">
    What is it
</h1>
<p align="center">It is a <code>telegram</code> bot based on <code>aiogram</code>.</p>
<p align="center">It resends all documents which you send him to a certain email adress</p>

<h1 align="center">
    Basic idea
</h1>

<p align="center">
    My girlfriend suggested me an idea of creating an email for a child and send all photos, videos and documents
    related to the child there.
    Then, after 18 years of collecting documents give a password to your child.
    You will be able to see his life from very beginning.
</p>

<h1 align="center">
    Installation
</h1>

<h4 align="center">
    Create bot in <code>botfather</code> in telegram and save <code>api key</code>.<br><br>
</h4>

<h4 align="center">Clone the repository</h4>

```bash
git clone https://github.com/clowzed/memkeeper.git
cd memkeeper
```

<h4 align="center"> Install <code><a href="https://github.com/pypa/pipenv">pipenv</a></code> if not installed</h4>

```bash
python3 -m pip install pipenv
```

<h4 align="center">Create your own configuration file</h4>

```bash
cat config_example.ini > config.ini
```
<h4 align="center"> Set lines in file with your credentials </h4>

```ini
[credentials]
bot_token = bot api key from botfather

[mail]
to_email = email of your child
from_email = email from witch this bot will send files
from_email_password = password of this email

[access]
granted_mobile_phones = list of mobile phones of users which can send files
# example: granted_mobile_phones = 79998887766,73331234455
```
<h4 align="center">
    Go to <a href="https://support.google.com/accounts/answer/6010255">your account settings</a>
    (if you are using gmail) and grant access from unsafe applications.
</h4>

<h1 align="center">
    Running
</h1>
<p align="center">
    After setting configuration file and creating your bot simply run.
</p>

```bash
pipenv install
pipenv run python memkeeper.py
```


<h1 align="center">
    Supported message types
</h1>


<div align="center">
    <table align="center">
        <thead align="center">
            <tr align="center">
                <th align="center">message type</th>
                <th align="center">can be resend</th>
                <th align="center">can be resend in group</th>
            </tr>
        </thead>
        <tbody align="center">
            <tr>
                <td align="center">photo</td>
                <td align="center">🟢</td>
                <td align="center">🟢</td>
            </tr>
            <tr>
                <td align="center">video</td>
                <td align="center">🟢</td>
                <td align="center">🟢</td>
            </tr>
            <tr>
                <td align="center">animation</td>
                <td align="center">🟢</td>
                <td align="center">🟢</td>
            </tr>
            <tr>
                <td align="center">document</td>
                <td align="center">🟢</td>
                <td align="center">🟢</td>
            </tr>
            <tr>
                <td align="center">voice</td>
                <td align="center">🟢</td>
                <td align="center">🟢</td>
            </tr>
            <tr>
                <td align="center">plain text</td>
                <td align="center"></td>
                <td align="center">🟢</td>
            </tr>
        </tbody>
    </table>
</div>