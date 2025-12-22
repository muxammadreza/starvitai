import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { useState } from 'react';

export default function App() {
  const [glucose, setGlucose] = useState('');
  const [ketones, setKetones] = useState('');

  // GKI = (Glucose / 18.016) / Ketones (if Glucose in mg/dL)
  // Or Glucose / Ketones (if Glucose in mmol/L)
  // Assuming mmol/L for now as per Starvit metabolic focus
  // Wait, GKI metric usually requires consistent units.
  // Prompt says "GKI (glucose/ketones in mmol/L)".
  const gki = (parseFloat(glucose) || 0) / (parseFloat(ketones) || 1); 

  const submit = async () => {
    // API call stub
    console.log('Submitting', { glucose, ketones });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Starvit Patient</Text>
      
      <Text style={styles.label}>Glucose (mmol/L)</Text>
      <TextInput 
        value={glucose} 
        onChangeText={setGlucose} 
        style={styles.input} 
        keyboardType="numeric"
      />

      <Text style={styles.label}>Ketones (mmol/L)</Text>
      <TextInput 
        value={ketones} 
        onChangeText={setKetones} 
        style={styles.input} 
        keyboardType="numeric"
      />

      <Text style={styles.result}>GKI: {isNaN(gki) ? '-' : gki.toFixed(2)}</Text>
      
      <Button title="Log Measurement" onPress={submit} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 50, flex: 1, justifyContent: 'center' },
  header: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  label: { marginBottom: 5 },
  input: { borderWidth: 1, padding: 10, marginBottom: 20, borderRadius: 5 },
  result: { fontSize: 18, marginBottom: 20, textAlign: 'center' }
});
