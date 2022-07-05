#!/usr/bin/env python3
"""Log stat"""


from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
nginx = client.logs.nginx

print(f'{nginx.count_documents({})}')
print('Methods:')

print(f'\tmethod GET: {nginx.count_documents({"method": "GET"})}')
print(f'\tmethod POST: {nginx.count_documents({"method": "POST"})}')
print(f'\tmethod PUT: {nginx.count_documents({"method": "PUT"})}')
print(f'\tmethod PATCH: {nginx.count_documents({"method": "PATCH"})}')
print(f'\tmethod DELETE: {nginx.count_documents({"method": "DELETE"})}')

print(f'{nginx.count_documents({"path": "/status"})} status check')
