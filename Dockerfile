FROM python:3.11-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install poetry

RUN git clone --depth 1 https://github.com/kamesan1577/geek-camp-vol8.git
WORKDIR /src/geek-camp-vol8
ENV PYTHONPATH="/src/geek-camp-vol8/"

RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# start discord server 
ENTRYPOINT ["poetry", "run", "python3", "/src/geek-camp-vol8/discord_memo/main.py" ]
