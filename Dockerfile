FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY ./ ./discord-memo

WORKDIR /src/discord-memo
ENV PYTHONPATH="/src/discord-memo/"

RUN pip install -r requirements.txt

# start discord server 
ENTRYPOINT ["python3", "/src/discord-memo/discord_memo/main.py" ]
