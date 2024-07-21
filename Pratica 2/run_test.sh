#!/bin/bash

# Iniciar o servidor em segundo plano
python3 server.py &
SERVER_PID=$!
echo "Servidor iniciado com PID $SERVER_PID"
sleep 2

nota=0
total_tests=5

echo "Teste 1"
# Função para simular o cliente tentando adivinhar o número e acertando
simulate_client_guess() {
  python3 client.py <<EOF
1
10
QUIT
EOF
}

# Função para simular o cliente desistindo antes de acertar o número
simulate_client_quit() {
  python3 client.py <<EOF
QUIT
EOF
}

# Função para simular o cliente dando dois palpites e desistindo
simulate_client_two_guesses_and_quit() {
  python3 client.py <<EOF
20
25
QUIT
EOF
}

# Função para simular dois clientes sequenciais
simulate_two_clients_sequentially() {
  python3 client.py <<EOF > client_output_simultaneous_1.txt
QUIT
EOF

  sleep 2

  python3 client.py <<EOF > client_output_simultaneous_2.txt
30
35
99
77
39
50
EOF
}

# Função para simular três clientes sequenciais com palpites variados
simulate_three_clients_sequentially() {
  python3 client.py <<EOF > client_output_three_1.txt
55
65
60
EOF

  sleep 2

  python3 client.py <<EOF > client_output_three_2.txt
65
75
70
EOF

  sleep 2

  python3 client.py <<EOF > client_output_three_3.txt
75
85
80
EOF
}

# Executar o cliente (tentativa de adivinhar) e redirecionar a saída para um arquivo
simulate_client_guess > client_output_guess.txt

# Esperar um momento para garantir que todas as mensagens foram trocadas
sleep 2

# Verificar se a saída do cliente está correta (tentativa de adivinhar)
if grep -q "Adivinhe o número entre 1 e 100" client_output_guess.txt &&
   grep -q "Acima" client_output_guess.txt &&
   grep -q "Igual" client_output_guess.txt; then
  echo "Teste de adivinhar passou"
  nota=$((nota + 1))
else
  echo "Teste de adivinhar falhou"
fi

echo "Teste 2"
# Executar o cliente (desistência) e redirecionar a saída para um arquivo
simulate_client_quit > client_output_quit.txt

# Esperar um momento para garantir que todas as mensagens foram trocadas
sleep 2

# Verificar se a saída do cliente está correta (desistência)
if grep -q "Adivinhe o número entre 1 e 100" client_output_quit.txt &&
   grep -q "QUIT" client_output_quit.txt; then
  echo "Teste de desistência passou"
  nota=$((nota + 1))
else
  echo "Teste de desistência falhou"
fi

echo "Teste 3"
# Executar o cliente (dois palpites e desistência) e redirecionar a saída para um arquivo
simulate_client_two_guesses_and_quit > client_output_two_guesses_quit.txt

# Esperar um momento para garantir que todas as mensagens foram trocadas
sleep 2

# Verificar se a saída do cliente está correta (dois palpites e desistência)
if grep -q "Adivinhe o número entre 1 e 100" client_output_two_guesses_quit.txt &&
   grep -q "Acima" client_output_two_guesses_quit.txt &&
   grep -q "QUIT" client_output_two_guesses_quit.txt; then
  echo "Teste de dois palpites e desistência passou"
  nota=$((nota + 1))
else
  echo "Teste de dois palpites e desistência falhou"
fi

echo "Teste 4"
# Executar dois clientes sequencialmente para garantir a correta atribuição dos números
simulate_two_clients_sequentially

# Esperar um momento para garantir que todas as mensagens foram trocadas
sleep 2

# Verificar se a saída dos clientes está correta (sequencial)
if grep -q "Adivinhe o número entre 1 e 100" client_output_simultaneous_1.txt &&
   grep -q "QUIT" client_output_simultaneous_1.txt &&
   grep -q "Adivinhe o número entre 1 e 100" client_output_simultaneous_2.txt &&
   grep -q "Igual" client_output_simultaneous_2.txt; then
  echo "Teste de dois clientes sequenciais passou"
  nota=$((nota + 1))
else
  echo "Teste de dois clientes sequenciais falhou"
fi

echo "Teste 5"
# Executar três clientes sequenciais para garantir a correta atribuição dos números
simulate_three_clients_sequentially

# Esperar um momento para garantir que todas as mensagens foram trocadas
sleep 2

# Verificar se a saída dos clientes está correta (sequencial)
if grep -q "Adivinhe o número entre 1 e 100" client_output_three_1.txt &&
   grep -q "Igual" client_output_three_1.txt &&
   grep -q "Adivinhe o número entre 1 e 100" client_output_three_2.txt &&
   grep -q "Igual" client_output_three_2.txt &&
   grep -q "Adivinhe o número entre 1 e 100" client_output_three_3.txt &&
   grep -q "Igual" client_output_three_3.txt; then
  echo "Teste de três clientes sequenciais passou"
  nota=$((nota + 1))
else
  echo "Teste de três clientes sequenciais falhou"
fi

# Encerrar o servidor
kill $SERVER_PID
echo "Servidor encerrado"

# Apagar os arquivos de saída do cliente
rm client_output_guess.txt client_output_quit.txt client_output_two_guesses_quit.txt client_output_simultaneous_1.txt client_output_simultaneous_2.txt client_output_three_1.txt client_output_three_2.txt client_output_three_3.txt

# Calcular a nota final
nota_final=$((nota * 10 / total_tests))

echo "******************************************"
echo "Nota final: $nota_final/10"
echo "******************************************"
