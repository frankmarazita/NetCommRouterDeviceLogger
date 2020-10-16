import requests
import re
import csv

url = "http://192.168.20.1/js/summary.js"

# Exclude local IP addresses
NOIP = False

data_from_file = []

# Import existing data from output file
try:
    with open('output.csv', newline='') as file_input:
        file_reader = csv.reader(file_input, delimiter=',')
        for row in file_reader:
            data_from_file.append(row)
except:
    pass

data = requests.get(url)
matches = []
matches += re.findall(r'(?:(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}|(?:[a-zA-Z0-9\-]+))(?:[,\.0-9A-Za-z])*(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}', data.text)


with open('output.csv', mode='w', newline='') as file_output:
    file_writer = csv.writer(file_output, delimiter=',')

    devices = []
    for match in matches:
        devices.append(match.replace("\"", "").split(","))

    # Remove local ip addresses
    # for device in devices:
    #     if NOIP:
    #         device.pop(1)

    # Write existing devices
    for device in data_from_file:
        file_writer.writerow(device)

    # Write new devices
    for device in devices:
        if device not in data_from_file:
            file_writer.writerow(device)
