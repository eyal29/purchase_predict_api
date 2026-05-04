FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Indispensable pour LightGBM
RUN apt update
RUN apt install libgomp1 -y

RUN mkdir /app
WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY app.py /app/app.py
COPY src/ /app/src/

RUN uv sync

EXPOSE 80

CMD ["uv", "run", "gunicorn", "app:app", "-b", "0.0.0.0:80", "-w", "4"]