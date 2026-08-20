import re

from agents.symptom_agent import symptom_agent
from agents.doctor_locator import doctor_locator_agent


class MultiAgentOrchestrator:

    def extract_specialist(self, text):

        specialist = ""
        reason = ""
        urgency = ""

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if line.lower().startswith("recommended specialist:"):
                specialist = line.split(":", 1)[1].strip()

            elif line.lower().startswith("specialist recommended:"):
                specialist = line.split(":", 1)[1].strip()

            elif line.lower().startswith("reason:"):
                reason = line.split(":", 1)[1].strip()

            elif line.lower().startswith("urgency:"):
                urgency = line.split(":", 1)[1].strip()

        return {
            "name": specialist,
            "reason": reason,
            "urgency": urgency
        }

    def process(self, symptoms, latitude, longitude):

        print("\n==============================")
        print("Agent 1 : Symptom Analysis")
        print("==============================")

        specialist_text = symptom_agent.analyze(symptoms)

        print("\n========== RAW AI RESPONSE ==========")
        print(specialist_text)
        print("=====================================")

        specialist = self.extract_specialist(specialist_text)

        print(specialist)

        print("\n==============================")
        print("Agent 2 : Nearby Hospitals")
        print("==============================")

        print("Searching hospitals...")
        print("Latitude:", latitude)
        print("Longitude:", longitude)
        hospitals = doctor_locator_agent.search(
        latitude,
        longitude
    )

        print("Hospital search finished.")

        print(f"Found {len(hospitals)} hospitals")

        print("\n==============================")
        print("Agent 3 : Hospital Recommendation")
        print("==============================")

        if hospitals:
            recommendation = {
                "hospital": hospitals[0]["name"],
                "reason": "Nearest available hospital."
            }
        else:
            recommendation = {
                "hospital": "No hospital found",
                "reason": "No nearby hospitals available."
            }

        print(recommendation)

        return {
            "specialist": specialist,
            "recommended_hospital": recommendation,
            "hospitals": hospitals
        }


orchestrator = MultiAgentOrchestrator()
