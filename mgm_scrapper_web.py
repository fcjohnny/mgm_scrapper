#! /usr/bin/env python3
from selenium import webdriver
from selenium import common
import datetime
import sys
import csv
import json

def main():
  driver = webdriver.Firefox()
  driver.get('https://www.signaturemgmgrand.com/en/booking/room-booking.html#/step1&arrive=2018-04-11&depart=2018-04-12&numGuests=2')
  date = datetime.datetime.today()
  delta_1_day = datetime.timedelta(days=1)
  current_month = date.month
  current_year = date.year
  price_list = []
  while not(date.month == current_month and date.year >
  current_year):
    date_string = '{}-{}-{}'.format(date.day,date.month-1,date.year)
    xPath_Price = '//td[@id="c-'+date_string+'"]//span[contains(text(),"$")]'
    try:
      price = driver.find_element_by_xpath(xPath_Price).text
    except common.exceptions.NoSuchElementException:
      price = "unavailable"
    price_list.append([date.strftime('%Y-%m-%d'),price])
    #print(date.strftime('%Y-%m-%d,'+price))
    date = date + delta_1_day
  if len(sys.argv) > 1 and sys.argv[1] == "json":
    write_json(price_list)
  else:
    write_csv(price_list)
  driver.close()

def write_csv(data):
  with open(datetime.datetime.today().strftime('%Y-%m-%d')+'.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

def write_json(data):
  json_encoded = json.JSONEncoder().encode(data)
  with open(datetime.datetime.today().strftime('%Y-%m-%d')+'.json','w') as \
  jsonfile:
    for line in json_encoded:
      jsonfile.write(line)

if __name__ == "__main__":
  main()
