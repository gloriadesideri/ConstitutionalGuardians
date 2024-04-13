FROM python:3.10.8-slim
LABEL description="Uncensored model inference"
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
# RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 6000
CMD ["python", "-m", "dotenv", "-f", ".env", "app.py"]
