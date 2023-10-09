FROM python:3.11-alpine
WORKDIR /chatbot
COPY requeriments.txt .
RUN pip install -r requeriments.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]