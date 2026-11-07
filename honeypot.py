import socket
from datetime import datetime

PORTA = 8000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", PORTA))
servidor.listen()
print(f"Honeypot escutando na porta {PORTA}... (Ctrl+C para parar)")

pagina = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head><title>Painel Administrativo</title></head>
<body>
  <h2>Acesso restrito - Area Administrativa</h2>
  <form method="POST">
    Usuario: <input name="usuario"><br><br>
    Senha: <input name="senha" type="password"><br><br>
    <button>Entrar</button>
  </form>
</body>
</html>
"""

while True:
    try:
        conexao, endereco = servidor.accept()
        ip = endereco[0]
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        conexao.settimeout(0.5)      # espera no máximo 0.5s por cada pedaço
        dados = b""                  # começa vazio (b"" = bytes vazios)
        try:
            while True:
                pedaco = conexao.recv(2048)
                if not pedaco:
                    break            # o outro lado fechou
                dados += pedaco      # junta os pedaços
        except socket.timeout:
            pass                     # parou de chegar dado: seguimos

        dados = dados.decode(errors="ignore")

        print(f"[{agora}] Conexao de {ip}")

        with open("registros.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{agora}] IP: {ip}\n")
            arquivo.write(dados)
            arquivo.write("\n----------------------------------------\n")

        conexao.sendall(pagina.encode())
        conexao.close()
    except Exception as erro:
        print(f"Erro numa conexao (ignorado): {erro}")

  