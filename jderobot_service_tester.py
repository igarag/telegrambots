#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import requests
import time
import datetime

import subprocess
import smtplib
from email.mime.text import MIMEText
#from websocket import create_connection


"""
Script to send an email to several people to inform them of the 
operation of JdeRobot services.

For the WebSocket request it is necessary to install a client
of WebSocket. One of the most popular is: websocket-client,
can be installed via pip.
"""

__author__ = "Ignacio Arranz Águeda"
__license__ = "GPL"
__version__ = "0.5"
__email__ = "n.arranz.agueda@gmail.com"
__status__ = "Production"

# This flag sends the warning email to only one person.
debug = True

services = [
        "https://kibotics.org",
        "https://makers.kibotics.org",

        "https://unibotics.org",
        "https://developers.unibotics.org",

        "https://gitlab.jderobot.org",
        "https://jderobot.org/Main_Page",
    ]


def checking_certs():

    certs_expired = []
    notification = "certs"
    sites = ["kibotics", "unibotics", "jderobot"]

    for site in sites:
        print(site)
        cert = subprocess.getoutput("echo | openssl s_client -connect " + site + ".org:443 " \
                                    " 2>/dev/null | openssl x509 -noout -dates")

        # Expired time
        # Example: Feb 18 10:00:00 2019 - Formato completo: '%b %d %H:%M:%S %Y'
        cert_date = cert.split("\n")[1].split("=")[1].split(" GMT")[0]
        format_cert = datetime.datetime.strptime(cert_date, '%b %d %H:%M:%S %Y')
        expired_date = datetime.datetime(format_cert.year, format_cert.month, format_cert.day)

        # Time Now
        today = datetime.datetime.today()

        if today > expired_date - datetime.timedelta(days=5):
            site_date = {}
            site_date[site] = str(expired_date)
            certs_expired.append(site_date)

        cert_success = True
    print(certs_expired)
    return certs_expired, notification
    


def checking_services():
    '''
    Check and build the list of services that are down.
    '''
    downed_services = []
    notification = "services"
    for site in services:
        try:
            code = requests.get(site)
            if code.status_code != 200:
                downed_services.append(site)
                print(site, " DOWN")
        except:
            print("Error en la solicitud: " + site + "\n")
            downed_services.append(site)
            print("\n=== DOWNED SERVICES ====================")
            #print(str(downed_services))
            print(*downed_services, sep = "\n") 
            print("==========================================\n")
    
    return downed_services, notification

    # Check Daphne:
    # try:
    #     ws = create_connection("wss://kibotics.org/_ws_/?user=crodriguezgarci& \
    #             client_ip=10.1.130.237&simulation_type=remote&main_server_ip=kibotics.org& \
    #             host_ip=193.147.79.196&exercise=drone_cat_mouse& \
    #             docker_id=6c239743a4a0794381dc7af6c2da926ace3f4348813d814a9adbc763b55b007d")
    #     ws.send("Monitoring - Are you still alive?")
    #     result =  ws.recv()
    #     ws.close()
    # except:
    #     print("Error en la solicitud WebSocket. Dahpne Caído.\n")
    #     downed_services.append("wss://kibotics.org/_ws_/[...]")
    #     print(*downed_services, sep = "\n")


def send_email(sites, notification):

    # Building message and users.
    if debug:
        addressees = [ 'n.arranz.agueda@gmail.com' ]
    else:
        addressees = [
                    'n.arranz.agueda@gmail.com',
                    'xarlye13@gmail.com',
                    'aitor.martinez.fernandez@gmail.com',
                    'f.perez475@gmail.com',
                    'josemaria.plaza@gmail.com'
        ]

    for addr in addressees:
        if notification == "services":
            message = "ATENCIÓN: Fallo en el servicio: " + str(sites)
        elif notification =="certs":
            message = "ATENCIÓN: Certificados próximos a su caducidad de: " + ','.join(map(str, sites))
            print(message)

        msg = MIMEText(message)
        if debug:
            msg['Subject'] = "=========== JdeRobot Monitor (debug) ==========="
        else:
            msg['Subject'] = "=========== JdeRobot Monitor ==========="
        msg['From']    = 'JdeRobot-Admin <jderobot@gmail.com>'
        msg['To']      = addr
        
        
        # Sending email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("jderobot", "gsoc2015")
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("\nMain sent to " + str(addr))
        



if __name__ == "__main__":
    # List of services than are down.

    downed_services, notification = checking_services()
    certs_expired, notification = checking_certs()

    #checking_certs()
    #print(downed_services)

    if len(downed_services) != 0: send_email(downed_services, notification)
    if len(certs_expired) != 0: send_email(certs_expired, notification)
