# Usa a imagem base oficial do Debian
FROM debian:latest

# Mantenedor do Dockerfile
LABEL maintainer="seuemail@example.com"

# Evita perguntas ao usar apt-get
ENV DEBIAN_FRONTEND noninteractive

# Instalação e configuração inicial do CouchDB
RUN apt-get update && \
    apt-get install -y debconf-utils curl apt-transport-https gnupg && \
    echo "couchdb couchdb/mode select standalone" | debconf-set-selections && \
    echo "couchdb couchdb/bindaddress string 127.0.0.1" | debconf-set-selections && \
    echo "couchdb couchdb/adminpass password teste" | debconf-set-selections && \
    echo "couchdb couchdb/adminpass_again password teste" | debconf-set-selections && \
    echo "couchdb couchdb/cookie string teste" | debconf-set-selections && \
    curl https://couchdb.apache.org/repo/keys.asc | gpg --dearmor | tee /usr/share/keyrings/couchdb-archive-keyring.gpg >/dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/couchdb-archive-keyring.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ $(. /etc/os-release; echo $VERSION_CODENAME) main" | \
    tee /etc/apt/sources.list.d/couchdb.list && \
    apt-get update && \
    apt-get install -y couchdb

# Instalação do Python e outras ferramentas
RUN apt-get update && \
    apt-get install -y python3-full python3-pip pandoc curl wget git texlive-fonts-extra texlive-xetex unzip && \
    rm /usr/lib/python3.11/EXTERNALLY-MANAGED && \
    pip install couchdb flask

# Clona o repositório e move o template para o diretório do Pandoc
RUN git clone https://github.com/Wandmalfarbe/pandoc-latex-template.git && \
    mv pandoc-latex-template/eisvogel.tex /usr/share/pandoc/data/templates/ && \
    rm -rf pandoc-latex-template

# Copia os scripts para o container
COPY add-view.sh /usr/local/bin/add-view.sh
COPY run-apps.sh /usr/local/bin/run-apps.sh

# Dá permissão de execução aos scripts
RUN chmod +x /usr/local/bin/add-view.sh /usr/local/bin/run-apps.sh

# Expõe a porta 80
EXPOSE 80

# Define o script run-apps.sh como ponto de entrada
ENTRYPOINT ["/usr/local/bin/run-apps.sh"]
