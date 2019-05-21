import requests
import os
import argparse
from dotenv import load_dotenv


def get_short_link(token, link):
  url_template = 'https://api-ssl.bitly.com/v4/bitlinks'
  url_auth = {"Authorization": "Bearer {}".format(token)}
  url_params = {"long_url": link}

  url_response = requests.post(url_template, headers=url_auth, json=url_params)
  url_response.raise_for_status()
  response = url_response.json()

  return response['link']

def get_num_of_clicks(token, short_link):
  bitlink = short_link.split('//')[1]
  url_template = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(bitlink)
  url_auth = {"Authorization": "Bearer {}".format(token)}

  url_response = requests.get(url_template, headers=url_auth)
  url_response.raise_for_status()
  response = url_response.json()

  return response['total_clicks']

def is_bitlink(token, link):
  bitlink = link.split('//')[1]
  url_template = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(bitlink)
  url_auth = {"Authorization": "Bearer {}".format(token)}
  try:
    url_response = requests.get(url_template, headers=url_auth)
    url_response.raise_for_status()
  except requests.exceptions.HTTPError as error:  
    return False
  return True


if __name__=="__main__":
  #link = input('Введите исходную ссылку: ')
  parser = argparse.ArgumentParser()
  parser.add_argument('name', help='Исходная ссылка')
  args = parser.parse_args()
  
  load_dotenv()
  token = os.getenv("token")

  link = args.name
  if not link:
    exit("Не корректна введена ссылка!")
    
  if is_bitlink(token, link):

    try:
      total_clicks = get_num_of_clicks(token, link)
    except requests.exceptions.HTTPError as error:
      exit("Не могу получить данные с сервера:\n{0}".format(error))
    print(f'Всего переходов: {total_clicks}')

  else:

    try:
      short_link = get_short_link(token, link)
    except requests.exceptions.HTTPError as error:
      exit("Не могу получить данные с сервера:\n{0}".format(error))
    print(f'Короткая ссылка: {short_link}')