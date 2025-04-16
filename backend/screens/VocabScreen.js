import React, { useEffect, useState } from 'react';
import { View, Text, Button, ScrollView } from 'react-native';
import api from '../services/api';

export default function VocabScreen() {
  const [words, setWords] = useState([]);

  const fetchWords = async () => {
    const res = await api.get('/mywords');
    setWords(res.data || []);
  };

  const handleDelete = async (word) => {
    await api.post('/delete', { word });
    fetchWords();
  };

  useEffect(() => {
    fetchWords();
  }, []);

  return (
    <ScrollView style={{ padding: 16 }}>
      {words.map((w, i) => (
        <View key={i} style={{ marginBottom: 8 }}>
          <Text>{w}</Text>
          <Button title="Delete" onPress={() => handleDelete(w)} />
        </View>
      ))}
    </ScrollView>
  );
}