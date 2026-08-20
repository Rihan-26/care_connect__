from services.gemini import ask_gemini


class SymptomAgent:

    def analyze(self, symptoms):

        prompt = f"""
You are an experienced medical triage assistant.

Patient Symptoms:
{symptoms}

Recommend ONLY ONE most appropriate medical specialist.

Return your answer EXACTLY in the following format.

Recommended Specialist: <doctor>

Reason: <Explain in 2-3 sentences why this specialist is appropriate.>

Urgency: <Low / Medium / High>

Rules:
- Do not use Markdown.
- Do not use bullet points.
- Do not use headings.
- Do not write anything before or after the format.
- Always include all three fields.
"""

        return ask_gemini(prompt)


symptom_agent = SymptomAgent()