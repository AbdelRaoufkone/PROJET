from flask import Flask, request, render_template, redirect, url_for
import psycopg2
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

app = Flask(__name__)

 
@app.route('/', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        return redirect('/home')
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def index():
    return render_template('accueil.html')

@app.route('/licence/algorithmique', methods=['GET', 'POST'])
def hist_algo():
	global matiere
	con = psycopg2.connect(database="Mabase", user = "KONE", password = "67749189", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute("SELECT * FROM algo")
	rows = cur.fetchall()
	con.close()
	if request.method == 'POST':
		matiere = 'Algorithmique'
		return redirect(url_for('emargement'))
	return render_template('algorithme.html', ligne = rows)

@app.route('/licence/robotique', methods=['GET', 'POST'])
def hist_robot():
	global matiere
	con = psycopg2.connect(database="Mabase", user = "KONE", password = "67749189", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute("SELECT * FROM robot")
	rows = cur.fetchall()
	con.close()
	if request.method == 'POST':
		matiere = 'Robotique'
		return redirect(url_for('emargement'))
	return render_template('robotique.html', ligne = rows)

@app.route('/licence/programmationpypthon', methods=['GET', 'POST'])
def hist_progpy():
	global matiere
	con = psycopg2.connect(database="Mabase", user = "KONE", password = "67749189", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS programmationpy (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
	cur.execute("SELECT * FROM programmationpy")
	rows = cur.fetchall()
	con.close()
	if request.method == 'POST':
		matiere = 'Programmation Python'
		return redirect(url_for('emargement'))
	return render_template('programmation.html', ligne = rows)
	

@app.route('/licence/emargement', methods=['GET', 'POST'])
def emargement():
	if request.method == 'POST':
		dates = request.form['dates']
		lecon = request.form['lecons']
		absent = request.form['absents']
		conn = psycopg2.connect(database="Mabase", user = "KONE", password = "67749189", host = "127.0.0.1", port = "5432")
		cur = conn.cursor()

		if matiere == 'Algorithmique':
			cur.execute('''CREATE TABLE IF NOT EXISTS algo (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
			cur.execute("INSERT INTO algo VALUES (%s,%s,%s)", (dates,lecon,absent))
			conn.commit()
			return redirect(url_for('hist_algo'))
		elif matiere == 'Robotique':
			cur.execute('''CREATE TABLE IF NOT EXISTS robot (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
			cur.execute("INSERT INTO robot VALUES (%s,%s,%s)", (dates,lecon,absent))
			conn.commit()
			return redirect(url_for('hist_robot'))
		elif matiere == 'Programmation Python':
			cur.execute('''CREATE TABLE IF NOT EXISTS programmationpy (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
			cur.execute("INSERT INTO programmationpy VALUES (%s,%s,%s)", (dates,lecon,absent))
			conn.commit()			
			return redirect(url_for('hist_progpy'))
		conn.close()
	return render_template('emargement.html', cour = matiere)

if __name__ == '__main__':
	app.run(debug=True)
