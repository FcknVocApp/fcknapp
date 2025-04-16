import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { API_URL } from '@env';

export default function TranslateScreen() {
  const [word, setWord] = useState('');
  const [translation, setTranslation] = useState(null);
  const [exampleEn, setExampleEn] = useState('');
  const [exampleRu, setExampleRu] = useState('');
  const [status, setStatus] = useState('');
  const [isSaved, setIsSaved] = useState(false);

  // Функция для перевода
  const handleTranslate = async () => {
    console.log('Отправляю запрос на перевод...');  // Лог перед отправкой запроса

    setStatus('⏳ Перевожу...');
    setIsSaved(false);

    try {
      // Отправка запроса на сервер
      const response = await fetch(`${API_URL}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word, tox_level: 'mama' }) // Передаем слово и уровень токсичности
      });

      const data = await response.json();

      // Лог ответа от сервера
      console.log('Ответ от сервера:', data);

      if (response.ok) {
        setTranslation(data.translation);
        setExampleEn(data.example_en);
        setExampleRu(data.example_ru);
        setStatus('✅ Успешно!');
      } else {
        setStatus('❌ Слово не найдено в базе');
      }
    } catch (error) {
      console.error('Ошибка при запросе:', error);  // Лог ошибок
      setStatus('⚠️ Ошибка соединения');
    }
  };

  // Функция для добавления в словарь
  const handleAdd = async () => {
    const payload = {
      word,
      translation,
      example_en: exampleEn,
      example_ru: exampleRu
    };
    try {
      const response = await fetch(`${API_URL}/add-from-translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (response.ok) {
        setStatus('💾 Слово добавлено в словарь');
        setIsSaved(true);
      } else {
        setStatus('⚠️ Не удалось сохранить');
      }
    } catch (error) {
      console.error('Ошибка при сохранении:', error);  // Лог ошибок
      setStatus('⚠️ Ошибка при сохранении');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Слово на перевод:</Text>
      <TextInput
        value={word}
        onChangeText={setWord}
        placeholder="например: burnout"
        style={styles.input}
      />
      <Button title="Перевести" onPress={handleTranslate} />

      {translation && (
        <View style={styles.result}>
          <Text style={styles.text}>🎯 Перевод: {translation}</Text>
          <Text style={styles.text}>🔥 EN: {exampleEn}</Text>
          <Text style={styles.text}>🔥 RU: {exampleRu}</Text>
          <Button
            title={isSaved ? "✅ Уже в словаре" : "💾 В словарь"}
            onPress={handleAdd}
            disabled={isSaved}
          />
        </View>
      )}

      <Text style={styles.status}>{status}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, flex: 1, backgroundColor: '#fff' },
  title: { fontSize: 18, fontWeight: '600', marginBottom: 10 },
  input: {
    borderColor: '#ccc',
    borderWidth: 1,
    marginBottom: 10,
    padding: 10,
    borderRadius: 5
  },
  result: { marginTop: 20 },
  text: { fontSize: 16, marginBottom: 5 },
  status: { marginTop: 20, fontStyle: 'italic', color: '#555' }
});