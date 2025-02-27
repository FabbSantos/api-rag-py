FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY requirements.txt .

RUN uv pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]