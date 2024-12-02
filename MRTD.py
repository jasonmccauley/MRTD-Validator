import string
class MRTDProcessor:
    def __init__(self):
        # Define weights for check digit calculation
        self.weights = [7, 3, 1]




    def encode_mrz(self, fields: dict) -> tuple:
        """
        Encodes fields into MRZ format strings.

        :param fields: Dictionary containing travel document information fields.
        :return: A tuple of two strings representing the MRZ.
        """
        line1 = f"{fields['type']}<{fields['issuing_country']}{fields['last_name']}<<{fields['given_name'].replace(' ', '<')}".ljust(44, "<")
        line2 = (
            f"{fields['passport_number']}{self.calculate_check_digit(fields['passport_number'])}"
            f"{fields['country_code']}{fields['birth_date']}{self.calculate_check_digit(fields['birth_date'])}"
            f"{fields['sex']}{fields['expiration_date']}{self.calculate_check_digit(fields['expiration_date'])}"
            f"{fields['personal_number']}{self.calculate_check_digit(fields['personal_number'])}"
        ).ljust(44, "<")
        return line1, line2