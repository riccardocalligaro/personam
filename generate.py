from numpy.random import choice
import numpy
import pandas as pd
import random
from codicefiscale import codicefiscale
from datetime import date

from models import Person
from faker import Faker
from PIL import Image
import requests

sex = 'm'
generate_face = True

person = Person()
names_df=pd.read_csv('data/names.csv', sep=',')

# filter by sex
names_df = names_df[names_df['gender'] == sex] 

names_probs = numpy.array(names_df['percent'])
names_probs /= names_probs.sum()


name = choice(names_df.iloc[:, 0].values, p=names_probs)
lowered_name = ''
for name in name.split(' '):
    lowered_name += name.lower().capitalize() + ' '

lowered_name = lowered_name.strip()
person.first_name = lowered_name

# surnames_df=pd.read_csv('data/surnames.csv', sep=',')
# surnames_probs = numpy.array(surnames_df['percent'])
# surnames_probs /= surnames_probs.sum()
# surname = choice(surnames_df.iloc[:, 1].values, p=surnames_probs)
surnames_df = pd.read_csv('data/surnames.csv', sep=',')
surname = surnames_df.sample()['name'].values[0]

phone = random.randint(0000000, 9999999)

prefixes = [330, 331, 333, 334, 335, 336, 337, 338, 339, 360, 363, 366, 368, 340, 342, 345, 346, 347, 348, 349, 320, 323, 327, 328, 329, 380, 383, 388, 389, 390, 391, 392, 393, 397]
prefix = random.choice(prefixes)

complete_phone_number = f'{prefix}{phone}'

cities_df = pd.read_csv('data/cities.csv', sep=',')
# print(cities_df['pop_res_21'])
cities_df = cities_df[cities_df['pop_res_21'] > 20000] 
sampled_city = cities_df.sample(n = 1)
city = sampled_city['comune'].values[0]

province = sampled_city['den_prov'].values[0]
province_code = sampled_city['sigla'].values[0]
region = sampled_city['den_reg'].values[0]

addresses_df = pd.read_csv('data/addresses.csv', sep=',')
address = choice(addresses_df.iloc[:, 0].values).title()
street_number = random.randint(1, 100)
fake = Faker()
birth_date = fake.date_between(start_date='-55y', end_date='-20y')
formatted_birth_date = birth_date.strftime("%d/%m/%Y")
today = date.today()
age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

nickname = f'{lowered_name}_{surname}{random.randint(0, 100)}'.lower()
codice_fiscale = codicefiscale.encode(surname=surname, name=lowered_name, sex='M', birthdate=formatted_birth_date, birthplace=province)
print(f'{lowered_name} {surname}')
print(f'Nato a {province} il {formatted_birth_date} ({age})')
print(codice_fiscale)
print(nickname)

print(f'\n{address} {street_number}')
print(f'{city} ({province_code})')
print(f'{complete_phone_number}\n')



hobbies_df = pd.read_csv('data/hobbies.csv', sep=',')
hobbies = hobbies_df.sample(n = 3)['name'].values

# 28% laureati
# 62% diplomati

universities_df = pd.read_csv('data/universities.csv', sep=',')
universities_df = universities_df[universities_df['name'].str.contains(f'{province}|{region}')]

if len(universities_df) > 0:
    university = universities_df.sample()['name'].values[0]
    print(university)

jobs_df = pd.read_csv('data/jobs.csv', sep=',')
sampled_job = jobs_df.sample(n = 1)
job = sampled_job['name'].values[0]

if generate_face:
    im = Image.open(requests.get(f'https://fakeface.rest/face/view?gender={"male" if sex == "m" else "female"}&minimum_age={age-2}&maximum_age={age+7}', stream=True).raw)
    im.show()

print(job)
print(hobbies)
