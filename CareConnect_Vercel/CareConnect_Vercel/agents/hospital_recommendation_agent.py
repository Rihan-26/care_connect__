from services.gemini import ask_gemini


class HospitalRecommendationAgent:

    def recommend(self, specialist, hospitals):

        if not hospitals:
            return {
                "recommended": None,
                "reason": "No hospitals found nearby."
            }

        hospital_names = "\n".join(
            [f"- {hospital['name']}" for hospital in hospitals]
        )

        prompt = f"""
You are an AI healthcare assistant.

The patient should consult a:

{specialist}

Nearby hospitals:

{hospital_names}

Instructions:

1. Recommend ONLY ONE hospital.
2. Explain why that hospital is the best choice.
3. If several hospitals are similar, choose the largest multi-specialty hospital.
4. Return EXACTLY in this format.

Hospital:
Reason:
"""

        response = ask_gemini(prompt)

        return response


hospital_recommendation_agent = HospitalRecommendationAgent()