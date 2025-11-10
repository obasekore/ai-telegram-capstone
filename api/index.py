
from flask import Flask, request, jsonify, render_template, url_for
import requests
import json
from flask_cors import CORS
# from ultralytics import YOLO

app = Flask(__name__, static_folder='statics')#, template_folder='/templates')
# model = YOLO("yolo11n.pt")

CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
  q = ''
  pass

@app.route('/telegram/webhook', methods=['GET', 'POST'])
def telegramStart():
    bot_token = env.get('TELEGRAM_BOT_TOKEN')
    # https://api.telegram.org/bot$telegram_apikey/webappinfo
    wake = 'start'
    default = [{'text':'start'}]
    # data==> url:
    if request.method == 'POST':
        # Access POST data from the request
        msg = request.get_json()  
        print("Message: ",msg)

        msg_text = 'Can not process the request, please enter a valid request.'
        keyboard = {}
        # Trying to parse message
        try:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage' # Calling the telegram API to reply the message
            print("There is a text")
            chat_id = msg['message']['chat']['id']
            text = msg['message']['text'] # This gets the text from the msg
            text = text.lower()
            services = plans.keys()
            if wake in text:
                networks = [{'text': network} for network in services]
                networks += default
                keyboard = {
                    # 'keyboard':[[{'text' : 'button 1'}, {'text' : 'button 2'}, {'text' : 'button 3'}]],
                    'keyboard':[networks],
                    'resize_keyboard':True,
                    'one_time_keyboard' : True
                }
                msg_text = "Please select the network plan you want to subscribe."

            elif text in list(services):
                temp = ''#[{'text': text.upper() + ':' + network + '@#' + plans[text]['amount']} for network in plans[text].keys()]
                temp_plan = plans[text]
                networks = [{'text':f'{text.upper()}: {network} @ #{temp_plan[network]["amount"]}' } for network in temp_plan.keys()]
                networks += default
                keyboard = {
                    # 'keyboard':[[{'text' : 'button 1'}, {'text' : 'button 2'}, {'text' : 'button 3'}]],
                    'keyboard':[networks],
                    'resize_keyboard':True,
                    'one_time_keyboard' : True
                }
                msg_text =  "Please select the {} data size you want to subscribe.".format(text.upper())

            elif (len(text.split(':'))>1):
                amount = text.split('@')[-1]
                networks = [{'text': 'Pay ' + amount} ]
                networks += default
                keyboard = {
                    # 'keyboard':[[{'text' : 'button 1'}, {'text' : 'button 2'}, {'text' : 'button 3'}]],
                    'keyboard':[networks],
                    'resize_keyboard':True,
                    'one_time_keyboard' : True
                }

                msg_text =  "Confirm to proceed with the purchase of {}.".format(text)
                # amount
            payload = {
            'chat_id': chat_id,
            'text': msg_text,
            'reply_markup': keyboard
            }
            r = requests.post(url, json=payload)

            if r.status_code == 200:
                return 'ok'
            else: 
                return 'Failed to send message to Telegram'
        except:
            print("No text found")

        return 'ok'
    return 'Okay'
