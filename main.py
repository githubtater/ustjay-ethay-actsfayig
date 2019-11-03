import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

fact_string = 'Here\'s a random fact for you! <b>  {}</b><br>' \
        'Click here to view it in Pig Latin: {}'


def get_fact():
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    return facts[0].getText()


@app.route('/')
def home():
    latin_url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    fact = get_fact().strip()
    payload = {'input_text': fact}
    r = requests.post(latin_url, data=payload, allow_redirects=False)
    soup = BeautifulSoup(r.content, "html.parser")
    url = soup.find('a', href=True)
    build_url = latin_url.replace('/piglatinize/', '') + url.text
    return fact_string.format(fact, f'<a href="{build_url}">{build_url}</a>')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='localhost', port=port)

