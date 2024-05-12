from flask import Flask, render_template, request, send_file
import subprocess
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    if request.method == 'POST':
        try:
            username = request.form['username']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            token = request.form['token']
            filename = 'databpjs.csv'
            search_keyword = f'to:{username} since:{start_date} until:{end_date} lang:id'
            limit = 100
            
            # Tentukan lokasi dan nama file CSV
            current_directory = os.path.dirname(os.path.realpath(__file__))
            filepath = os.path.join(current_directory, 'tweets-data', filename)

            # Menjalankan perintah tweet-harvest dari Python
            subprocess.run(f'npx -y tweet-harvest@2.6.0 -o "{filepath}" -s "{search_keyword}" --tab "LATEST" -l {limit} --token {token}', shell=True)

            # Setelah proses crawling selesai, baca file CSV dari lokasi yang sesuai
            df = pd.read_csv(filepath)

            # Konversi DataFrame ke HTML
            table_html = df.to_html(classes='table table-striped')

            # Menyimpan DataFrame ke dalam format CSV
            df.to_csv(filepath, index=False)

            return render_template('result.html', table=table_html, filename=filename)
        except Exception as e:
            return f'Terjadi kesalahan: {str(e)}'
    else:
        return 'Metode yang digunakan tidak valid.'

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tweets-data', filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
