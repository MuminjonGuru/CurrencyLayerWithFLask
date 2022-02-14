from flask import Flask, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/result/<string:usd_aud>/<string:usd_eur>/<string:usd_gbp>')
def result_realtime(usd_aud, usd_eur, usd_gbp):
    return "<h3>USDAUD: {};  <br>USDEUR: {}; <br>USDGBP: {}</h3>".format(usd_aud, usd_eur, usd_gbp)


@app.route('/rtrates', methods=['GET', 'POST'])
def rtrates():
    if request.method == 'GET':
        return '''<h1>Please fill out the parameters</h1>
                    <form method="POST" action="/rtrates">
                    <input type="text" name="acc_key" value="c92b0e664f8dd7743333fed2f42fd6c9">
                    <input type="text" name="currencies" value="AUD,EUR,GBP">                
                    <input type="submit" value="Request">
                </form>'''
    else:
        acc_key = request.form['acc_key']
        currencies = request.form['currencies']

        req = requests.get('https://api.currencylayer.com/live?access_key=' + acc_key + '&currencies=' + currencies)
        response = req.json()

        usd_aud = response['quotes']['USDAUD']
        usd_eur = response['quotes']['USDEUR']
        usd_gbp = response['quotes']['USDGBP']

        return redirect(url_for('result_realtime', usd_aud=usd_aud, usd_eur=usd_eur, usd_gbp=usd_gbp))


@app.route('/result/<string:from_c>/<string:to_c>/<string:amount>/<string:quote>/<string:result>')
def result_conversion(from_c, to_c, amount, quote, result):
    return "<h3>From: {};  <br>To: {}; <br>Amount: {}; <br> Result: {}; <br> Quote: {};</h3>" \
        .format(from_c, to_c, amount, result, quote)


@app.route('/conversion', methods=['GET', 'POST'])
def conversion():
    if request.method == 'GET':
        return '''<h1>Please fill out the parameters</h1>
                    <form method="POST" action="/conversion">
                    <input type="text" name="acc_key" value="c92b0e664f8dd7743333fed2f42fd6c9">
                    <input type="text" name="from" value="from">
                    <input type="text" name="to" value="to">
                    <input type="text" name="amount" value="amount">
                    <input type="submit" value="Request">
                </form>'''
    else:
        acc_key = request.form['acc_key']
        from_c = request.form['from']
        to_c = request.form['to']
        amount = request.form['amount']

        req = requests.get(
            'https://api.currencylayer.com/convert?access_key=' + acc_key + '&from=' + from_c
            + "&to=" + to_c + "&amount=" + amount)
        response = req.json()

        quote = response['info']['quote']
        result = response['result']

        return redirect(
            url_for('result_conversion', from_c=from_c, to_c=to_c, amount=amount, quote=quote, result=result))


if __name__ == '__main__':
    app.run()
