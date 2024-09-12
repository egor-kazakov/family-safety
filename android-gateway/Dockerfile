FROM python:3.12-alpine
RUN apk --no-cache add android-tools
WORKDIR /app
COPY . .
RUN pip install prometheus-client
EXPOSE 5037
EXPOSE 8000
CMD ["python3", "main.py"]
