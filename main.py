import pyodbc
import requests
import json


#import file config.json

with open('config.json') as json_file:
    config = json.load(json_file)


server = config['server']
database = config['database']
username = config['username']
password = config['password']

# Set up the connection to the Zendesk API
zendesk_url = config['ZENDESK_URL']
zendesk_user = config['ZENDESK_USER']
zendesk_token = config['ZENDESK_TOKEN']
headers = {'Content-Type': 'application/json'}
auth = (zendesk_user, zendesk_token)

while True:
    modulo = input("Escolha o módulo (1-groups, 2-users, 3-tickets): ")
    if modulo in ["1", "1-groups",'groups']:
        modulo = "groups"
        break
    elif modulo in ["2", "2-users","users"]:
        modulo = "users"
        break
    elif modulo in ["3", "3-tickets","tickets"]:
        modulo = "tickets"
        break
    else:
        print("Entrada inválida. Tente novamente.")


if modulo== "tickets":

    url = zendesk_url + f'/api/v2/incremental/tickets.json?start_time=1615821979&include=metric_sets'
else:
    url = zendesk_url + f'/api/v2/{modulo}.json'

listaComDados = []

while url:
    response = requests.get(url, headers=headers, auth=auth)
    data = json.loads(response.text)
    listaComDados += data[modulo]
    url = data['next_page']
    print(f'Lendo dados da api: {url}')
