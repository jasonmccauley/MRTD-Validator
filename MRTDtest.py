import unittest
from unittest.mock import patch 
from MRTD import MRTDProcessor




class Test_MRTD_Processor(unittest.TestCase):


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
    # Added this test case to kill mutants 
    def test_MRZ_validator_invalid(self):
        """
        Test validate_mrz with MRZ lines where some check digits are incorrect.
        """
        # Expected results for different mismatched cases
        expected_result1 = ["Mismatch in birth date check digit.", "Mismatch in expiration date check digit."]
        expected_result2 = ["Mismatch in passport number check digit.", "Mismatch in personal number check digit."]

        # Example MRZ lines for each case
        line1_example = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
        line2_example1 = "L898902C36UTO6908062F1204158ZE184226B<<<<<<<1"  # Incorrect birth date and expiration check digits
        line2_example2 = "L898902C26UTO7408122F1204159ZE184226B<<<<<<<2"  # Incorrect passport number and personal number check digits

        # Intilize the MRTDProcessor
        check = MRTDProcessor()
        #Running it through the function
        result1 = check.validate_mrz(line1_example, line2_example1)
        # Matched the results with expected results
        self.assertEqual(result1, expected_result1)

        # Validate passport number and personal number mismatches
        # Running the examples through the function 
        result2 = check.validate_mrz(line1_example, line2_example2)
        # Matching it with the results
        self.assertEqual(result2, expected_result2)