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

required_keys_encoder = {
    "type", "issuing_country", "last_name", "given_name",
    "passport_number", "country_code", "birth_date",
    "sex", "expiration_date", "personal_number"
}


# Creating a function to measure performance
def measure_performance():
    #Intilizing an array for the results
    results = []
    # I intilize a loop that goes through the first 100 files so the next loop can iterate through them in thousant increments
    for records in range(101):
        # starting the time function to keep track of the time it takes to decode
        start = time.time()
        # Looping through the data to encode it dependent on what number k is at for the amount of files
        for record in encoded_records[:records]:
            # Splitting the data to input in the decode_mrz
            line1, line2 = record.split(";")
            # Call function for the lines 
            check.decode_mrz(line1, line2)
            # Record the time it finished and subtract it from the time it started, which gives the time it took
        decode_time = time.time() - start

        # starting the time function to keep track of the time it takes to encode
        start = time.time()
        # Looping through the data to encode it dependent on what number k is at for the amount of files
        for record in decoded_records[:records]:
            # Perparing the fields to be able to encode it
            fields = {
                # Default case of p 
                "type": "P", 
                **record["line1"],
                **record["line2"]
            }
            # Mention which keys are missing for debugging purposes
            missing_keys = required_keys_encoder - fields.keys()
            # Create a condition if any keys are missing
            if missing_keys == 0:
                raise KeyError(f"Missing keys in record: {missing_keys}")
            # Run the encode function for each field
            check.encode_mrz(fields)
        # Record the time it finished and subtract it from the time it started, which gives the time it took
        encode_time = time.time() - start
    results.append([records, decode_time, encode_time])
    # Looping through the data set in increments of 1000
    for k in range(1000, 10001, 1000):
        # starting the time function to keep track of the time it takes to decode
        start = time.time()
        # Looping through the data to encode it dependent on what number k is at for the amount of files
        for record in encoded_records[:k]:
            # Splitting the data to input in the decode_mrz
            line1, line2 = record.split(";")
            # Call the function 
            check.decode_mrz(line1, line2)
            # Record the time it finished and subtract it from the time it started, which gives the time it took
        decode_time = time.time() - start

        # starting the time function to keep track of the time it takes to encode
        start = time.time()
        # Looping through the data to encode it dependent on what number k is at for the amount of files
        for record in decoded_records[:k]:
            # Perparing the fields to be able to encode it
            fields = {
                #Defualt cases
                "type": "P", 
                **record["line1"],
                **record["line2"]
            }
            # Mention which keys are missing for debugging purposes
            missing_keys = required_keys_encoder - fields.keys()
            # Create a condition if any keys are missing
            if missing_keys:
                raise KeyError(f"Missing keys in record: {missing_keys}")
            # Run the encode function for each field
            check.encode_mrz(fields)
        # Record the time it finished and subtract it from the time it started, which gives the time it took
        encode_time = time.time() - start

        # Append results
        results.append([k, decode_time, encode_time])

    return results

# Run performance testing
performance_results = measure_performance()

# Save results to a text file
# Used ChatGPT to help format a txt file to store the results 
output_file = os.path.join(current_dir, "performance_data.xlsx")
with open(output_file, "w") as txtfile:
    # Write header
    txtfile.write(f"{'Records':<10}{'Decode_Time':<15}{'Encode_Time':<15}\n")
    txtfile.write("=" * 40 + "\n")
    # Write data rows
    for k, decode_time, encode_time in performance_results:
        txtfile.write(f"{k:<10}{decode_time:<15.6f}{encode_time:<15.6f}\n")

print(f"Performance testing complete. Results saved to {output_file}.")
