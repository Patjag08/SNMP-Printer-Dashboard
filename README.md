# SNMP-Printer-Dashboard
A basic HTML and JS Webpage to display a table of printers for help with management in an IT environment, this was created to assist at Krohne with managing printers at the IT Department however is decently universal. In order to actualy get the information to display a python script must be running in the same folder called 'grab_print.py'. This file is responsible for generating the .json file that is rendered on the webpage and it looks kind of like this:
```
[
    {
        "name": "GENERIC-PRINTER",
        "IP": "192.168.1.1",
        "device_model": "GENERIC-PRINTER-MODEL",
        "Serial_number": "ABCDEF",
        "Black_toner": "97",
        "Cyan_toner": "97",
        "Magenta_toner": "97",
        "Yellow_toner": "97",
        "Print_count": "642"
    }
]
```
This is then grabbed by table.js and iterates through the json file entries to display a table within the html.

## Instalation
The webpage is straight forward however for the python to work there are a few steps.

First, Make sure python is running on version 3.11 or else some dependancies will not function.

Second, run the following module installs with [pip](https://pip.pypa.io/en/stable/):

```bash
pip install pysnmp
pip install pysnmplib
```

Next is within the file there is a set of three config variables, these are used to make sure you filter through the disered IP's to get info about the printers.

```python
#######################################################################################
#Config

end_num = 11               #What number should it start with?
front_num = '10.30.129.'   #Fill with the front part of the VLAN IP
iterations = 24            #How many Ips should it look through, starting with end_num

#End-config
#######################################################################################
```

And that should be it, the rest of the python file is better left untouched.

## Operations

For the site to function you may run the site on any Apache HTTP server you find fit and should work relatively well, just ensure it has access to the necessary vlans to pickup any printers you wnat to have on the dashboard. Also make sure the python script is running to keep the .json up to date for the site itself.
