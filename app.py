from http.client import responses

from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)


def fetch_conversion_factor(source,target):
    url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=9a9a105066244353a1f0419766f1574f"
    response = requests.get(url)
    data = response.json()
    rates = data['rates']

    source = source.upper()
    target = target.upper()

    if source not in rates or target not in rates:
        return None

    rate = float(rates[target]) / float(rates[source])
    return rate

if __name__ == "__main__":
    app.run(debug=True)