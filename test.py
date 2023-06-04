import re

input_str = '"finished"'
if re.match(r'^\".*\"$', input_str):
    print("Match found!")
else:
    print("Match not found.")