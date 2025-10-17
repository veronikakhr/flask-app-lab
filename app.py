from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('resume.html', title="Резюме Вероніки")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")

if __name__ == '__main__':
    app.run(debug=True)
