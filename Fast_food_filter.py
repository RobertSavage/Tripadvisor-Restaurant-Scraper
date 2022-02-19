emails = []
listcount = 0

Text_file = open('Tennessee_urls.txt','r')

for i in Text_file:
	
	if 'sonic' in i.lower():
		continue
	elif 'dominos' in i.lower():
		continue
	elif 'subway' in i.lower():
		continue
	elif 'mcdonald' in i.lower():
		continue
	elif 'applebee' in i.lower():
		continue
	elif 'waffle_house' in i.lower():
		continue
	elif 'dairy_queen' in i.lower():
		continue
	elif 'wendy' in i.lower():
		continue
	elif 'taco_bell' in i.lower():
		continue
	elif 'kfc' in i.lower():
		continue
	elif 'chick_fil_a' in i.lower():
		continue
	elif 'five_guy' in i.lower():
		continue
	elif 'arby' in i.lower():
		continue
	elif 'mcalister' in i.lower():
		continue
	elif 'olive_garden' in i.lower():
		continue
	elif 'zaxby' in i.lower():
		continue
	elif 'olympic_steak_house' in i.lower():
		continue
	elif 'pizza_hut' in i.lower():
		continue
	elif 'captain_d' in i.lower():
		continue
	elif 'burger_king' in i.lower():
		continue
	elif 'jimmy_john' in i.lower():
		continue
	elif 'popeyes' in i.lower():
		continue
	elif 'starbucks' in i.lower():
		continue
	elif 'denny' in i.lower():
		continue
	else:
		Email_list = open('URLS_nofastfood.txt','a')
		Email_list.write(str(i))
	
print('done')
'''
list of places i need to add


'''