FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    openjdk-17-jdk \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Установка buildozer
RUN pip3 install --upgrade pip && \
    pip3 install buildozer cython==0.29.33

WORKDIR /app

# Копируем файлы приложения
COPY . /app/

# Сборка APK
CMD ["buildozer", "android", "debug"]
