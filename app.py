from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configuração de acesso ao seu MySQL
def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Usuário padrão
        password="root",          # Sua senha do MySQL (deixe vazio "" se não tiver)
        database="calculadora" # Nome exato do seu banco de dados
    )

@app.route('/')
def home():
    # Puxa os últimos 5 cálculos salvos para exibir ao carregar a página
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT num1, operacao, num2, resultado FROM historico ORDER BY id DESC LIMIT 5")
    historico_dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    return render_template('index.html', resultado=None, historico=historico_dados)

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operacao = request.form['operacao']
        
        # Faz a operação com base na escolha do usuário
        if operacao == 'soma': 
            resultado = str(num1 + num2)
            sinal = "+"
        elif operacao == 'subtracao': 
            resultado = str(num1 - num2)
            sinal = "-"
        elif operacao == 'multiplicacao': 
            resultado = str(num1 * num2)
            sinal = "*"
        elif operacao == 'divisao':
            if num2 != 0:
                resultado = str(num1 / num2)
                sinal = "/"
            else:
                resultado = "Erro: Divisão por zero!"
                sinal = "/"
        else: 
            resultado = "Operação inválida"
            sinal = "?"
            
    except ValueError:
        resultado = "Erro: Digite números válidos!"
        sinal = "?"

    # Se o cálculo funcionou e não deu erro, grava no MySQL
    if "Erro" not in resultado:
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            comando_sql = "INSERT INTO historico (num1, operacao, num2, resultado) VALUES (%s, %s, %s, %s)"
            # Salvamos o sinal matemático (+, -, *, /) para ficar mais bonito na tela
            valores = (num1, sinal, num2, resultado)
            
            cursor.execute(comando_sql, valores)
            conexao.commit() 
            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Erro ao salvar no banco: {e}")

    # Puxa o histórico atualizado para recarregar a tela
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT num1, operacao, num2, resultado FROM historico ORDER BY id DESC LIMIT 5")
    historico_dados = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template('index.html', resultado=resultado, historico=historico_dados)

if __name__ == '__main__':
    app.run(debug=True)
