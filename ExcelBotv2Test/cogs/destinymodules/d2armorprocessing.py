def armor(filename, arg):
	import pandas as pd
	raw = pd.read_csv(filename)
	columnstodrop =['Hash','Id','Tag','Source','Year','Event','DTR Rating','# of Reviews', 'Mobility', 'Resilience', 'Recovery', 'Discipline', 'Intellect','Strength', 'Total', 'Notes','Perks 0','Perks 1','Perks 2','Perks 3','Perks 4','Owner','Locked','Equipped' ]
	data = raw.drop(labels=columnstodrop,axis=1).copy()
	abbr = {'Int': 'Intellect (Base)','Dis':'Discipline (Base)','Mob':'Mobility (Base)','Str':'Strength (Base)','Rec':'Recovery (Base)','Res':'Resilience (Base)'}

	for entry in arg:
		listentry = entry.split(',')
		print(listentry)
		if len(listentry) == 3:
			data[f'Sum ({entry})'] = data[abbr[listentry[0]]] + data[abbr[listentry[1]]] + data[abbr[listentry[2]]]
		elif len(listentry) == 2:
			data[f'Sum ({entry})'] = data[abbr[listentry[0]]] + data[abbr[listentry[1]]]
		else:
			return 'One of the combinations is not of length 2 or 3'


	return data
