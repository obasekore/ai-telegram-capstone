
from flask import Flask, request, jsonify, render_template, url_for
import requests
import json
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__, static_folder='statics')#, template_folder='/templates')
model = YOLO("yolo11n.pt")

CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
  q = ''
  pass
