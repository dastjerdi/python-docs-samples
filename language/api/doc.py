import argparse
import json
import sys
import glob
import googleapiclient.discovery
import os


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
    response = request.execute()
    return response

counter = 0
results = {}
os.chdir("texts")
for file in glob.glob("*.txt"):
	with open(file, 'r') as myfile:
            data=myfile.read(999999).replace('\n', '')
	    results[file] = analyze_entities(data)
	    counter += 1
	    print(counter)

with open('result.json', 'w') as fp:
    json.dump(results, fp)
