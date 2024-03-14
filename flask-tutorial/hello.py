from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<marquee><h1>Olá Mundo!</h1></marquee>"

app.run(debug=True)