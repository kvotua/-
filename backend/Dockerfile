FROM python:3.12-slim
WORKDIR /code
RUN pip install --no-cache-dir --upgrade poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main
COPY . .
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
