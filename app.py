from flask import Flask, render_template,request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = conexao()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template("index.html", produtos=produtos)

@app.route("/add", methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        conn = conexao()
        conn.execute('INSERT INTO produtos (nome,categoria,quantidade,preco) values (?,?,?,?)', (nome,categoria,quantidade,preco))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route("/delete/<int:id>")
def delete_product(id):
    conn = conexao()
    conn.execute('DELETE FROM produtos where id = ?',(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = conexao()
    produto = conn.execute('SELECT * FROM produtos where id =?', (id)).fetchone()
    if request.method == 'POST' :
        nome = request.form['nome']
        categoria = request.form['categoria']
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        conn.execute('update produtos SET nome = ?, categoria = ?, quantidade = ?, preco = ?, where id = ?', (nome, categoria, quantidade, preco, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', produto=produto)




if __name__ == '__main__': 
    app.run(port=80, debug=True)







