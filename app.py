from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/metodos)", methods=["GET", "POST"])
def metodos():
    if request.method == "POST":
        pass
    return render_template("metodos.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/algoritmos")
def algoritmos():
    return render_template("algoritmos.html")

if __name__ == "__main__":
    app.run(debug=True)
