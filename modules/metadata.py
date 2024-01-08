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
            # Read the existing content
            content = f.read()

            # Remove the trailing ']' if it exists
            if content.strip().endswith(']'):
                f.seek(0, os.SEEK_END)
                f.seek(f.tell() - 1, os.SEEK_SET)
                f.truncate()

            # Write the new metadata
            if content and content.strip() != '[':
                f.write(',\n')  # Separate metadata with a comma if there's existing content
            json.dump(data, f, indent=2)

            # Write closing square bracket
            f.write('\n]\n')

    except Exception as e:
        logly.error('Error while logging metadata: {}'.format(e))
