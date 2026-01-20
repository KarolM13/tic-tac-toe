# Dockerfile dla aplikacji Kółko-Krzyżyk
FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki wymagań i zainstaluj zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę aplikacji
COPY . .

# Eksponuj port
EXPOSE 5555

# Zmienna środowiskowa dla Flask
ENV FLASK_APP=server.py

# Uruchom aplikację
CMD ["python", "server.py"]
