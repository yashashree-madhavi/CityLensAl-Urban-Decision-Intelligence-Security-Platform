import React from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useRouter } from "expo-router";

export default function Signup() {
  const router = useRouter();

  return (
    <View style={styles.container}>

      <Text style={styles.logo}>
        CITY<Text style={styles.accent}>LENS</Text>
      </Text>

      <Text style={styles.title}>Create Account</Text>

      <Text style={styles.subtitle}>
        Join CityLens and help make your city better
      </Text>

      <View style={styles.form}>

        <Text style={styles.label}>Full Name</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your full name"
          placeholderTextColor="#64768b"
        />

        <Text style={styles.label}>Mobile Number</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your mobile number"
          placeholderTextColor="#64768b"
          keyboardType="phone-pad"
        />

        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your email"
          placeholderTextColor="#64768b"
          keyboardType="email-address"
        />

        <TouchableOpacity
          style={styles.button}
          onPress={() => router.push("/otp")}
        >
          <Text style={styles.buttonText}>CONTINUE</Text>
        </TouchableOpacity>

      </View>

      <View style={styles.loginRow}>
        <Text style={styles.loginText}>
          Already have an account?
        </Text>

        <TouchableOpacity
          onPress={() => router.push("/login")}
        >
          <Text style={styles.loginLink}> Login</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity
        style={styles.back}
        onPress={() => router.back()}
      >
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#050d18",
    padding: 30,
    justifyContent: "center",
  },

  logo: {
    color: "#f4f7fb",
    fontSize: 27,
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 40,
  },

  accent: {
    color: "#14d8d2",
  },

  title: {
    color: "#f4f7fb",
    fontSize: 29,
    fontWeight: "700",
  },

  subtitle: {
    color: "#7c8da1",
    fontSize: 13,
    marginTop: 8,
    marginBottom: 25,
  },

  form: {
    width: "100%",
    maxWidth: 500,
    alignSelf: "center",
  },

  label: {
    color: "#b8c4d2",
    fontSize: 12,
    marginBottom: 8,
    marginTop: 12,
  },

  input: {
    height: 52,
    backgroundColor: "#0b1929",
    borderWidth: 1,
    borderColor: "#1d3046",
    borderRadius: 9,
    paddingHorizontal: 15,
    color: "#f4f7fb",
    fontSize: 14,
  },

  button: {
    height: 54,
    backgroundColor: "#13c9c5",
    borderRadius: 9,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 25,
  },

  buttonText: {
    color: "#031315",
    fontWeight: "800",
    letterSpacing: 1,
  },

  loginRow: {
    flexDirection: "row",
    justifyContent: "center",
    marginTop: 30,
  },

  loginText: {
    color: "#64768b",
    fontSize: 12,
  },

  loginLink: {
    color: "#14d8d2",
    fontSize: 12,
    fontWeight: "700",
  },

  back: {
    alignItems: "center",
    marginTop: 20,
  },

  backText: {
    color: "#64768b",
    fontSize: 12,
  },
});