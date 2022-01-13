"""
Copyright 2021 MiranDaniel
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from flask import Flask, render_template, request, redirect
import yaml
import requests
import os

config = {}
config["recaptcha"] = {}
config["discord"] = {}
config["server"] = {}

if os.environ.get('DISCORD_CATCHA_DARK_THEME') != "":
    config["dark_theme"] = os.environ.get('DISCORD_CATCHA_DARK_THEME')
else:
    config["dark_theme"] = True

if os.environ.get('DISCORD_CATCHA_RECAPTCHA_PUBLIC') != "":
    config["recaptcha"]["public"] = os.environ.get('DISCORD_CATCHA_RECAPTCHA_PUBLIC')
else:
    print("!! Recaptcha public key is not defined, exiting")
    quit(1)

if os.environ.get('DISCORD_CATCHA_RECAPTCHA_PRIVATE') != "":
    config["recaptcha"]["private"] = os.environ.get('DISCORD_CATCHA_RECAPTCHA_PRIVATE')
else:
    print("!! Recaptcha private key is not defined, exiting")
    quit(1)

if os.environ.get('DISCORD_CATCHA_DISCORD_ROOM') != "":
    config["discord"]["welcome_room"] = os.environ.get('DISCORD_CATCHA_DISCORD_ROOM')
else:
    print("!! Discord welcome room not defined, exiting")
    quit(1)

if os.environ.get('DISCORD_CATCHA_DISCORD_PRIVATE') != "":
    config["discord"]["private"] = os.environ.get('DISCORD_CATCHA_DISCORD_PRIVATE')
else:
    print("!! Discord private key is not defined, exiting")
    quit(1)

def recaptcha(token):
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': config["recaptcha"]["private"],
        'response': token,
        'remoteip': request.remote_addr,
    }
    response = requests.post(recaptcha_url, data = payload)
    result = response.json()
    return result

def invite():
    resp = requests.post(
        'https://discordapp.com/api/channels/%s/invites' % config["discord"]["welcome_room"],
        headers={'Authorization': 'Bot %s' % config["discord"]["private"]},
        json={'max_uses': 1, 'unique': True, 'expires': 300}
    )
    i = resp.json()
    return i["code"]

app = Flask(__name__)

theme = "text-dark border-dark" if config["dark_theme"] else "text-light border-light"
border = "border-dark" if config["dark_theme"] else ""
catpcha_theme = "dark" if config["dark_theme"] else "light"


@app.route("/") # main function
def index():
    key = request.args.get('key') # get key parameter from URL
    if key: # if key set
        r = recaptcha(key) # confirm captcha
        if r["success"]: # if ok
            i = invite() # generate new invite
            return redirect(f"https://discord.gg/{i}") # redirect user to new invite
        else: # if captcha invalid
            return render_template("index.html", public=config["recaptcha"]["public"], failed=True, theme=theme, border=border, catpcha_theme=catpcha_theme) # return error page
    # if not key
    return render_template("index.html", public=config["recaptcha"]["public"], failed=False, theme=theme, border=border, catpcha_theme=catpcha_theme) # return normal page
