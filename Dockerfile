FROM python:3.11.4
RUN mkdir /api
COPY ./app /api/app
COPY ./poetry.lock /api
COPY ./pyproject.toml /api
WORKDIR /api
RUN mkdir -p logs
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install
EXPOSE 9000
# CMD ["poetry", "run", "uvicorn", "--timeout-keep-alive", "120", "--workers", "4", "app:app", "--host", "0.0.0.0", "--port", "9000"]
