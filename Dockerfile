
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CHROME_BIN=/usr/bin/google-chrome

RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 dirmngr \
    fonts-liberation \
    libx11-6 libnss3 libxi6 libxcomposite1 \
    libasound2 libxtst6 libatk1.0-0 libgtk-3-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O /tmp/google-linux-signing-key.pub https://dl.google.com/linux/linux_signing_key.pub \
    && install -o root -g root -m 644 /tmp/google-linux-signing-key.pub /usr/share/keyrings/ \
    && sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.pub] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
