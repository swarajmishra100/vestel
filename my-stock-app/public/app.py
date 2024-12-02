from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io

# Personally Developed
from backend import backend
from algorithm import algorithm

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form.get("ticker", "AAPL").upper()
        tester = backend()
        algo = algorithm(ticker)
        tester.run(algo)

        img = io.BytesIO()
        plt.figure(figsize=(10, 6), num="RSI Algorithm for " + ticker)
        tester.calculateVol(algo)
        tester.graphReturns(algo)
        tester.graphRSI(algo)
        tester.calculate_total_returns(algo)
        tester.calculate_market_return(algo)
        plt.tight_layout()

        plt.savefig(img, format='png')
        img.seek(0)  # Rewind the buffer
        return send_file(img, mimetype='image/png', as_attachment=False)

    return render_template("index.html", plot_url=None, ticker=None)

if __name__ == "__main__":
    app.run(debug=False)
