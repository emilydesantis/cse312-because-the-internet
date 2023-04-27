import socketserver
import database
import json
import hashlib
import base64
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def html():
   return render_template('frontend/index.html')

def css():
   return render_template('frontend/style.css')

def js():
   return render_template('frontend/main.js')

if __name__ == '__main__':
    app.run(debug=True)


