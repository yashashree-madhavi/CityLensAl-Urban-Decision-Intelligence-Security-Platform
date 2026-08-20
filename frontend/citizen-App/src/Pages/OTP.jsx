import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useRouter, useLocalSearchParams } from "expo-router";

export default function OTP() {
  const router = useRouter();
  const params = useLocalSearchParams();

  const [otp, setOtp] = useState("");

  const verifyOTP = () => {
    if (otp === "123456") {
      router.replace("/dashboard");
    } else {
      alert("Invalid OTP. For testing use 123456.");
    }
  };

  return (
    <View style={styles.container}>

      <Text style={styles.logo}>
        CITY<Text style={styles.accent}>LENS</Text>
      </Text>

      <Text style={styles.title}>
        Verify Your Number
      </Text>

      <Text style={styles.subtitle}>
        Enter the 6-digit OTP sent to
      </Text>

      <Text style={styles.mobile}>
        {params.mobile || "your mobile number"}
      </Text>

      <TextInput
        style={styles.otpInput}
        placeholder="Enter OTP"
        placeholderTextColor="#64768b"
        keyboardType="number-pad"
        maxLength={6}
        value={otp}
        onChangeText={setOtp}
      />

      <TouchableOpacity
        style={styles.button}
        onPress={verifyOTP}
      >
        <Text style={styles.buttonText}>
          VERIFY OTP
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        onPress={() => router.back()}
        style={styles.back}
      >
        <Text style={styles.backText}>
          ← Change Number
        </Text>
      </TouchableOpacity>

      <Text style={styles.testText}>
        Demo OTP: 123456
      </Text>

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
    fontSize: 28,
    fontWeight: "800",
    marginBottom: 45,
  },

  accent: {
    color: "#14d8d2",
  },

  title: {
    color: "#f4f7fb",
    fontSize: 27,
    fontWeight: "700",
  },

  subtitle: {
    color: "#7c8da1",
    fontSize: 13,
    marginTop: 10,
  },

  mobile: {
    color: "#14d8d2",
    fontSize: 14,
    marginTop: 6,
    marginBottom: 25,
  },

  otpInput: {
    width: "100%",
    maxWidth: 400,
    height: 55,
    backgroundColor: "#0b1929",
    borderWidth: 1,
    borderColor: "#1d3046",
    borderRadius: 9,
    color: "#f4f7fb",
    textAlign: "center",
    fontSize: 22,
    letterSpacing: 8,
  },

  button: {
    width: "100%",
    maxWidth: 400,
    height: 54,
    backgroundColor: "#13c9c5",
    borderRadius: 9,
    justifyContent: "center",
    alignItems: "center",
    marginTop: 18,
  },

  buttonText: {
    color: "#031315",
    fontWeight: "800",
    letterSpacing: 1,
  },

  back: {
    marginTop: 20,
  },

  backText: {
    color: "#64768b",
    fontSize: 12,
  },

  testText: {
    color: "#475b70",
    fontSize: 10,
    marginTop: 25,
  },
});