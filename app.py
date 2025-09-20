from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        a = float(request.form.get("a", 0))
        b = float(request.form.get("b", 0))
        # exemplo: calcular Z = a*x + b*y com x=2,y=3 (substitua pela sua lógica)
        resultado = a*2 + b*3
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
