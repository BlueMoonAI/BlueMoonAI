import json

from bluemoon.utils.logly import logly
import os

metadata={}
def save_metadata(filename, data):
    try:
        # Check if the file exists
        file_exists = os.path.isfile(filename)

        # Open the file in append mode if it exists; otherwise, open it in write mode to create a new file
        with open(filename, 'a+' if file_exists else 'w+') as f:
            for key, value in data:
                metadata[key] = value
                f.write('\n')
            json.dump(metadata, f, indent=2)

    except Exception as e:
        logly.error('Error while logging metadata: {}'.format(e))

