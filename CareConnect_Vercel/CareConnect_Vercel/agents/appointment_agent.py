from services.gemini import ask_gemini


class AppointmentAgent:

    def get_appointment_details(self, hospital_name):

        prompt = f"""
You are an AI Appointment Assistant.

Search for the hospital below and provide the latest information.

Hospital:
{hospital_name}

Return ONLY in this format:

Hospital:
Phone:
Email:
Booking Website:
Appointment Process:
"""

        return ask_gemini(prompt)


appointment_agent = AppointmentAgent()