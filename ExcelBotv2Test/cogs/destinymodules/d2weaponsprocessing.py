def processfiles(invfilename,mstrfilename='Master.csv'):
	import pandas as pd
	import numpy as np
	from nltk.corpus import stopwords

	#list of stopwords
	stop_words = list(set(stopwords.words('english')))

	#importing Master and inventory files
	raw_mster = pd.read_csv(mstrfilename)
	raw_inventory = pd.read_csv(invfilename)

	#copy files
	master = raw_mster.copy()
	inventory = raw_inventory.copy()

	#Processing master['Name']
	master['Name'] = master['Name'].apply(lambda x: x.lower())
	master['Name'] = master['Name'].apply(lambda x: x.split())
	master['Name'] = master['Name'].apply(lambda x: [word for word in x if word not in stop_words])
	master['Name'] = master['Name'].apply(lambda x: ' '.join(x))
	master['Name'] = master['Name'].apply(lambda x: ''.join(x.split('.')))
	master['Perklist'] = master['Perk 1'] + ', ' + master['Perk 2']
	master.fillna(value='-----',inplace=True)
	master['Archetype'] = master['Archetype'].apply(lambda x:x +' Frame' if ('Frame' not in x and '--' not in x and x != 'Aggressive') else x)
	master['Archetype'] = master['Archetype'].apply(lambda x:x +' Burst' if x == 'Aggressive' else x)
	master['Archetype'] = master['Archetype'].apply(lambda x:x +' Burst' if x == 'Aggressive' else x)
	master['Archetype'] = master['Archetype'].apply(lambda x: 'Häkke Precision Frame' if 'Hakke' in x else x)
 

	#Processing inventory['Name']
	inventory['Name'] = inventory['Name'].apply(lambda x: x.lower())
	inventory['Name'] = inventory['Name'].apply(lambda x: x.split())
	inventory['Name'] = inventory['Name'].apply(lambda x: [word for word in x if word not in stop_words])
	inventory['Name'] = inventory['Name'].apply(lambda x: ' '.join(x))
	inventory['Name'] = inventory['Name'].apply(lambda x: ''.join(x.split('.')))
	inventory.fillna(value='-----',inplace=True)
	inventory['Perkcheck'] = 0
	inventory['PvE?'] = 0
	inventory['PvP?'] = 0
	inventory['In Masterlist?'] = 'Y'
	for perkno in range(0,11):
		inventory['Perks ' + str(perkno)] = inventory['Perks ' + str(perkno)].apply(lambda x : x.strip('*'))

    #Copying files
	columnstodrop = ['Hash','Id','Tag','Source','Owner','Locked','Equipped','Year','Season','Event','DTR Rating','# of Reviews','Recoil','AA','Impact','Range','Blast Radius','Velocity','Stability','ROF','Reload','Mag','Equip','Charge Time','Draw Time','Accuracy','Notes']
	inventory.drop(labels=columnstodrop,axis=1,inplace=True)
	inv = inventory.copy()
	mster = master.copy()
	#inv.to_csv('inventoryprocessed.csv',index=False)
	#print('DONE')
	#print(len(inv.columns))
	return inv, mster

def comparison(mster,inv):
	import pandas as pd
	#Tier=4
	#Perkcheckcolumnno = 45
	#Namecolumnno = 0
	rows = len(inv)
	for i in range(rows):
		#print(i)

		#check if gun is legendary
		if str(inv.iloc[i]['Tier']) != 'Legendary':
			inv.iloc[i,inv.columns.get_loc('In Masterlist?')] = inv.iloc[i]['Tier']
			continue
		gun_name = inv.iloc[i]['Name']

		#check if gun is in the database
		if mster['Name'].str.contains(gun_name).any() == False and str(inv.iloc[i]['Tier']) == 'Legendary':
			inv.iloc[i,inv.columns.get_loc('In Masterlist?')] = 'N'
			guntype = inv.loc[i]['Type']
			archetype = inv.loc[i]['Perks 0']
			mster_similar = mster[(mster['Type'] == guntype) & (mster['Archetype'] == archetype)]
			perknumbers=[0]
			pvxlist = ['min']
			for k in range(len(mster_similar)):
				Sight_barrels = False
				Magazine = False
				perkcheckcounter = 0
				for perkno in range(0,11):
					if inv.iloc[i]['Perks ' + str(perkno)] in mster_similar.iloc[k]['Sights/Barrels'] and Sight_barrels == False:
						perkcheckcounter += 1
						Sight_barrels = True
						continue
					if inv.iloc[i]['Perks ' + str(perkno)] in mster_similar.iloc[k]['Magazine'] and Magazine ==False:
						perkcheckcounter += 1
						Magazine = True
						continue
					if inv.iloc[i]['Perks ' + str(perkno)] in mster_similar.iloc[k]['Perklist']:
						perkcheckcounter += 1
				perknumbers.append(perkcheckcounter)
				pvxlist.append(mster_similar.iloc[k]['pvX'])
			maxno = max(perknumbers)
			perknpvx = list(zip(perknumbers,pvxlist))
			maxperknpvx = [x[1] for x in perknpvx if x[0] == maxno]
			if 'PvE' in maxperknpvx:
				inv.iloc[i,inv.columns.get_loc('PvE?')] = 1
			if 'PvP' in maxperknpvx:
				inv.iloc[i,inv.columns.get_loc('PvP?')] = 1
			inv.iloc[i, inv.columns.get_loc('Perkcheck')] = max(perknumbers)
			continue

		#makes a copy of a slice of df containing only the rolls of interest for a particular weapon
		mster_name = mster[mster['Name'] == gun_name].copy()
		perknumbers =[0]
		pvxlist =['min']

		for j in range(len(mster_name)):
			Sight_barrels = False
			Magazine = False
			perkcheckcounter = 0
			for perkno in range(0,11):
				if inv.iloc[i]['Perks ' + str(perkno)] in mster_name.iloc[j]['Sights/Barrels'] and Sight_barrels == False:
					perkcheckcounter += 1
					Sight_barrels = True
					continue
				if inv.iloc[i]['Perks ' + str(perkno)] in mster_name.iloc[j]['Magazine'] and Magazine ==False:
					perkcheckcounter += 1
					Magazine = True
					continue
				if inv.iloc[i]['Perks ' + str(perkno)] in mster_name.iloc[j]['Perklist']:
					perkcheckcounter += 1


			perknumbers.append(perkcheckcounter)
			pvxlist.append(mster_name.iloc[j]['pvX'])

		print(perknumbers)
		print(pvxlist)
		maxno = max(perknumbers)
		perknpvx = list(zip(perknumbers,pvxlist))
		maxperknpvx = [x[1] for x in perknpvx if x[0] == maxno]
		if 'PvE' in maxperknpvx:
			inv.iloc[i,inv.columns.get_loc('PvE?')] = 1
		if 'PvP' in maxperknpvx:
			inv.iloc[i,inv.columns.get_loc('PvP?')] = 1


		inv.iloc[i, inv.columns.get_loc('Perkcheck')] = max(perknumbers)
	return inv