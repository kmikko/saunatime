# -*- coding: utf-8 -*-

from requests import session
from datetime import datetime, timedelta
import sys
import time
import argparse

retry_count = 0

def main():
  parser = argparse.ArgumentParser(description="So you want some sauna time?")
  parser.add_argument("-u","--username", help="OmaPSOAS username", required=True)
  parser.add_argument("-p","--password", help="OmaPSOAS password", required=True)
  parser.add_argument("-c","--cid", help="cID", required=True)
  parser.add_argument("-r", "--retry", help="Times to retry. Default 5.", default=5)
  args = vars(parser.parse_args())

  with session() as c:
    def login():
      payload = {
        "username": args["username"],
        "password": args["password"]
      }

      r = c.post("https://ssl.omapsoas.fi/index/login", data=payload, allow_redirects=False)

      if r.status_code != 302:
        print("{0} - ERROR: Login failed".format("{:%d/%m/%Y %H:%M:%S}".format(datetime.now())))
        sys.exit()

    def reserve():
      global retry_count
      headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
      }

      cookies = {
        "PHPSESSID": c.cookies.get_dict()["PHPSESSID"]
      }

      today = datetime.now()
      reservation_date = datetime.now() + timedelta(days=14)
      url = "https://ssl.omapsoas.fi/reservation/reserve/date/{0}/cid/{2}/mins/{1}".format("{:%Y-%m-%d}".format(reservation_date), today.hour*60, args["cid"])

      response = c.post(url, headers=headers, cookies=cookies)
      if "error" in response.text:
        if retry_count < args["retry"]:
          print("{0} - ERROR: {1}".format("{:%d/%m/%Y %H:%M:%S}".format(datetime.now()), response.text))
          print("{0} - Retrying {1}/{2} in 10s...".format("{:%d/%m/%Y %H:%M:%S}".format(datetime.now()), retry_count+1, args["retry"]))
          retry_count += 1
          time.sleep(10)
          reserve()
        else:
          print("{0} - Could not make a reservation, quitting...".format("{:%d/%m/%Y %H:%M:%S}".format(datetime.now())))
          sys.exit()
      else:
        print("{0} - Sauna reserved!".format("{:%d/%m/%Y %H:%M:%S}".format(datetime.now())))
        sys.exit()

    login()
    reserve()

if __name__ == "__main__":
  main()
