import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from "react-native";
import { useRouter } from "expo-router";

export default function Dashboard() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>

        {/* HEADER */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Good Morning</Text>
            <Text style={styles.name}>Welcome to CityLens</Text>
          </View>

          <TouchableOpacity style={styles.notification}>
            <Text>🔔</Text>
          </TouchableOpacity>
        </View>

        {/* FLOOD RISK */}
        <View style={styles.riskCard}>
          <View>
            <Text style={styles.cardLabel}>CURRENT CITY RISK</Text>
            <Text style={styles.riskTitle}>Low Risk</Text>
            <Text style={styles.cardText}>
              No major flood alerts in your area.
            </Text>
          </View>

          <View style={styles.riskCircle}>
            <Text style={styles.riskPercent}>18%</Text>
            <Text style={styles.riskSmall}>Risk</Text>
          </View>
        </View>

        {/* REPORT BUTTON */}
        <TouchableOpacity style={styles.reportButton}>
          <Text style={styles.reportIcon}>+</Text>

          <View>
            <Text style={styles.reportTitle}>
              Report an Issue
            </Text>

            <Text style={styles.reportSubtitle}>
              Help improve your city
            </Text>
          </View>
        </TouchableOpacity>

        {/* QUICK SERVICES */}
        <Text style={styles.sectionTitle}>Quick Access</Text>

        <View style={styles.grid}>

          <TouchableOpacity style={styles.serviceCard}>
            <Text style={styles.serviceIcon}>🌊</Text>
            <Text style={styles.serviceTitle}>Flood Risk</Text>
            <Text style={styles.serviceText}>Check risk</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.serviceCard}>
            <Text style={styles.serviceIcon}>🔔</Text>
            <Text style={styles.serviceTitle}>Alerts</Text>
            <Text style={styles.serviceText}>View alerts</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.serviceCard}>
            <Text style={styles.serviceIcon}>📋</Text>
            <Text style={styles.serviceTitle}>My Reports</Text>
            <Text style={styles.serviceText}>Track reports</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.serviceCard}>
            <Text style={styles.serviceIcon}>📍</Text>
            <Text style={styles.serviceTitle}>Nearby</Text>
            <Text style={styles.serviceText}>City services</Text>
          </TouchableOpacity>

        </View>

        {/* RECENT ALERT */}
        <Text style={styles.sectionTitle}>Latest Alert</Text>

        <View style={styles.alertCard}>
          <View style={styles.alertIcon}>
            <Text>⚠</Text>
          </View>

          <View style={{ flex: 1 }}>
            <Text style={styles.alertTitle}>
              Heavy Rainfall Expected
            </Text>

            <Text style={styles.alertText}>
              Moderate rainfall is expected in your area.
            </Text>

            <Text style={styles.alertTime}>
              Updated 10 minutes ago
            </Text>
          </View>
        </View>

      </ScrollView>

      {/* BOTTOM NAVIGATION */}
      <View style={styles.bottomNav}>

        <TouchableOpacity style={styles.navItem}>
          <Text style={styles.navIcon}>⌂</Text>
          <Text style={styles.navActive}>Home</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.navItem}>
          <Text style={styles.navIcon}>🗺</Text>
          <Text style={styles.navText}>Map</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.navItem}>
          <Text style={styles.navIcon}>📋</Text>
          <Text style={styles.navText}>Reports</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.navItem}>
          <Text style={styles.navIcon}>👤</Text>
          <Text style={styles.navText}>Profile</Text>
        </TouchableOpacity>

      </View>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#050d18",
  },

  header: {
    padding: 25,
    paddingTop: 45,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  greeting: {
    color: "#7c8da1",
    fontSize: 12,
  },

  name: {
    color: "#f4f7fb",
    fontSize: 22,
    fontWeight: "700",
    marginTop: 5,
  },

  notification: {
    width: 42,
    height: 42,
    borderRadius: 9,
    backgroundColor: "#0b1929",
    borderWidth: 1,
    borderColor: "#1d3046",
    alignItems: "center",
    justifyContent: "center",
  },

  riskCard: {
    marginHorizontal: 25,
    padding: 20,
    borderRadius: 12,
    backgroundColor: "#091725",
    borderWidth: 1,
    borderColor: "#172c40",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  cardLabel: {
    color: "#64768b",
    fontSize: 10,
  },

  riskTitle: {
    color: "#29d27b",
    fontSize: 24,
    fontWeight: "700",
    marginTop: 5,
  },

  cardText: {
    color: "#7c8da1",
    fontSize: 11,
    marginTop: 5,
    maxWidth: 210,
  },

  riskCircle: {
    width: 75,
    height: 75,
    borderRadius: 40,
    borderWidth: 5,
    borderColor: "#29d27b",
    alignItems: "center",
    justifyContent: "center",
  },

  riskPercent: {
    color: "#f4f7fb",
    fontSize: 16,
    fontWeight: "700",
  },

  riskSmall: {
    color: "#64768b",
    fontSize: 9,
  },

  reportButton: {
    marginHorizontal: 25,
    marginTop: 15,
    padding: 17,
    backgroundColor: "#13c9c5",
    borderRadius: 10,
    flexDirection: "row",
    alignItems: "center",
  },

  reportIcon: {
    fontSize: 28,
    color: "#031315",
    marginRight: 15,
  },

  reportTitle: {
    color: "#031315",
    fontSize: 15,
    fontWeight: "800",
  },

  reportSubtitle: {
    color: "#164f50",
    fontSize: 10,
    marginTop: 3,
  },

  sectionTitle: {
    color: "#f4f7fb",
    fontSize: 16,
    fontWeight: "700",
    marginHorizontal: 25,
    marginTop: 25,
    marginBottom: 12,
  },

  grid: {
    flexDirection: "row",
    flexWrap: "wrap",
    paddingHorizontal: 20,
    gap: 10,
  },

  serviceCard: {
    width: "47%",
    backgroundColor: "#091725",
    borderWidth: 1,
    borderColor: "#172c40",
    borderRadius: 10,
    padding: 16,
  },

  serviceIcon: {
    fontSize: 22,
  },

  serviceTitle: {
    color: "#f4f7fb",
    fontSize: 13,
    fontWeight: "700",
    marginTop: 10,
  },

  serviceText: {
    color: "#64768b",
    fontSize: 10,
    marginTop: 4,
  },

  alertCard: {
    marginHorizontal: 25,
    marginBottom: 30,
    padding: 15,
    backgroundColor: "#091725",
    borderWidth: 1,
    borderColor: "#172c40",
    borderRadius: 10,
    flexDirection: "row",
    gap: 12,
  },

  alertIcon: {
    width: 38,
    height: 38,
    borderRadius: 8,
    backgroundColor: "#48321a",
    alignItems: "center",
    justifyContent: "center",
  },

  alertTitle: {
    color: "#f4f7fb",
    fontSize: 12,
    fontWeight: "700",
  },

  alertText: {
    color: "#7c8da1",
    fontSize: 10,
    marginTop: 4,
  },

  alertTime: {
    color: "#64768b",
    fontSize: 8,
    marginTop: 7,
  },

  bottomNav: {
    height: 70,
    backgroundColor: "#071321",
    borderTopWidth: 1,
    borderTopColor: "#17283c",
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
  },

  navItem: {
    alignItems: "center",
  },

  navIcon: {
    fontSize: 18,
  },

  navActive: {
    color: "#14d8d2",
    fontSize: 9,
    marginTop: 3,
  },

  navText: {
    color: "#64768b",
    fontSize: 9,
    marginTop: 3,
  },
});