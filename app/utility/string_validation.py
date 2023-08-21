import re

def __strip_spaces(s):
    s = re.sub(r'^\s+', '', s)
    s = re.sub(r'\s+$', '', s)
    return s

def email_format(email_str): return bool(re.match(r'^[\w.-]+@[\w-]+[.][\w-]+$', __strip_spaces(email_str)))

def phone_format(phone_str): return bool(re.match(r'^[+]\d+$', __strip_spaces(phone_str)))