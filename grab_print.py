#Imports
from pysnmp.hlapi import *
import json
import time

#Variables
printers = []

printer_OIDS = {
    "host_name": "1.3.6.1.2.1.1.5.0",
    "printer_model": "1.3.6.1.2.1.25.3.2.1.3.1",
    "serial_num": "1.3.6.1.2.1.43.5.1.1.17.1",
    "blck_toner": "1.3.6.1.2.1.43.11.1.1.9.1.1",
    "cyan_toner": "1.3.6.1.2.1.43.11.1.1.9.1.2",
    "magenta_toner": "1.3.6.1.2.1.43.11.1.1.9.1.3",
    "yellow_toner": "1.3.6.1.2.1.43.11.1.1.9.1.4",
    "print_count": "1.3.6.1.2.1.43.10.2.1.4.1.1"
}

switch_OIDS = {
    "Hostname"      : "1.3.6.1.2.1.1.5.0",    # sysName
    "Description"   : "1.3.6.1.2.1.1.1.0" ,   # sysDescr
    "Uptime"        : "1.3.6.1.2.1.1.3.0" ,   # sysUpTime
    "PortCount"     : "1.3.6.1.2.1.17.1.2.0", # dot1dBaseNumPorts
}
#######################################################################################
#Config

end_num = 11               #What number should it start with?
front_num = '10.30.129.'   #Fill with the front part of the VLAN IP
iterations = 24            #How many Ips should it look through, starting with end_num

#End-config
#######################################################################################
PRINTER_IP = ''
COMMUNITY = 'public'

def snmp_get(oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(COMMUNITY, mpModel=0),  # SNMP v1
        UdpTransportTarget((PRINTER_IP, 161), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    error_indication, error_status, error_index, var_binds = next(iterator)

    if error_indication:
        raise RuntimeError(error_indication)
    elif error_status:
        raise RuntimeError(
            f'{error_status.prettyPrint()} at {error_index}'
        )
    else:
        for _, value in var_binds:
            return value.prettyPrint()

def display_val(val_to_grab, is_printer): #Grabs the OID in a way that if it fails its friendly to display
    try:
        if is_printer:
            oid = printer_OIDS[val_to_grab]
        else:
            oid = switch_OIDS[val_to_grab]
        val_to_return = snmp_get(oid)
        return val_to_return
    except Exception as e:
        print(e)
        return "Fail"
while True:
    end_num = 11
    printers.clear()
    for i in range(iterations + 1):
        PRINTER_IP = f'{front_num}{end_num}'
        try:
            to_append = {"name":display_val("host_name", True), 
                    "IP":PRINTER_IP,  
                    "device_model":display_val("printer_model", True),
                    "Serial_number": display_val("serial_num", True),
                    "Black_toner": display_val("blck_toner", True),
                    "Cyan_toner": display_val("cyan_toner", True),
                    "Magenta_toner": display_val("magenta_toner", True),
                    "Yellow_toner": display_val("yellow_toner", True),
                    "Print_count": display_val("print_count", True),
                    }
            printers.append(to_append)
        except Exception as e:
            print("Couldnt access printer")
            print(e)
        end_num += 1

    with open('printers.json', 'w', encoding='utf-8') as f:
        json.dump(printers, f, ensure_ascii=False, indent=4)
    print("Wrote to json")
    time.sleep(60)
    print("Refreshed")

    




