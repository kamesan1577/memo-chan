FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/src"

WORKDIR /src
RUN pip install poetry 

COPY pyproject.toml* poetry.lock* ./
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

COPY ./discord_memo /src/discord_memo
ENTRYPOINT ["poetry", "run", "python3", "/src/discord_memo/main.py" ]
