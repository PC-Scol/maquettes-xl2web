FROM python:3.13-bookworm

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/PC-Scol/maquettes-xl2web /usr/src/app

WORKDIR /usr/src/app

RUN git submodule init && git submodule update

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0"]
