import os
import json

from bluemoon.utils.logly import logly

metadata = {}

def save_metadata(filename, data):
    try:
        # Check if the file exists
        file_exists = os.path.isfile(filename)

        # Open the file in append mode if it exists; otherwise, open it in write mode to create a new file
        with open(filename, 'a' if file_exists else 'w') as f:
            if file_exists:
                f.seek(0, os.SEEK_END)
                # If the file is not empty, move the cursor to the end and remove the last '}\n' characters
                if f.tell() > 0:
                    f.seek(f.tell() - 3)  # Move back to the first character of '}'
                    f.truncate()

            f.write('{\n')
            for key, value in data:
                metadata[key] = value
            json.dump(metadata, f, indent=2)
            f.write(',\n}\n')

    except Exception as e:
        logly.error('Error while logging metadata: {}'.format(e))
