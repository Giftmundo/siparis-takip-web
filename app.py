from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'siparisler.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Siparis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    musteri_adi = db.Column(db.String(100), nullable=False)
    proje_adi = db.Column(db.String(100), nullable=False)
    siparis_no = db.Column(db.String(50), nullable=False)
    adet = db.Column(db.Integer, nullable=False)
    kutu_boyutu = db.Column(db.String(50), nullable=False)
    kutu_rengi = db.Column(db.String(50), nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    teslim_turu = db.Column(db.String(50), nullable=False)
    siparis_durumu = db.Column(db.String(50), nullable=False)
    siparis_tarihi = db.Column(db.Date, nullable=False)
    teslim_tarihi = db.Column(db.Date, nullable=False)

# Veritabanı tablolarını oluştur
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            yeni_siparis = Siparis(
                musteri_adi=request.form['musteri_adi'],
                proje_adi=request.form['proje_adi'],
                siparis_no=request.form['siparis_no'],
                adet=int(request.form['adet']),
                kutu_boyutu=request.form['kutu_boyutu'],
                kutu_rengi=request.form['kutu_rengi'],
                fiyat=float(request.form['fiyat']),
                teslim_turu=request.form['teslim_turu'],
                siparis_durumu=request.form['siparis_durumu'],
                siparis_tarihi=datetime.strptime(request.form['siparis_tarihi'], '%Y-%m-%d').date(),
                teslim_tarihi=datetime.strptime(request.form['teslim_tarihi'], '%Y-%m-%d').date()
            )
            db.session.add(yeni_siparis)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Hata: {e}"

    siparisler = Siparis.query.all()
    return render_template('index.html', siparisler=siparisler)

if __name__ == '__main__':
    app.run(debug=True)
