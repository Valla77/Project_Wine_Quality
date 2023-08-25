FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y
# apt-get command linux. installation de logiciel

# RUN curl -fsSL https://get.deta.dev/cli.sh | sh
# -fsSL option curl

# RUN curl "https://awscli.amazoncd aws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# Invite de commande aws. Pour interagir avec aws. authentification
# RUN unzip awscliv2.zip
# RUN ./aws/install
# cherche script et install dans aws

COPY requirements.txt /dependencies/requirements.txt
# Il faut créer le folder dans le container
RUN pip install -r /dependencies/requirements.txt
#Intall toutes les librairies qui sont dans le fichier requirements


CMD streamlit run --server.port 4000 --server.address "0.0.0.0" app.py
