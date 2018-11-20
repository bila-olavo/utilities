#!/usr/bin/python
import sys
import requests
import os
import urllib
from urlparse import urlparse
import boto3
import botocore

if len(sys.argv) == 1:
  print('use ./downloader.py {arg1} {arg2} {argN}')
  sys.exit(1)

cwd = os.getcwd()

count = 1
total = len(sys.argv)
while count < total:
  url = sys.argv[count]
  parse = urlparse(url)
  if 'http' in parse.scheme:
    print ("Downloading: " +url+ '...')
    filename = url.rsplit('/', 1)[-1]
    path = cwd + '/' + filename
    r = requests.get(url)
    with open( path, 'wb') as f:  
      f.write(r.content)
  elif 's3' in parse.scheme:
    print ("Downloading: " +url+ '...')
    filename = url.rsplit('/', 1)[-1]
    path = cwd + '/' + filename
    bucket_name = parse.netloc
    s3 = boto3.resource('s3')
    try:
      s3.Bucket(bucket_name).download_file(filename, path)
    except botocore.exceptions.ClientError as e:
      if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
      else:
        raise
  else:
    print ('Invalid link: ' +url+ '')
    sys.exit(1)
  count = count + 1

sys.exit(0)