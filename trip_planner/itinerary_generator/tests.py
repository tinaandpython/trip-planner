# from django.test import TestCase
import unittest
import requests
from django.conf import settings

# Create your tests here.
class TestTripPlannerAPI(unittest.TestCase):
    def test_trip_planner_api_consistency(self):
        url = "https://ai-trip-planner.p.rapidapi.com/"
        querystring = {"days": "2", "destination": "Paris"}
        headers = {
                "x-rapidapi-key": settings.RAPIDAPI_KEY,
                "x-rapidapi-host": settings.RAPIDAPI_HOST,
        }

        # Makes multiple requests to the API
        responses = [requests.get(url, headers=headers, params=querystring) for _ in range(5)]

        # Extracts JSON data from each response
        json_responses = [response.json() for response in responses]

        # Checks if all responses are identical
        all_identical = all(json_responses[i] == json_responses[i + 1] for i in range(len(json_responses) - 1))

        if all_identical:
            print("All API responses are identical.")
        else:
            print("API responses are NOT identical.")
            # Prints the differences if there are any
            for i in range(len(json_responses) - 1):
                if json_responses[i] != json_responses[i + 1]:
                    print(f"Difference between response {i} and response {i+1}:")
                    print(f"Response {i}: {json_responses[i]}")
                    print(f"Response {i+1}: {json_responses[i + 1]}")

        # Asserts that all responses are identical
        self.assertTrue(all_identical, "API responses are not identical")


if __name__ == "__main__":
    unittest.main()
