from services.maps import MapsService


class DoctorLocatorAgent:

    def search(self, latitude, longitude):

        hospitals = MapsService.nearby_hospitals(
            latitude,
            longitude
        )

        return hospitals


doctor_locator_agent = DoctorLocatorAgent()