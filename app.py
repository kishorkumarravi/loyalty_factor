from flask import Flask, jsonify, request, make_response
import os
import json
import logging
import logging.config
import pandas as pd

data = [{'cardType':'Silver', 'category':'FUEL','tran_date':'2020-01-12', 'desc':'Test', 'reward':'1', 'status':'SUCCESS'},\
        {'cardType':'Gold', 'category':'INSURANCE','tran_date':'2020-02-12', 'desc':'Test', 'reward':'2', 'status':'CANCELLED'},
        {'cardType':'Platinum', 'category':'WALLET','tran_date':'2020-03-12', 'desc':'Test', 'reward':'0', 'status':'FAILED'},
        {'cardType':'Black', 'category':'WALLET','tran_date':'2020-03-12', 'desc':'Test', 'reward':'16', 'status':'FAILED'}]

month_util = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', \
    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

card_reward = {'Silver':1, 'Gold':2, 'Platinum':4, 'Black':8}

app = Flask(__name__)

def init_logging(default_path=os.path.join(os.path.dirname(os.path.abspath(\
    os.path.dirname(__file__))), 'logging.yml'), default_level=logging.INFO,):
    logging.basicConfig(level=default_level)

@app.route('/about', methods=['GET'])
def about():
    logging.info(f'About')
    return jsonify(message='About')

@app.route('/upload/file', methods=['POST'])
def uploadfile():
    try:
        input_file = request.files['file']
        df = pd.read_csv(input_file, index_col = 0)
        str_data = df.reset_index().to_json(orient='records')

        json_data = json.loads(str_data)

        logging.info(f'Initial records : {len(data)}')
        for rec in json_data:
            reward, status = get_reward(rec)
            rec['reward']= reward
            rec['status']= status

            data.append(rec)
        logging.info(f'total records : {len(data)}')
        return make_response(jsonify(message='Records added succesfully'), 200)
    except Exception as err:
        logging.error(f'err : {err}')
        return make_response(jsonify(message='Failed to upload record'), 400)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        logging.info(f'Initial records : {len(data)}')
        req_data = json.loads(request.data)
        for rec in req_data:
            reward, status = get_reward(rec)
            rec['reward']= reward
            rec['status']= status

            data.append(rec)
        logging.info(f'total records : {len(data)}')
        return make_response(jsonify(message='Records added succesfully'), 200)
    except Exception as err:
        logging.error(f'err : {err}')
        return make_response(jsonify(message='Failed to upload record'), 400)

@app.route('/fetch/all', methods=['GET'])
def fetch():
    try:
        logging.info(f'Fetching all records')
        return jsonify(data=data, size=len(data))
    except Exception as err:
        logging.error(f'err : {err}')
        return make_response(jsonify(message='Failed to Fetch records'), 400)

@app.route('/fetch/<type>/<value>', methods=['GET'])
def fetch_by_type(type, value):
    try:
        logging.info(f'Fetching by {type} : {value}')
        result = []
        for rec in data:
            if type == 'month':
                month = month_util[value]
                date = rec['tran_date']
                rec_month = date[5:7]
                if rec_month == month:
                    result.append(rec)
            else:
                if rec[type] == value:
                    result.append(rec)
        return make_response(jsonify(data=result), 200)
    except Exception as err:
        logging.error(f'err : {err}')
        return make_response(jsonify(message='Failed to add record'), 400)

def get_reward(req_data):
    try:
        amount = req_data['amount']
        temp_reward = str(int(amount)/150)[:1]
        cardType = req_data['cardType']
        rewardType = card_reward[cardType]
        org_reward = int(temp_reward)*int(rewardType)
        logging.info(f'reward :: {org_reward}')
        return org_reward, 'SUCCESS'
    except Exception as err:
        logging.error(f'Exception get_reward: {err}')
        return 0, 'FAILED'

if __name__ == "__main__":
    init_logging()
    app.run()

