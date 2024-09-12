FROM python:3.12-alpine
RUN apk --no-cache add adb
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5037
EXPOSE 8000
CMD ["python3", "main.py"]
