import requests
random_land = requests.get('https://api.3geonames.org/randomland.IT.json').json()
lat = random_land['nearest']['latt']
lon = random_land['nearest']['longt']

geodecoded_place = requests.get(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json').json()

print(geodecoded_place)
print(geodecoded_place['address']['road'])
print(geodecoded_place['address']['village'])
print(geodecoded_place['address']['county'])
print(geodecoded_place['address']['state'])
print(geodecoded_place['address']['postcode'])