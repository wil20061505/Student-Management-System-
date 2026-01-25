FROM python:3.10-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . .
ENV PYTHONPATH=/app

CMD ["python", "Menu/main.py"]