# Honeypot de Login

Um honeypot simples em Python: um servidor que finge ser uma tela de login de administrador, atrai quem tenta acessar e **registra tudo** (data, hora, IP e o que a pessoa digita). Meu segundo projeto de segurança, e o primeiro do lado "defensor" (Blue Team).

## O que faz
- Fica escutando numa porta e responde com uma falsa página de login
- Lê a requisição HTTP inteira de quem conecta
- Grava num arquivo (`registros.txt`) a data, a hora, o IP e os dados enviados
- Aguenta várias conexões sem cair (tratamento de erros)

## Como usar
```bash
python honeypot.py
```
Depois acesse http://localhost:8000 no navegador.

## Como funciona
- Usa **sockets TCP no modo servidor**: `bind` (reserva a porta), `listen` (abre) e `accept` (atende quem conecta). É o contrário de um cliente, que usa `connect`.
- Lê os dados num **loop até o visitante parar de enviar**, porque o TCP é um fluxo e uma requisição pode chegar em vários pedaços. Foi isso que fez a captura funcionar mesmo através de um proxy.
- Responde uma página HTML com um formulário de login falso.

## O que eu aprendi
- A diferença entre o lado **cliente** e o lado **servidor** de um socket
- Que o **TCP é um fluxo de bytes**, não uma mensagem pronta: um único `recv` pode não trazer tudo
- Como **tratar erros** para um servidor não cair por causa de uma conexão ruim
- Que, atrás de um proxy/CDN, o **IP real** do visitante vem num cabeçalho (`Cf-Connecting-Ip`), não no socket
- Testei o honeypot pela internet com um **túnel (Cloudflare)** e capturei um acesso real vindo de outra rede

## Próximos passos
- [ ] Extrair usuário e senha limpos, em vez do pedido HTTP inteiro
- [ ] Registrar o IP real a partir do cabeçalho `Cf-Connecting-Ip`
- [ ] Rodar num servidor isolado (VPS) para analisar ataques reais

## Aviso
Projeto de estudo. Um honeypot deve ser usado apenas em ambiente controlado e **nunca** exposto a partir da sua máquina pessoal. O arquivo `registros.txt` é gerado ao rodar e não faz parte do repositório.

---
Feito por **Caio Santhiago Reis da Conceição** — estudante de Ciência da Computação (PUC Minas)
