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