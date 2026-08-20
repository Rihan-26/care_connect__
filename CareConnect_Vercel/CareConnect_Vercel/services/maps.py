import os
import math
import requests
from dotenv import load_dotenv

load_dotenv()


class MapsService:

    @staticmethod
    def get_coordinates(location):

        url = "https://api.geoapify.com/v1/geocode/search"

        params = {
            "text": location,
            "apiKey": os.getenv("GEOAPIFY_API_KEY")
        }

        try:

            response = requests.get(url, params=params)

            data = response.json()

            if not data.get("features"):
                return None

            coords = data["features"][0]["geometry"]["coordinates"]

            return coords[1], coords[0]

        except Exception as e:

            print("Geocoding Error:", e)

            return None

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):

        R = 6371

        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)

        a = (
            math.sin(dLat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dLon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return round(R * c, 2)

    @staticmethod
    def nearby_hospitals(user_lat, user_lon):

        api_key = os.getenv("GEOAPIFY_API_KEY")

        url = (
            f"https://api.geoapify.com/v2/places"
            f"?categories=healthcare.hospital"
            f"&filter=circle:{user_lon},{user_lat},10000"
            f"&bias=proximity:{user_lon},{user_lat}"
            f"&limit=20"
            f"&apiKey={api_key}"
        )

        try:

            response = requests.get(
                url,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

        except Exception as e:

            print("Geoapify Error:", e)

            return []

        hospitals = []

        for place in data.get("features", []):

            props = place.get("properties", {})

            lat = props.get("lat")
            lon = props.get("lon")

            if lat is None or lon is None:
                continue

            distance = MapsService.calculate_distance(
                user_lat,
                user_lon,
                lat,
                lon
            )

            hospitals.append({
                "id": len(hospitals) + 1,
                

                "name": props.get(
                    "name",
                    "Unknown Hospital"
                ),

                "address": props.get(
                    "formatted",
                    "Address Not Available"
                ),

                "latitude": lat,

                "longitude": lon,

                "distance": f"{distance} km",

                "phone": props.get(
                    "contact:phone",
                    "Not Available"
                ),

                "website": props.get(
                    "website",
                    "Not Available"
                ),

                "emergency": "Unknown"

            })

        hospitals.sort(
            key=lambda x: float(
                x["distance"].replace(" km", "")
            )
        )

        print("\n========== GEOAPIFY ==========")
        print("Hospitals Found:", len(hospitals))

        for h in hospitals[:5]:
            print(h)

        print("==============================\n")

        return hospitals