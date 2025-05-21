from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from usuario import Usuario 
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = "senha_muito_segura"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

bcrypt = Bcrypt(app)

def conexao():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if 'user_id' in session:
        conn = conexao()
        cursor = conn.cursor()
        produtos = cursor.execute("SELECT * FROM produtos").fetchall()
        conn.close()

        return render_template('index.html', produtos=produtos)  # <-- agora passa os dados
    else:
        return redirect(url_for('login', next=request.url))

    
@app.route("/add", methods=["GET", "POST"])
def add_product():
    if 'user_id' in session:
        if request.method == 'POST':
            nome = request.form['nome']
            categoria = request.form['categoria']
            quantidade = request.form['quantidade']
            preco = request.form['preco']

            conn = conexao()
            conn.execute(
                "INSERT INTO produtos (nome, categoria, quantidade, preco) VALUES (?, ?, ?, ?)",
                (nome, categoria, quantidade, preco)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
        else:
            return render_template("add.html")  # ✅ Mostra o formulário
    else:
        return redirect(url_for("login"))  # ✅ Redireciona para a rota do login




@app.route("/editar/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    if 'user_id' not in session:
        return redirect(url_for("login"))

    conn = conexao()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        cursor.execute("""
            UPDATE produtos 
            SET nome = ?, categoria = ?, quantidade = ?, preco = ?
            WHERE id = ?
        """, (nome, categoria, quantidade, preco, id))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    else:
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        produto = cursor.fetchone()
        conn.close()

        if produto:
            return render_template("editar.html", produto=produto)
        else:
            return "Produto não encontrado", 404

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        next_page = request.args.get('next')  # Captura a próxima página (se tiver)

        conn = conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = cursor.fetchone()
        conn.close()

        if user:
            usuario = Usuario(user[0], user[1], user[2])
            if bcrypt.check_password_hash(usuario.senha, senha):
                session['user_id'] = usuario.id
                session['username'] = usuario.login
                return redirect(url_for('welcome'))
            else:
                return render_template('login.html', mensagem="Usuário ou Senha incorreta")
        else:
            return render_template('login.html', mensagem="Usuário não registrado")
    else:
        return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html')


@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        login = request.form['login']
        senha_plana = request.form['senha']
        senha_hash = bcrypt.generate_password_hash(senha_plana).decode('utf-8')

        try:
            conn = conexao()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (login, senha) VALUES (?, ?)", (login, senha_hash))
            conn.commit()
            conn.close()
            return render_template("login.html", sucesso_mensagem="Usuário registrado com sucesso")
        except sqlite3.IntegrityError:
            conn.close
            return render_template("registro.html", mensagem="Usuário já registrado")
    else:
        return render_template("registro.html")
    
@app.route("/deletar/<int:id>")
def delete_product(id):
    if 'user_id' not in session:
        return redirect(url_for("login", next=request.url))

    conn = conexao()
    conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/bemVindo")
def bem_vindo():
    if 'user_id' not in session:
        return render_template("login.html", mensagem="Sessão expirada")
    return render_template("bemVindo.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=8070)
