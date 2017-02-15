import requests
import json

# pars group
all_id = ['proglib', 'newsbarca', 15648447]

param = {'owner_id': -22746750, 'count': 100}
r = requests.get('https://api.vk.com/method/wall.get', params=param)
response = r.json()

# post_date = response['response'][1]['date']
# post_date2 = response['response'][2]['date']
# post_date3 = response['response'][3]['date']
# post_date4 = response['response'][4]['date']

for i in range(1, 101):
    post_date = response['response'][i]['date']
    post_date2 = response['response'][i]['comments']['count']

    print(post_date,',', post_date2,)

# with open('data.json', 'w') as outfile:
#     json.dump(response, outfile)