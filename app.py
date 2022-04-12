from cgitb import text
from flask import Flask, render_template, make_response, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os.path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F3HUIF23H8923F9H8389FHXKLN'
app.config['UPLOAD_FOLDER'] = '/home/adam/paste-tool/templates'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/pastebin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class texts(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  location = db.Column(db.String(1000), nullable=False)
  url = db.Column(db.String(100), nullable=False)
  def __init__(self, location, url):
    self.location = location
    self.url = url

# db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    oko = request.form['text']
    now1 = datetime.now()
    d1 = now1.strftime("%d%m%Y")
    current_time = now1.strftime("%H%M%S")
    file_name = str(d1) + '' + str(current_time)
    completeName = os.path.join(app.config['UPLOAD_FOLDER'], file_name+".txt")  
    with open(completeName, 'w', encoding="utf8", errors='ignore') as file:
      file.write(oko)
    u = texts(completeName, file_name)
    db.session.add(u)
    db.session.commit()
    return redirect('/file/' + file_name)

  return render_template('index.html')

@app.route('/file/<file>')
def file(file):
  try:
    q = db.session.query(texts.location).filter(texts.url == file).first()
    if q == None: return redirect('/')
    resp = make_response(render_template(file + '.txt'))
    return render_template('file.html', resp=[resp.get_data().decode('UTF-8')])
  except: return redirect('/')

@app.route('/raw/file/<file>')
def getfile(file):
  try:
    q = db.session.query(texts.location).filter(texts.url == file).first()
    if q == None: return redirect('/')
    resp = make_response(render_template(file + '.txt'))
    resp.mimetype = 'text/plain'
    return resp
  except: return redirect('/')


if __name__ == '__main__':
  app.run(debug=True)