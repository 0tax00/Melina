#!/bin/bash

# Iniciar o serviço CouchDB
echo "Iniciando CouchDB..."
service couchdb start

# Espera um momento para o CouchDB iniciar completamente
sleep 10

# Executa o script para adicionar views ao CouchDB
echo "Adicionando views ao CouchDB..."
/usr/local/bin/add-view.sh

# Clona o repositório Melina e executa o app.py
echo "Clonando e iniciando o aplicativo Melina..."
git clone https://github.com/0tax00/Melina.git
cd Melina/melina
python3 app.py &

# Prevenir que o container encerre imediatamente
echo "Serviços iniciados. Mantendo o container em execução..."
tail -f /dev/null
