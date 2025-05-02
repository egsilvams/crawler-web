from flask import Flask, request, render_template, redirect, url_for, send_file
from crawler import crawler  # Seu crawler original
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        clusters = int(request.form['clusters'])
        resultado = crawler(url, clusters)
        return redirect(url_for('resultado', total=len(resultado)))
    return render_template('index.html')

@app.route('/resultado')
def resultado():
    total = request.args.get('total', type=int)
    with open("urls_encontradas.txt", "r", encoding="utf-8") as f:
        urls = [linha.strip() for linha in f.readlines()]
    return render_template("resultado.html", resultado=urls, total=total)

@app.route('/download')
def download():
    caminho = "urls_encontradas.txt"
    if os.path.exists(caminho):
        return send_file(caminho, as_attachment=True)
    return "Arquivo não encontrado", 404

if __name__ == "__main__":
    app.run(debug=True)
