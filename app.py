from flask import Flask, render_template,request,url_for,redirect
import requests
from bs4 import BeautifulSoup
from analyze import get_word_count, text_from_html

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('analyzer.html')


@app.route('/get_info',methods=['POST'])
def get_info():
    url = request.form['input_url']
    try:
        source = requests.get(url, timeout=5)
        soup = BeautifulSoup(source.text, 'html.parser')
        page_text = text_from_html(soup)
        total_count, unique_count, top_words = get_word_count(page_text)
    except requests.ConnectionError as e:
        error_message = "Connection Error. Make sure you are connected to Internet"
        return redirect(url_for('error',error_message=error_message+":"+str(e)))
    except requests.Timeout as e:
        error_message = "Timeout Error"
        return redirect(url_for('error', error_message=error_message+":"+str(e)))
    except requests.RequestException as e:
        error_message = "General Error"
        return redirect(url_for('error', error_message=error_message+":"+str(e)))
    except KeyboardInterrupt as e:
        error_message = "Keyboard interrupt"
        return redirect(url_for('error', error_message=error_message+":"+str(e)))

    return render_template('analyzer.html',total_count=total_count,unique_count=unique_count,top_words=top_words)


@app.route('/error/<error_message>')
def error(error_message):
    return render_template('error.html',error_message=error_message)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
