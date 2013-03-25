callsign-notify
===============

This script checks the ACMA website for the status of a call sign.
If the call sign is found to be active, it emails the user.

It is recommend that the script be run in a cron job every few hours. Do not
run more regularly, in order to not stress the server.

 00 08-19 * * 1-5 /usr/bin/python /home/user/bin/callsign-notify.py

Requires python-requests and assumes that the 'mail' command installed and
configured for outgoing e-mail. Written for Python 2.7.

Joel <joel@jms.id.au>
March 2013
