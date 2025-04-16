import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import api from '../services/api';

export default function QuizScreen() {
  const [quiz, setQuiz] = useState([]);

  useEffect(() => {
    api.get('/quiznow').then(res => {
      setQuiz(res.data || []);
    });
  }, []);

  return (
    <ScrollView style={styles.container}>
      {quiz.map((q, i) => (
        <View key={i} style={styles.questionBlock}>
          <Text style={styles.questionText}>{q.word}</Text>
          {q.choices?.map((c, j) => (
            <TouchableOpacity
              key={j}
              onPress={() => {}}
              style={styles.choiceButton}
            >
              <Text style={styles.choiceText}>{String(c)}</Text>
            </TouchableOpacity>
          ))}
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16
  },
  questionBlock: {
    marginBottom: 24,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderColor: '#ddd'
  },
  questionText: {
    fontSize: 18,
    marginBottom: 8
  },
  choiceButton: {
    backgroundColor: '#eee',
    padding: 10,
    borderRadius: 6,
    marginTop: 6
  },
  choiceText: {
    fontSize: 16
  }
});