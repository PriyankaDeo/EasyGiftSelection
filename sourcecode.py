#!/usr/bin/python

import requests
import json
import itertools 
import sys

category = ['boots', 'clothing', 'shoes']			#Categories of items. Can be taken as input from user
KEY = '12c3302e49b9b40ab8a222d7cf79a69ad11ffd78'   #KEY for Api access

filtered_data = {}
url_data = {}
cnt = input('Enter number of items: ');		#Number of gifts
ttl = input('Enter total of items: ');		#Total cost of gifts

def get_items(json_data, key):				#Function to parse json 
    if type(json_data) is dict:
        for item_key in json_data:
            if type(json_data[item_key]) in (list, dict):
                get_items(json_data[item_key], key)
            elif item_key == key:
                #print json_data[item_key]
                perform_operation(json_data[item_key], json_data['price'], json_data['productUrl'])
    if type(json_data) == str:
        json_data = json.loads(json_data)
    elif type(json_data) is list:
        for item in json_data:
            if type(item) in (list, dict):
                get_items(item, key)
	
	
def perform_operation(pdId, prc, url):		#Function to store required items info
	if float(prc.split('$')[1]) < ttl:
		filtered_data[pdId] = float(prc.split('$')[1])	#Price of required items
		url_data[pdId] = url.replace("\\", "")	#Urls of the required items


def main():
    	try:
		for cat in category:
			url = 'http://api.zappos.com/Search?key=' + KEY + '&term=' + cat
			response = requests.get(url)		#make API call
			d1 = json.loads(response.text)
			get_items(d1, "productId")

		sorted_data = sorted(filtered_data, key = filtered_data.get)	#sort items on price
		list_items = []
		for subset in itertools.combinations(sorted_data, cnt):		#all possible cnt number of combinations of items
		#print subset
			total_items = 0
			for s in subset:
				vals = filtered_data[s]
				total_items += vals
			#print total_items
			if total_items >= ttl - 10 and total_items <= ttl + 10:		#total cost of items can be + or - 10 USD deviation
			#print total_items 
				list_items.append([total_items, subset])	#stores total of items and corresponding items productId
		print "The available items for your given cost total are: "
		if list_items:
			f = open('output.txt', 'w')
			for comb in list_items:		#display price and urls for criteria matching items 
				print comb[0]
				f.write(str(comb[0]) + '\n')
				for i in range(cnt):
					print url_data[(comb[1][i])]
					f.write(str(url_data[(comb[1][i])]) + '\n')
			f.close()
		else:
			print "No items can be found for your search criteria"
	except requests.ConnectionError as e:
		print "Cannot connect to Zappos. Try checking internet connection or using different key"
	except:
		print "Unexpected error occured: ", sys.exc_info()[0]
		raise


if __name__ == __main__:
	import sys; 
	main();
