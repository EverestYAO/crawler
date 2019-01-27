from flask import Flask
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-never-know'

@app.route('/',methods=['GET'])
def run():
    time.sleep(15)
    return 'hello world'


