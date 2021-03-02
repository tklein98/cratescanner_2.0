from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import Flask, flash, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
