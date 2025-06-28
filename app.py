from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])  #dBm
            # num2 = float(request.form["num2"])
            result = 10*np.log10(num1/10)       #mW
        except ValueError:
            result = "Invalid input"
    return render_template("calculator.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
