#!/bin/bash

echo "📚 Получаю слово для квиза..."

RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/quiznow \
  -H "Content-Type: application/json" \
  -d '{"count": 1, "only_mistakes": false}')

echo "🔎 Ответ от сервера:"
echo "$RESPONSE"

if [[ "$RESPONSE" == "[]" || -z "$RESPONSE" ]]; then
  echo "⚠️  Нет доступных слов для квиза. Добавь хотя бы одно слово."
  exit 1
fi

ID=$(echo $RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
WORD=$(echo $RESPONSE | grep -o '"word":"[^"]*"' | cut -d':' -f2 | tr -d '"')
OPTIONS=$(echo $RESPONSE | grep -o '"options":\[[^]]*\]' | sed 's/"options":\[//' | tr -d '[]"')

echo ""
echo "👉 Слово: $WORD"
echo "❓ Варианты перевода:"
IFS=',' read -ra VARIANTS <<< "$OPTIONS"
for i in "${!VARIANTS[@]}"; do
  echo "$((i+1)). ${VARIANTS[i]}"
done

echo ""
read -p "Введи перевод (копируй): " ANSWER

CHECK=$(curl -s -X POST http://127.0.0.1:8000/quiznow/check \
  -H "Content-Type: application/json" \
  -d '{"id": '"$ID"', "answer": "'"$ANSWER"'"}')

echo ""
echo "🧠 Результат:"
echo $CHECK | jq
