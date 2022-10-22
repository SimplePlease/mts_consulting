from flask import Flask, request
from config import texts
app = Flask(__name__)


@app.route('/')  # this is the home page route
def hello_world():  # this is the home page function that generates the page code
    return "Hello world!"    


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')
  
    if query_result.get('action') == 'get.general_info.certain':
        tarif_wanted = query_result.get('parameters').get('tarif_wanted')
        print('here tarif_wanted = {0}'.format(tarif_wanted))
        fulfillmentText = texts['tarif'][tarif_wanted]
        print(fulfillmentText)

    if query_result.get('action') == 'get.general_info.all':
      fulfillmentText = texts['general_info']
      print(fulfillmentText)

    if query_result.get('action') == 'get.general_info.certain.measures':
      tarif_wanted = query_result.get('parameters').get('tarif_wanted')
      measure = query_result.get('parameters').get('measures')
      fulfillmentText = texts[measure][tarif_wanted]
      print(fulfillmentText)

    if query_result.get('action') == 'get.measures.certain':
      tarif = query_result.get('parameters').get('tarif')
      measure = query_result.get('parameters').get('measures')
      fulfillmentText = texts[measure][tarif]
      print(fulfillmentText)

    if query_result.get('action') == 'get.info.cheaper.than' or query_result.get('action') == 'get.info.cheaper':
      tarif_wanted = query_result.get('parameters').get('tarif_wanted')
      price = query_result.get('parameters').get('price')
      fulfillmentText = texts[price][tarif_wanted]
      print(fulfillmentText)

    if query_result.get('action') == 'get.general_info.extra':
      tarif_wanted = query_result.get('parameters').get('tarif_wanted')
      measure = query_result.get('parameters').get('measures')
      if measure == 'Минуты':
        measure = 'Доп минуты'
      if measure == 'Смс':
        measure = 'Доп Смс'
      if measure == 'Интернет':
        measure = 'Доп интернет'
      fulfillmentText = texts[measure][tarif_wanted]
      print(fulfillmentText)

    if query_result.get('action') == 'sms.abroad':
      tarif_wanted = query_result.get('parameters').get('tarif_wanted')
      fulfillmentText = texts['Зарубеж'][tarif_wanted]
      print(fulfillmentText)

    if query_result.get('action') == 'get.general_info.home_number':
      tarif_wanted = query_result.get('parameters').get('tarif_wanted')
      fulfillmentText = texts['Городской'][tarif_wanted]
      print(fulfillmentText)

    if query_result.get('action') == 'short':
      tarif_wanted = query_result.get('parameters').get('tarif_wanted')
      fulfillmentText = texts['Команда'][tarif_wanted]
      print(fulfillmentText)

    if query_result.get('action') == 'get.list.by_price':
      prices = query_result.get('parameters').get('number')
      znak = query_result.get('parameters').get('price')
      res = list()
      temp = texts['Цены']
      if len(prices) == 1 and znak != None:
        print('aaa', znak)
        for key in texts['Цены']:
          if znak == 'Дешевый' and temp[key] <= prices[0]:
            print('1')
            res.append(f'{key} по цене {temp[key]} руб./мес.')
          if znak == 'Дорогой' and temp[key] >= prices[0]:
            res.append(f'{key} по цене {temp[key]} руб./мес.')
            print('2')
        print(res)
      elif len(prices) > 1:
        prices = sorted(prices)
        for key in texts['Цены']:
          if texts['Цены'][key] >= prices[0] and texts['Цены'][key] <= prices[-1]:
            print(texts['Цены'][key], prices[0], prices[-1])
            res.append(f'{key} по цене {temp[key]} руб./мес.')
      if len(res) == 0:
        fulfillmentText = 'К сожалению, таких тарифов нет, но ознакомьтесь с нашими предложениями:\n'
        fulfillmentText += texts['general_info']
      else:
        fulfillmentText = 'Вам подойдут тарифы:\n'
        fulfillmentText += str.join(',\n', res)
        print(fulfillmentText)
    return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }


if __name__ == '__main__':
    # This line is required to run Flask on repl.it
    app.run(host='0.0.0.0', port=8080)
