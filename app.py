from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Kullanıcı bilgilerini tutacak listeler
users = []
articles = [
    {"title": "How to Craft a Developer Resume", "description": "Tips and ideas for creating a great tech resume.", "read_time": "1 min read"},
    {"title": "Vue.js Global 2020: A Recap", "description": "Thoughts and experiences from attending Vue.js Global.", "read_time": "10 min read"},
    {"title": "Build a Blog using Nuxt.js Content Module", "description": "What you need to know about the Nuxt Content Module.", "read_time": "1 min read"},
    {"title": "My 3 Favorite VS Code Extensions", "description": "Shared my top 3 favorite VS Code Extensions.", "read_time": "1 min read"},
    {"title": "How to Switch Logo in Dark Mode", "description": "How I switch the color of my logo in dark mode.", "read_time": "1 min read"},
    {"title": "Deploy a Gridsome App on Azure Static Web Apps", "description": "How to deploy a static website using Azure Static Web Apps.", "read_time": "8 min read"},
    {"title": "5 Soft Skills Every Software Developer Should Learn", "description": "Some core technical things that are not so obvious.", "read_time": "1 min read"},
    {"title": "Let's Learn Data Visualization with D3.js", "description": "A challenge to learn a new technology using D3.js.", "read_time": "10 min read"}
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
