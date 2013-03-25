#!/usr/bin/python
#
# ACMA callsign notification script
#
# Joel <joel@jms.id.au>
# March 2013
#
# This script checks the ACMA website for the status of a callsign.
# If the callsign is found to be active, it emails the user.
#

import requests
import logging
import subprocess
import time
import sys

# Config option: list name, email, callsign as strings in a tuple
hams = []

# Config option: set the logging level
logging.basicConfig(level=logging.INFO)

URL = """http://web.acma.gov.au/pls/radcom/register_search.search_dispatcher?pSEARCH_TYPE=Licences&pSUB_TYPE=any%20detail&pEXACT_IND=matches&pQRY=CALLSIGN"""

EMAILCMD = """echo "Dear NAME,\n\nYour callsign is active. You can confirm by visiting the ACMA website:\n\n    URL\n\nCongratulations!" | mail -s "ACMA Licence Status" EMAIL"""

if len(hams) == 0:
    logging.error("Add at least one person to the hams list")
    sys.exit()

for name, email, callsign in hams:
    url = URL.replace("CALLSIGN", callsign)
    r = requests.get(url)
    if r.status_code != 200:
        logging.error("Failed to reach server: %d" % r.status_code)
        continue
    logging.info("Got ACMA webpage for %s" % callsign)
    if r.text.count("No matches") != 0:
        logging.info("%s not there yet" % name)
        continue
    logging.info("Found matches")
    if r.text.count(name) > 0:
        # Confirmed. Send mail to the ham.
        logging.debug("Sending email to %s at %s" % (name, email))
        cmd = EMAILCMD.replace("EMAIL", email)
        cmd = cmd.replace("URL", url)
        cmd = cmd.replace("NAME", name)
        if subprocess.call(cmd, shell=True) == 0:
            logging.info("Email sent")
        else:
            logging.info("Failed to send email")
    # Wait before hitting the website again
    time.sleep(10)
