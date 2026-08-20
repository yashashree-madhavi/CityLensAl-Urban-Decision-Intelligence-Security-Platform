import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useRouter } from "expo-router";

export default function Welcome() {
  const router = useRouter();

  return (
    <View style={styles.container}>

      <Text style={styles.logo}>
        CITY<Text style={styles.accent}>LENS</Text>
      </Text>

      <Text style={styles.title}>
        Welcome to CityLens
      </Text>

      <Text style={styles.subtitle}>
        Your city. Your voice. Your safety.
      </Text>

      <TouchableOpacity
        style={styles.button}
        onPress={() => router.push("/login")}
      >
        <Text style={styles.buttonText}>
          GET STARTED
        </Text>
      </TouchableOpacity>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#050d18",
    justifyContent: "center",
    alignItems: "center",
    padding: 30,
  },

  logo: {
    color: "#f4f7fb",
    fontSize: 34,
    fontWeight: "800",
    marginBottom: 45,
  },

  accent: {
    color: "#14d8d2",
  },

  title: {
    color: "#f4f7fb",
    fontSize: 30,
    fontWeight: "700",
    textAlign: "center",
  },

  subtitle: {
    color: "#7c8da1",
    fontSize: 14,
    marginTop: 10,
    marginBottom: 35,
    textAlign: "center",
  },

  button: {
    width: "100%",
    maxWidth: 400,
    height: 54,
    backgroundColor: "#13c9c5",
    borderRadius: 9,
    alignItems: "center",
    justifyContent: "center",
  },

  buttonText: {
    color: "#031315",
    fontSize: 14,
    fontWeight: "800",
    letterSpacing: 1,
  },
});