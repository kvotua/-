FROM python:3.12-slim
WORKDIR /bot
COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir --upgrade poetry
RUN poetry install
COPY . .
CMD ["poetry", "run", "python", "main.py"]
