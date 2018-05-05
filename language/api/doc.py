import argparse
import json
import sys
import glob
import googleapiclient.discovery
import os
import concurrent.futures
import urllib.request


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def analyze_entities(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
            'language': 'EN'
        },
        'encoding_type': encoding,
    }
    service = googleapiclient.discovery.build('language', 'v1')
    request = service.documents().analyzeEntities(body=body)
    try:
        response = request.execute()
    except:
        response = {}
    return response

counter = 0
results = {}
os.chdir("texts")
all_data = []
for file in glob.glob("*.txt")[:5]:
	with open(file, 'r') as myfile:
            data=myfile.read(999999).replace('\n', '')
            all_data += [data]
# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(analyze_entities, url): url for url in all_data}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print(counter)
            counter += 1	    

with open('result.json', 'w') as fp:
    json.dump(future_to_url, fp)