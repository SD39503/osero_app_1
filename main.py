from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')  # ルートを変更
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)      