import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useRouter } from "expo-router";

export default function Login() {
  const router = useRouter();

  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");

  return (
    <View style={styles.container}>

      <Text style={styles.logo}>
        CITY<Text style={styles.accent}>LENS</Text>
      </Text>

      <Text style={styles.title}>Welcome Back</Text>

      <Text style={styles.subtitle}>
        Sign in to continue to CityLens
      </Text>

      <View style={styles.form}>

        <Text style={styles.label}>Mobile Number</Text>

        <TextInput
          style={styles.input}
          placeholder="Enter mobile number"
          placeholderTextColor="#64768b"
          keyboardType="phone-pad"
          value={mobile}
          onChangeText={setMobile}
        />

        <Text style={styles.label}>Password</Text>

        <TextInput
          style={styles.input}
          placeholder="Enter password"
          placeholderTextColor="#64768b"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        <TouchableOpacity
          style={styles.loginButton}
          onPress={() => router.push("/dashboard")}
        >
          <Text style={styles.loginText}>LOGIN</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.otpButton}
          onPress={() => router.push("/otp")}
        >
          <Text style={styles.otpText}>LOGIN WITH OTP</Text>
        </TouchableOpacity>

      </View>

      <View style={styles.signupRow}>
        <Text style={styles.signupText}>
          Don't have an account?
        </Text>

        <TouchableOpacity
          onPress={() => router.push("/signup")}
        >
          <Text style={styles.signupLink}> Sign Up</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity
        style={styles.back}
        onPress={() => router.replace("/")}
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
    fontSize: 28,
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 45,
  },

  accent: {
    color: "#14d8d2",
  },

  title: {
    color: "#f4f7fb",
    fontSize: 30,
    fontWeight: "700",
  },

  subtitle: {
    color: "#7c8da1",
    fontSize: 14,
    marginTop: 8,
    marginBottom: 30,
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
    marginTop: 15,
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

  loginButton: {
    height: 54,
    backgroundColor: "#13c9c5",
    borderRadius: 9,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 28,
  },

  loginText: {
    color: "#031315",
    fontWeight: "800",
    letterSpacing: 1,
  },

  otpButton: {
    height: 54,
    borderWidth: 1,
    borderColor: "#13c9c5",
    borderRadius: 9,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 12,
  },

  otpText: {
    color: "#13c9c5",
    fontWeight: "700",
    letterSpacing: 1,
  },

  signupRow: {
    flexDirection: "row",
    justifyContent: "center",
    marginTop: 35,
  },

  signupText: {
    color: "#64768b",
    fontSize: 12,
  },

  signupLink: {
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