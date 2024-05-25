from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Kullanıcı bilgilerini tutacak liste
users = []
articles = [
    {"Konu": "Ekonomi", "Haber": "Pazarlama dünyası İstanbul'da bir araya geldi.", "Link": "https://www.ntv.com.tr/galeri/ekonomi/pazarlama-dunyasi-istanbulda-bir-araya-geldi,9MNz9V4PrUmRGuOq1X-cvQ"},
    {"Konu": "Tarih", "Haber": "Bursa mutfağı, tarihi İpek Han Meydanı'nda vitrine çıktı", "Link": "https://www.hurriyet.com.tr/yerel-haberler/bursa/osmangazi/bursa-mutfagi-tarihi-ipek-han-meydaninda-vitr-42467625"},
    {"Konu": "Spor", "Haber": "Süper Lig'de 3. küme düşen takım belli oldu!", "Link": "https://www.haber1.com/guncel/sivrisinekler-oyunu-11-frankfurt-turk-tiyatro-festivalinde-sahnelendi/"},
    {"Konu": "Tiyatro", "Haber": "“Sivrisinekler” oyunu 11. Frankfurt Türk Tiyatro Festivali'nde sahnelendi", "Link": "https://www.haber1.com/guncel/sivrisinekler-oyunu-11-frankfurt-turk-tiyatro-festivalinde-sahnelendi/"},
    {"Konu": "Bilim", "Haber": "Bilim insanları açıkladı: Milyonları öldüren 'Kara Ölüm' nasıl yayıldı?", "Link": "https://www.ntv.com.tr/dunya/bilim-insanlari-acikladi-milyonlari-olduren-kara-olum-nasil-yayildi,ayJYAAvd4Eu4ZG_O1LiFug"},
    {"Konu": "Sinema", "Haber": "Sinemaseverlere müjde| Bu hafta 8 yeni film vizyona girecek.", "Okunma": "8 min read", "Link": "https://www.sonmuhur.com/sinemaseverlere-mujde-bu-hafta-8-yeni-film-vizyona-girecek"},
    {"Konu": "Astronomi", "Haber": "Astronomi tarihinde ilk: Kara deliğin manyetik alanları görüntülendi!", "Link": "https://www.ntv.com.tr/teknoloji/astronomi-tarihinde-ilk-kara-deligin-manyetik-alanlari-goruntulendi,EnxMSr6MNESRWwROOkNPwQ"},
    {"Konu": "Siyaset", "Haber": "Cumhurbaşkanı Erdoğan'dan Afrika Günü paylaşımı", "Link": "https://www.bursa.com/haber/cumhurbaskani-erdogan-dan-afrika-gunu-paylasimi-934366.html"}
]

current_user = None

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users.append({'username': username, 'email': email, 'password': password, 'profile': ''})
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    global current_user
    email = request.form['email']
    password = request.form['password']
    for user in users:
        if user['email'] == email and user['password'] == password:
            current_user = user
            return redirect(url_for('blog'))
    return 'Giriş başarısız!'
@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('home'))

@app.route('/blog')
def blog():
    if current_user is None:
        return redirect(url_for('home'))
    return render_template('blog.html', users=users, articles=articles)

@app.route('/profile/<username>')
def profile(username):
    user = next((user for user in users if user['username'] == username), None)
    if user is None:
        return 'Kullanıcı bulunamadı!'
    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if current_user is None:
        return redirect(url_for('home'))
    if request.method == 'POST':
        current_user['profile'] = request.form['profile']
        return redirect(url_for('profile', username=current_user['username']))
    return render_template('edit_profile.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
