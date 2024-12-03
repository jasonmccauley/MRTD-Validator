import json
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MRTD import MRTDProcessor


# Determine the path to the current script's directory
# We had some trouble pointing at the files so we used ChatGPT for this part to help us out
# Here we just intlize the path to refrence the Json Files
current_dir = os.path.dirname(os.path.abspath(__file__))
encoded_file_path = os.path.normpath(os.path.join(current_dir, "../part3/records_encoded.json"))
decoded_file_path = os.path.normpath(os.path.join(current_dir, "../part3/records_decoded.json"))


# Load the JSON files and refrence them through the path we made above
with open(encoded_file_path, "r") as f:
    encoded_records = json.load(f)["records_encoded"]

with open(decoded_file_path, "r") as f:
    decoded_records = json.load(f)["records_decoded"]

# Initialize the MRTDProcessor
check = MRTDProcessor()

# Creating a function to measure performance 
def measure_performance():
    #Intilizing an array for the results
    results = []
    # I intilize a loop that goes through the first 100 files so the next loop can iterate through them in thousant increments
    for k in range(101):
                # starting the time function to keep track of the time it takes to decode
        start = time.time()
        # Looping through the data to encode it dependent on what number k is at for the amount of files
        for record in encoded_records[:k]:
            # Splitting the data to input in the decode_mrz
            line1, line2 = record.split(";")
            check.decode_mrz(line1, line2)
            # Record the time it finished and subtract it from the time it started, which gives the time it took
        decode_time = time.time() - start

        # starting the time function to keep track of the time it takes to encode
        start = time.time()
        # Looping through the data to encode it dependent on what number k is at for the amount of files
        for record in decoded_records[:k]:
            # Perparing the fields to be able to encode it
            fields = {
                "type": "P", 
                **record["line1"],
                **record["line2"]
            }
            # Confirm all fields exist in each entry 
            required_keys = {"type", "issuing_country", "last_name", "given_name", "passport_number", "country_code", "birth_date", "sex", "expiration_date", "personal_number"}
            # Mention which keys are missing for debugging purposes
            missing_keys = required_keys - fields.keys()
            # Create a condition if any keys are missing
            if missing_keys:
                raise KeyError(f"Missing keys in record: {missing_keys}")
            # Run the encode function for each field
            check.encode_mrz(fields)
        # Record the time it finished and subtract it from the time it started, which gives the time it took
        encode_time = time.time() - start
    results.append([k, decode_time, encode_time])
