import re


# Taken from Stackoverflow question
# https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def extract_year(text):
    year = re.search("[0-9]{4}", text).group(0)
    return year