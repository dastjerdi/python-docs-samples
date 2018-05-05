import argparse
import json
import sys
import glob
import googleapiclient.discovery
import os
import concurrent.futures


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
files = glob.glob("*.txt")[150:]
for file in files:
	with open(file, 'r') as myfile:
            data=myfile.read(999999).replace('\n', '')
            all_data += [data]

data = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
    future_to_url = {executor.submit(analyze_entities, url): url for url in all_data}
    for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
        url = future_to_url[future]
        try:
            data[files[i]] = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print(counter)
            counter += 1

with open('result22.json', 'w') as fp:
    json.dump(data, fp)
