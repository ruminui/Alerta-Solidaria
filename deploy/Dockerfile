FROM python:3.13-slim
WORKDIR /app
COPY app/ ./app/
COPY backend/ ./backend/
ENV PYTHONDONTWRITEBYTECODE=1 AS_HOST=0.0.0.0 AS_PORT=8765 AS_DB=/data/alerta.sqlite
EXPOSE 8765
VOLUME /data
# Unsafe for public internet without external controls; pilot only.
CMD ["python","backend/server.py"]
