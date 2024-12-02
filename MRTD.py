import string
class MRTDProcessor:
    def __init__(self):
        # Define weights for check digit calculation
        self.weights = [7, 3, 1]

    def query_database(self):
        """
        Placeholder for database interaction.
        Should retrieve travel document information fields for encoding.
        """
        pass

    def decode_mrz(self, line1: str, line2: str) -> dict:
        """
        Decodes the two MRZ strings into respective fields.

        :param line1: The first line of the MRZ.
        :param line2: The second line of the MRZ.
        :return: A dictionary containing the decoded fields.
        """
        # Adjsuted this line based on the data given in part 3 changing gender to sex, and name to last_name and given_name
        name_parts = line1[5:].rstrip("<").split("<<")
        decoded = {
            "type": line1[:1],
            "issuing_country": line1[2:5],
            "last_name": name_parts[0],
            "given_name": name_parts[1].replace("<", " ") if len(name_parts) > 1 else "",
            "passport_number": line2[:9],
            "passport_number_check": int(line2[9]),
            "country_code": line2[10:13],
            "birth_date": line2[13:19],
            "birth_date_check": int(line2[19]),
            "sex": line2[20],
            "expiration_date": line2[21:27],
            "expiration_date_check": int(line2[27]),
            "personal_number": line2[28:42].rstrip("<"),
            "personal_number_check": int(line2[-1]),
        }
        return decoded

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