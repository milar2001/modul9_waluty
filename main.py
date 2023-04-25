from flask import Flask, render_template, request, flash
import requests
import csv

app = Flask(__name__, static_folder='static', template_folder='templates')

def save_exchange_data_to_csv():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    items = []
    for x in data[0]['rates']:
        items.append(x)

    with open("exchange_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["currency", "code", "bid", "ask"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)
@app.route('/', methods=['GET', 'POST'])
def currency_calculator():
    if request.method == "POST":
        currency = request.form["currency"]
        quantity = request.form["quantity"]
        with open("exchange_data.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if currency in row['code']:
                    currency_price = row['bid']
        currency_ammount = int(quantity) * float(currency_price)

        return render_template("currency_calculator.html", ammount=currency_ammount, currency=currency)
    return render_template("currency_calculator.html")
if __name__ == '__main__':
    save_exchange_data_to_csv()
    app.run()
