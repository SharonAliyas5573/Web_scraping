FROM python:3.9 
WORKDIR /app 
COPY . .
RUN pip install --no-cache-dir --upgrade -r  requirements.txt
WORKDIR /app/app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"] 
