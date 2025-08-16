def processfiles(invfilename,mstrfilename='Master.csv'):
	import pandas as pd
	import numpy as np

	#importing Master and inventory files
	mster = pd.read_csv(mstrfilename)
	raw_inventory = pd.read_csv(invfilename)

	#copy files
	inventory = raw_inventory.copy()

	#inventory file processing
	inventory['Name'] = inventory['Name'].apply(lambda x: x.lower())
	inventory.fillna(value='-----',inplace=True)
	for perkno in range(0,11):
		inventory['Perks ' + str(perkno)] = inventory['Perks ' + str(perkno)].apply(lambda x : str(x).strip('*'))
	columnstodrop = ['Hash','Id','Tag','Source','Owner','Locked','Equipped','Year','Season','Event','DTR Rating','# of Reviews','Recoil','AA','Impact','Range','Blast Radius','Velocity','Stability','ROF','Reload','Mag','Equip','Charge Time','Draw Time','Accuracy','Notes']
	inventory.drop(labels=columnstodrop,axis=1,inplace=True)
	inventory['Perkcheck'] = 0
	inventory['PvE?'] = 0
	inventory['PvP?'] = 0
	inventory['In Masterlist?'] = 'Y'

	inv = inventory.copy()


	#Compares inv to master
	rows = len(inv)

	for i in range(rows):
	    if str(inv.iloc[i]['Tier']) != 'Legendary':
	        inv.iloc[i,inv.columns.get_loc('In Masterlist?')] = inv.iloc[i]['Tier']
	        continue

	    gun_name = inv.iloc[i]['Name']
	    if mster['Name'].str.match(gun_name).any() == False and  str(inv.iloc[i]['Tier']) == 'Legendary':
	        #add code for dealing with absent games
	        inv.iloc[i,inv.columns.get_loc('In Masterlist?')] = 'N'
	        guntype = inv.loc[i]['Type']
	        archetype = inv.loc[i]['Perks 0']
	        mster_similar = mster[(mster['Weap Type'] == guntype) & (mster['Archetype'] == archetype)]
	        
	        perknumbers=[0]
	        pvxlist=['0']
	        for j in range(len(mster_similar)):
	            Perk1= False
	            Perk2= False
	            Perk3= False
	            Perk4= False
	            #perkcheckcounter = 0
	            for perkno in range(0,11):
	                if inv.iloc[i]['Perks ' + str(perkno)] in mster_similar.iloc[j]['Perk 1'] and Perk1 == False:
	                    Perk1 = True
	                    continue
	                if inv.iloc[i]['Perks ' + str(perkno)] in mster_similar.iloc[j]['Perk 2'] and Perk2 == False:
	                    Perk2 = True
	                    continue
	                if inv.iloc[i]['Perks ' + str(perkno)] in mster_similar.iloc[j]['Perk 3'] and Perk3 == False:
	                    Perk3 = True
	                    continue
	                if inv.iloc[i]['Perks ' + str(perkno)] in mster_similar.iloc[j]['Perk 4'] and Perk4 == False:
	                    Perk4 = True
	                    continue
	            perknumbers.append(sum([Perk1,Perk2,Perk3,Perk4]))
	            pvxlist.append(mster_similar.iloc[j]['PvX'])
	        print(perknumbers)
	        print(pvxlist)
	        maxno=max(perknumbers)
	        perknpvx = list(zip(perknumbers,pvxlist))
	        maxperknpvx = [x[1] for x in perknpvx if x[0] == maxno]
	        if 'pve' in maxperknpvx:
	            inv.iloc[i,inv.columns.get_loc('PvE?')] = 1
	        if 'pvp' in maxperknpvx:
	            inv.iloc[i,inv.columns.get_loc('PvP?')] = 1
	        inv.iloc[i, inv.columns.get_loc('Perkcheck')] = max(perknumbers)
	        continue
	    
	    mster_name = mster[mster['Name'] == gun_name].copy()
	    perknumbers=[0]
	    pvxlist=['0']
	    for j in range(len(mster_name)):
	        Perk1= False
	        Perk2= False
	        Perk3= False
	        Perk4= False
	        #perkcheckcounter = 0
	        for perkno in range(0,11):
	            if inv.iloc[i]['Perks ' + str(perkno)] in mster_name.iloc[j]['Perk 1'] and Perk1 == False:
	                Perk1 = True
	                continue
	            if inv.iloc[i]['Perks ' + str(perkno)] in mster_name.iloc[j]['Perk 2'] and Perk2 == False:
	                Perk2 = True
	                continue
	            if inv.iloc[i]['Perks ' + str(perkno)] in mster_name.iloc[j]['Perk 3'] and Perk3 == False:
	                Perk3 = True
	                continue
	            if inv.iloc[i]['Perks ' + str(perkno)] in mster_name.iloc[j]['Perk 4'] and Perk4 == False:
	                Perk4 = True
	                continue
	        perknumbers.append(sum([Perk1,Perk2,Perk3,Perk4]))
	        pvxlist.append(mster_name.iloc[j]['PvX'])
	    print(perknumbers)
	    print(pvxlist)
	    maxno=max(perknumbers)
	    perknpvx = list(zip(perknumbers,pvxlist))
	    maxperknpvx = [x[1] for x in perknpvx if x[0] == maxno]
	    if 'pve' in maxperknpvx:
	        inv.iloc[i,inv.columns.get_loc('PvE?')] = 1
	    if 'pvp' in maxperknpvx:
	        inv.iloc[i,inv.columns.get_loc('PvP?')] = 1
	    inv.iloc[i, inv.columns.get_loc('Perkcheck')] = max(perknumbers)
	return inv