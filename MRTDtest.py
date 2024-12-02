import unittest
from unittest.mock import patch
from MRTD import MRTDProcessor

class Test_MRTD_Processor(unittest.TestCase):

    # Route for testing Hardware scanner
    @patch('MRTD.MRTDProcessor.scan_mrz')
    def test_scan(self, mock_scan):
        ''' 
        Firstly, we "scan" the information on the passport, in this case we will be inputing it as a 
        return value. The Information that we ar inputting consists of the MRZ values, with 2 rows of
        information present.
        '''
        # Import the 2 rows of information 
        mock_scan.return_value = (
            "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<",
            "L898902C36UTO7408122F1204159ZE184226B<<<<<<<1"
        )
        # Refrencing the scan_mrz method from MRTD.py as a placeholder function, along with its value
        result = MRTDProcessor.scan_mrz()
        # Verifying that the results from the main function matches up with our test case
        self.assertEqual(
            result,
            (
                "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<",
                "L898902C36UTO7408122F1204159ZE184226B<<<<<<<1"
            )
        )
        '''
        This function will always pass, as we do not have an actaul scanner. The function in the main component
        is known as a placeholder function that will pass any value. 
        '''

    # Route for testing database
    @patch('MRTD.MRTDProcessor.query_database')
    def test_database(self, mock_query):
        '''
        In this mock test case we intilize a database and populate it. In this case we will be seperating
        all the 2 rows to indivual values except for the name which includes first, middle, and last name.
        '''
        # populating the database with a mock version of the data since the database doesn't exist
        mock_query.return_value = {
            "type": "P", # Document type
            "issuing_country": "UTO", # Issuing country 
            "name": "ERIKSSON<<ANNA<MARIA", # Last Name: First Name: Middle Name
            "passport_number": "L898902C3", # Passport Number
            "passport_number_check": 6,  # Check digit for the passport number
            "country_code": "UTO", # Country Code
            "birth_date": "690806", # Date of Birth
            "birth_date_check": 2,  # Check digit for the birth date
            "sex": "F", # Sex
            "expiration_date": "120415", # Expiration Date
            "expiration_date_check": 9,  # Check digit for the expiration date
            "personal_number": "ZE184226B", # Personal Number
            "personal_number_check": 1, # Check digit for personal number
        }
        # Calls the query_database class, but since its a placeholder it will pass anyway
        result = MRTDProcessor.query_database()
        # Creating a mock case of the expected results to compare with the database created
        expected_result = mock_query.return_value
        # Comparing the database that was ran through the main function to the expected results
        self.assertEqual(result, expected_result)
        # Iterate through the hash maps values and keys, verifying that the information is present and then comparing it
        for key, value in expected_result.items():
            self.assertIn(key, result)  # Verifying each key exists
            self.assertEqual(result[key], value)  # Verfying the value matches

    # Route for testing the check digits of the MRZ string to later verify the info in it
    def test_CheckDigit_calculator(self):       
        # call the method to verify the check digit for Pass port number
        check = MRTDProcessor()
        # Checking if the result from the main function matches our test case 
        self.assertEqual(check.calculate_check_digit("L898902C3"), 6)
        # call the method to verify the check digit for Birth date 
        # Checking if the result from the main function matches our test case 
        self.assertEqual(check.calculate_check_digit("690806"), 1)
        # call the method to verify the check digit for Expiration Date number
        # Checking if the result from the main function matches our test case 
        self.assertEqual(check.calculate_check_digit("120415"), 9)
        # call the method to verify the check digit for Personal number
        # Checking if the result from the main function matches our test case 
        self.assertEqual(check.calculate_check_digit("ZE184226B"), 1)

    # Route for testing the decoding of the MRZ string to later verify the info in it
    def test_MRZ_decoder(self):
        '''
        This tests the decoding of the MRZ strings, the decoder takes 2 input strings and sperates them 
        based on the format provided. They are then put in a hashmap for refrence, the keys and values 
        can be seen below.
        '''
        # Intilizing the result of what is expected to happen once the code is ran through the function
        # Creating a mock case of the expected results to compare with the database created
        expected_result = {
            "type": "P",
            "issuing_country": "UTO",
            "last_name": "ERIKSSON",
            "given_name": "ANNA MARIA",
            "passport_number": "L898902C3",
            "passport_number_check": 6,
            "country_code": "UTO",
            "birth_date": "740812",  # Updated to match line2_example
            "birth_date_check": 2,
            "sex": "F",
            "expiration_date": "120415",  # Updated to match line2_example
            "expiration_date_check": 9,
            "personal_number": "ZE184226B",
            "personal_number_check": 1,
        }
        # Setting the values for the imported fields
        line1_example = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
        line2_example = "L898902C36UTO7408122F1204159ZE184226B<<<<<<<1"
        # Running the setted values into the fields
        check = MRTDProcessor()
        result = check.decode_mrz(line1_example, line2_example)
        # Comparing the results of the function to the expected results of before
        self.assertEqual(result, expected_result)
        # testing each indivual key and value in the hash map to match the decoding
        for key, value in expected_result.items():
            self.assertIn(key, result)  # Verifying each key exists
            self.assertEqual(result[key], value)  # Verfying the value matches

    # Route for testing the decoded MRZ string back into its original version
    def test_MRZ_Encoder(self):
        '''
        This function returns the decoded MRZ strings back to its original format.
        '''
        # Intilizing return values
        # Setting the expected result of the function to the return values to compare
        expected_result = (
            "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<",
            "L898902C36UTO7408122F1204159ZE184226B1<<<<<<"
        )
        # Using the encode function to revert the feilds back into the MRZ string format the way it was scanned
        check = MRTDProcessor()
        result = check.encode_mrz({
            "type": "P",
            "issuing_country": "UTO",
            "last_name": "ERIKSSON",
            "given_name": "ANNA MARIA",
            "passport_number": "L898902C3",
            "passport_number_check": 6,
            "country_code": "UTO",
            "birth_date": "740812",  # Updated to match line2_example
            "birth_date_check": 2,
            "sex": "F",
            "expiration_date": "120415",  # Updated to match line2_example
            "expiration_date_check": 9,
            "personal_number": "ZE184226B",
            "personal_number_check": 1,
        })
        # checking if the results of the function is the same as the expected results
        self.assertEqual(result, expected_result)

    # Route for testing the validation of the feilds according to the check digits
    def test_MRZ_validator(self):
        '''
        This function validates that the check digits are valid with the information given
        '''
        # We test when no errors exist in the system 
        expected_result = []
        # Setting the values for the imported fields
        line1_example = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
        line2_example = "L898902C36UTO7408122F1204159ZE184226B<<<<<<<1"
        # Getting the result of the validate function 
        check = MRTDProcessor()
        result = check.validate_mrz(line1_example, line2_example)
        # We set the epected results to an emtpy array if it passes all the check digits
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()