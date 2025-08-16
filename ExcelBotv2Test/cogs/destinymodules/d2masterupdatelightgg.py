def masterlistupdate():
	'''
	Updates the master.csv file of legendaries from light.gg
	'''
	from requests import get
	from bs4 import BeautifulSoup
	import pandas as pd
	import string
	from time import sleep
	from random import randint
	#from IPython.display import clear_output

	#initializing dataframe
	columns= ['Name','PvX','Weap Type','Archetype','Perk 1', 'Perk 2', 'Perk 3', 'Perk 4']
	df = pd.DataFrame(columns=columns)

	url = 'https://www.light.gg/db/category/1?etc=weapons&page=1&f=4%285%29'
	response = get(url)
	page_html_soup = BeautifulSoup(response.text, 'html.parser')
	maxpageno = int(page_html_soup.find('a', class_='last').get('href').split('/db/category/1?page=')[1].split('&f=4(5)')[0]) + 1

	i=0
	for page in range(1,maxpageno):
		page_url = 'https://www.light.gg/db/category/1?page=' + str(page) +'&f=4(5)'
		response = get(page_url)
		page_html_soup = BeautifulSoup(response.text,'html.parser')
		rows  = page_html_soup.find_all('div', class_='legendary item-name')
		for row in rows:
			i+=1
			print(i)
			suffix_url = row.a.get('href')

			print(suffix_url)

			weapon_url = 'https://www.light.gg' + suffix_url
			response_weap = get(weapon_url)
			html_soup = BeautifulSoup(response_weap.text,'html.parser')

			#Weapon name
			name = html_soup.find('h2').text.strip().lower()

			#Weapon type
			weapon_type = html_soup.find('span',class_='weapon-type').text.split(' / ')[-1].rstrip()

			#Archetype
			archetype = html_soup.find('span',class_='pull-left').img.get('alt')

			#Finds the 4 columns: Perks(1,2,3,4)
			perkcolumns = html_soup.find_all('li',class_="random clearfix")

			if len(perkcolumns) == 0:
				continue
			if 'Item has recommended perks from the community' not in str(html_soup):
				continue

			#ADD a condition where if no random rolls are found then skip
			#ADD a condition where if no perks are recommended then skip
			pveperks = {'1':[],'2':[],'3':[],'4':[]}
			pvpperks = {'1':[],'2':[],'3':[],'4':[]}

			for no, perkcolumn in enumerate(perkcolumns,1):
				for perk in perkcolumn.find_all('li'):
					perkname = perk.find('div',class_="item show-hover random").img.get('alt')
					if 'class=\"pref\"' in str(perk):
						pveperks[str(no)].append(perkname)
						pvpperks[str(no)].append(perkname)
						#print(str(no) + '\t' + perkname + '\tPvE+PvP')
					if 'class=\"pref prefpve\"' in str(perk):
						pveperks[str(no)].append(perkname)
						#print(str(no) + '\t' + perkname + '\tPvE')
					if 'class=\"pref prefpvp\"' in str(perk):
						pvpperks[str(no)].append(perkname)
						#print(str(no) + '\t' + perkname + '\tPvP')


			if (pveperks['1'] == [] and pveperks['2'] == [] and pveperks['3'] == [] and pveperks['4'] == []) == False:
				df = df.append({'Name':name,'Weap Type' : weapon_type,'Archetype':archetype,
							'PvX': 'pve','Perk 1':pveperks['1'],'Perk 2':pveperks['2'],
						   'Perk 3':pveperks['3'],'Perk 4':pveperks['4']},ignore_index=True)
			if (pvpperks['1'] == [] and pvpperks['2'] == [] and pvpperks['3'] == [] and pvpperks['4'] == []) == False:
				df = df.append({'Name':name,'Weap Type' : weapon_type,'Archetype':archetype,
							'PvX': 'pvp','Perk 1':pvpperks['1'],'Perk 2':pvpperks['2'],
						   'Perk 3':pvpperks['3'],'Perk 4':pvpperks['4']},ignore_index=True)
			sleep(randint(5,10))

			df.to_csv('Master.csv',index=False)