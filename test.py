import csv
import numpy as np
import zipcode
import us
import pandas as pd

#http://www.fec.gov/disclosurep/pnational.do
#https://www.census.gov/popest/data/cities/totals/2015/SUB-EST2015.html

def get_contribution_data(file_location):
	data = {'zipcode': [], 'contribution_total': []}
	with open(file_location, 'rb') as f:
		reader = csv.reader(f, delimiter = ' ')
		for row in reader:
			data['zipcode'].append(row[0].strip())
			data['contribution_total'].append( float(row[-1].replace(',', '').strip()) )

	return pd.DataFrame(data)

def get_population_data(census_data_location):
	#column 8: city name (followed by 'city' if in that category)
	#column 9: state name
	#column -1: 2015 population estimate
	CITY = 8
	STATE = 9
	POPULATION = -1
	STATE_CODE_MAP = us.states.mapping('name', 'abbr')

	data = {'city': [], 'population': []}
	with open(census_data_location, 'rb') as f:
		reader = csv.reader(f, delimiter = ',')
		reader.next() #skip header
		for row in reader:
			if row[CITY][-5:] == ' city':
				city_name = row[CITY][:-5].upper() + ", " + str(STATE_CODE_MAP[row[STATE]])
				data['city'].append(city_name.strip())
				data['population'].append(int(row[POPULATION]))

	return pd.DataFrame(data)

def main():
	contribution_data_location = "./trump_oct_2016_contributions_by_zipcode.txt"
	census_data_location = "./SUB-EST2015_ALL.csv"

	c_data = get_contribution_data(contribution_data_location)
	p_data = get_population_data(census_data_location)

	c_by_city = {}
	#add up total contributions for each city
	for j in xrange(len(c_data)):
		zip_j = zipcode.isequal(c_data['zipcode'][j])
		try:
			city_name = zip_j.city.upper().strip() + ", " + zip_j.state.strip()
			if j in xrange(len(c_data['city'])):
				if p_data['city'][j] in c_by_city:
					c_by_city[city_name] += c_data['contribution_total'][j]
				else:
					c_by_city[city_name] = c_data['contribution_total'][j]
		except:
			continue

	print "Done with contribution totals dictionary computation"

	print c_by_city

	#now divide each city contribution total by population of that city
	c_per_p_by_city = {}
	for city in c_by_city:
		c_per_p_by_city[city] = c_by_city[city]/p_data[city]

	print c_per_p_by_city
	
	best_city = min(c_per_p_by_city)
	
	print best_city, "$" + c_per_p_by_city[best_city]

	

if __name__ == "__main__":
	main()
			
	
