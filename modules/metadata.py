import json

from bluemoon.utils.logly import logly


def save_metadata(filename, data):
    try:
        # Save each key-value pair separately for the image
        with open(filename, 'a+') as f:
            for key, value in data:
                json.dump({key: value}, f, indent=2)
                f.write('\n')
    except Exception as e:
        logly.error('Error while logging metadata: {}'.format(e))
