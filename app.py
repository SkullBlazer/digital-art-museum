from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Iwonttellany1!" #HIDE IF SHARING
app.config['MYSQL_DB'] = "test"
db = MySQL(app)
login = False

@app.route('/login', methods=['GET', 'POST'])
def index():
    global login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM customer;")
        bid = cur.rowcount + 1
        try:
            phone = request.form['phone']
            email = request.form['email']
            cur.execute('INSERT INTO customer (custid, custname, custemail, custpass, custphone) VALUES\
            (%s, %s, %s, %s, %s);', (bid, username, email, password, phone))
        except KeyError:
            cur.execute('SELECT * FROM customer WHERE custname = %s AND custpass = %s;', (username, password))
            cur.fetchall()
            if cur.rowcount == 0:
                cur.close()
                return render_template('invalid.html')
            else:
                login = True
                cur.close()
                return redirect(url_for('logged_in'))
        db.connection.commit()
        cur.close()
        return "Success!"
    return render_template('index.html')

@app.route('/users')
def users():
    cur = db.connection.cursor()
    users = cur.execute("SELECT * FROM customer;")

    if users > 0:
        userDetails = cur.fetchall()
        cur.close()
        return render_template('users.html', userDetails=userDetails)
    cur.close()

@app.route('/u')
def logged_in():
    if login:
        return render_template('site2.html')
    else:
        return redirect(url_for('index'))

@app.route('/home')
def home():
    global login
    if login:
        return render_template('site2.html')
    else:
        return render_template('site.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/art')
def art():
    cur = db.connection.cursor()
    q = cur.execute("SELECT * FROM art;")
    if q > 0:
        artTable = cur.fetchall()
        return render_template('art.html', artTable=artTable)
    cur.close()

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/artist', methods=['GET', 'POST'])
def artist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE aname = %s AND apass = %s;', (username, password))
        cur.fetchall()
        if cur.rowcount == 0:
            cur.close()
            return render_template('artistinvalid.html')
        else:
            cur.close()
            return redirect(url_for('logged_in'))
    return render_template('artist.html')

@app.route('/')
def redir():
    return redirect(url_for('home'))

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/product/1')
def product1():
    return render_template('products/product1.html')

@app.route('/product/2')
def product2():
    return render_template('products/product2.html')

@app.route('/product/3')
def product3():
    return render_template('products/product3.html')

@app.route('/product/4')
def product4():
    return render_template('products/product4.html')

@app.route('/product/5')
def product5():
    return render_template('products/product5.html')

@app.route('/product/6')
def product6():
    return render_template('products/product6.html')

if __name__ == "__main__":
    app.run(debug=True)