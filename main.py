import base64
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request,send_from_directory
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import datetime
'''Написать на питоне Веб-приложение, которое должно изменять размер картинки по указанному значению масштаба и показывать 
результат пользователю, выдавать графики распределения цветов исходной и полученной картинки.'''


app = Flask(__name__)
app.config['SECRET_KEY'] = '6LcoJj8mAAAAAPNFRrIpF6JM_rQeYgeZg_LS8MLd'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcoJj8mAAAAAE2lrAhxkHd_l2iu9hwDbswXunE9'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcoJj8mAAAAAPNFRrIpF6JM_rQeYgeZg_LS8MLd'

class ContactForm(FlaskForm):
    # name = StringField('Name', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    # message = StringField('Message', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Подтвердить')


@app.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # name = form.name.data
        # email = form.email.data
        # message = form.message.data
        # send email or save to database
        return index()
    return render_template('contact.html', form=form)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def ind():
    if request.method == 'POST':
        image = Image.open(request.files['image'])
        scale_1 = float(request.form['scale_1'])
        scale_2 = float(request.form['scale_2'])
        # Изменяю размер изображения
        new_size = (int(image.width * scale_1), int(image.height * scale_2))
        resized_image = image.resize(new_size)
        image.save('static/original.png')
        resized_image.save('static/resized.png')

        # Преобразуем изображения в массивы NumPy
        original_array = np.array(image)
        resized_array = np.array(resized_image)

        # Вычисляем гистограмму распределения цветов для измененного изображения
        histogram, bins = np.histogram(resized_array.flatten(), bins=256, range=(0, 255))
        # Рисуем гистограмму
        plt.bar(bins[:-1], histogram, width=1)
        plt.xlim(min(bins), max(bins))
        plt.savefig('static/histogram.png')

        # Кодируем изображения и гистограмму в base64
        with open('static/original.png', 'rb') as f:
            original_data = base64.b64encode(f.read()).decode('utf-8')
        with open('static/resized.png', 'rb') as f:
            resized_data = base64.b64encode(f.read()).decode('utf-8')
        with open('static/histogram.png', 'rb') as f:
            histogram_data = base64.b64encode(f.read()).decode('utf-8')
        # Возвращаем оригинальное и измененное изображения и гистограмму
        return render_template('result.html', original_data=original_data, resized_data=resized_data, histogram_data=histogram_data)
if __name__ == '__main__':
    app.run(debug=True)

