FROM python:3.11-alpine
WORKDIR /chatbot
COPY ./requeriments.txt /chatbot/requeriments.txt
COPY ./main.py /chatbot/main.txt
COPY ./rutas/formateo.py /chatbot/rutas/formateo.py
COPY ./rutas/manejador_acciones.py /chatbot/rutas/manejador_acciones.py

RUN pip install --no-cache-dir --upgrade -r /chatbot/requeriments.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]