import subprocess

class Kenneth:
    def __init__(self):

        # This is the main list of information for stuff.

        # Includes the WMIC command, a dict to hold the details for devices detected in that category,
        # Specific things to collect for the minimal text, a variable for the minimal text, and a variable
        # for the full text.  I'm sure there's a nicer way, figure it out later though.

        self.devices = {
            'cpu': {'wmic': 'cpu',
                    'devices': {},
                    "text": "",
                    "minimal": ['Description','Manufacturer','Name','NumberOfCores'],
                   "text_minimal": ""
                    },
            "gpu": {'wmic': 'path win32_videocontroller',
                    'devices': {},
                    "text": "",
                    "minimal": ['Caption','Description','AdapterRAM','CurrentHorizontalResolution','CurrentVerticalResolution'],
                   "text_minimal": ""
                    },
            "ram": {'wmic': 'memorychip',
                    'devices': {},
                    "text": "",
                    "minimal": ['PartNumber','Speed','Manufacturer','Capacity'],
                   "text_minimal": ""
                    },
            "motherboard": {'wmic': 'baseboard',
                    'devices': {},
                    "text": "",
                    "minimal": ['Product', 'SerialNumber','Manufacturer'],
                   "text_minimal": ""
                    },
            "disk": {'wmic': 'diskdrive',
                    'devices': {},
                    "text": "",
                    "minimal": ['Model','SerialNumber','Size'],
                   "text_minimal": ""
                    },
            "monitors": {'wmic': 'desktopmonitor',
                    'devices': {},
                    "text": "",
                    "minimal": ['Name'],
                   "text_minimal": ""
                    },
            "os": {'wmic': 'os',
                    'devices': {},
                    "text": "",
                    "minimal": ['Caption','BuildNumber','CSName','InstallDate','Manufacturer','SystemDrive','Version'],
                   "text_minimal": ""
                    },
            "overview":{
                'text': "",
                'text_minimal': ""
            }
        }

        # Iterate through the above list
        for device in self.devices:
            if device == 'overview':
                pass
            else:

                # Execute the WMIC command
                data = self.run_query(self.devices[device]['wmic'])

                # Parse the data out
                # This comes out as a list, usually there's only one thing in it
                parsed = self.parse_response_new(data)

                # But if there are two things in it, separate them.
                if len(parsed) > 1:
                    i = 0
                    for thing in parsed:

                        # Set the device name in the dict, and set the data to the device dict
                        self.devices[device]['devices'][f'{device}{i}'] = thing

                        # Fancy tabbing
                        max_key_length = max(len(key) for key in thing)

                        # Crafting lines for text and minimal text
                        for xx in thing:
                            line = f'{xx:<{max_key_length + 4}}{thing[xx]}\n'
                            self.devices[device]['text'] += line
                            if xx in self.devices[device]['minimal']:
                                self.devices[device]['text_minimal'] += line

                        self.devices[device]['text'] += "\n\n"
                        self.devices[device]['text_minimal'] += "\n\n"
                else:
                    self.devices[device]['devices'][f'{device}{0}'] = parsed[0]
                    print(parsed[0])
                    max_key_length = max(len(key) for key in parsed[0])

                    for thing in parsed[0]:
                        line = f'{thing:<{max_key_length + 4}}{parsed[0][thing]}\n'
                        self.devices[device]['text'] += line
                        if thing in self.devices[device]['minimal']:
                            self.devices[device]['text_minimal'] += line

                    self.devices[device]['text'] += "\n\n"
                    self.devices[device]['text_minimal'] += "\n\n"


    def parse_response_new(self,data):
        # This means there are multiple devices
        if "\r\r\n\r\r\n\r\r\n" in data:
            devices = data.split("\r\r\n\r\r\n\r\r\n")
        else:
            devices = [data]

        response_data = []

        # Itereate through the devices, usually just one
        for device in devices:
            response = {}

            # Split up into pairs
            pairs = device.split("\r\r\n")

            # Get key/value for each pair if the value exists and store in the dict
            for thing in pairs:
                key,value = thing.split("=")
                if value:
                    response[key] = value

            response_data.append(response)

        return response_data


    def run_query(self, query):
        try:
            result = subprocess.check_output(f"wmic {query} get /format:list", shell=True).decode()

            return result.strip()
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e}"

