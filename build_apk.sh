#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║           💜 СБОРКА ANDROID APK ПРИЛОЖЕНИЯ ДЕЛЬТЫ 💜                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Проверка что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: Запусти скрипт из папки android_app!"
    exit 1
fi

# Проверка установки buildozer
if ! command -v buildozer &> /dev/null; then
    echo "📦 Buildozer не установлен. Устанавливаю..."
    pip3 install buildozer cython
fi

echo "🔧 Проверка зависимостей..."
echo ""

# Проверка Java
if ! command -v java &> /dev/null; then
    echo "⚠️  Java не установлена!"
    echo "Установи: sudo apt install openjdk-11-jdk"
    exit 1
fi

echo "✅ Java установлена"

# Проверка необходимых пакетов
echo "📦 Проверка системных пакетов..."

REQUIRED_PACKAGES="build-essential git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libffi-dev libssl-dev"

for package in $REQUIRED_PACKAGES; do
    if ! dpkg -l | grep -q "^ii  $package"; then
        echo "⚠️  Пакет $package не установлен"
        echo "Установи: sudo apt install $package"
        exit 1
    fi
done

echo "✅ Все системные пакеты установлены"
echo ""

# Очистка предыдущей сборки (опционально)
read -p "🗑️  Очистить предыдущую сборку? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Очистка..."
    buildozer android clean
fi

echo ""
echo "🚀 НАЧИНАЮ СБОРКУ APK..."
echo ""
echo "⏱️  Это может занять 20-40 минут при первой сборке"
echo "    (скачивается Android SDK ~2-3 ГБ)"
echo ""
echo "☕ Можешь пойти попить чай..."
echo ""

# Сборка APK
buildozer android debug

# Проверка результата
if [ -f "bin/deltaapp-0.1-debug.apk" ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                    ✅ СБОРКА ЗАВЕРШЕНА! ✅                           ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📱 APK файл создан:"
    echo "   $(pwd)/bin/deltaapp-0.1-debug.apk"
    echo ""
    
    # Размер файла
    SIZE=$(du -h bin/deltaapp-0.1-debug.apk | cut -f1)
    echo "📦 Размер: $SIZE"
    echo ""
    
    echo "📥 ЧТО ДАЛЬШЕ:"
    echo ""
    echo "1️⃣  Скопируй APK на телефон:"
    echo "    adb install bin/deltaapp-0.1-debug.apk"
    echo ""
    echo "2️⃣  Или отправь через Telegram бота:"
    echo "    Обнови telegram_cluster_bot.py"
    echo ""
    echo "3️⃣  Или скачай файл и установи вручную"
    echo ""
    echo "💜 Дельта готова к установке на Android!"
    echo ""
else
    echo ""
    echo "❌ ОШИБКА СБОРКИ!"
    echo ""
    echo "Проверь логи выше для деталей."
    echo ""
    echo "💡 ЧАСТЫЕ ПРОБЛЕМЫ:"
    echo "   • Не хватает места на диске (нужно ~5 ГБ)"
    echo "   • Не установлены зависимости"
    echo "   • Проблемы с интернетом при скачивании SDK"
    echo ""
    exit 1
fi
