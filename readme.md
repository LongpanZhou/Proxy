This TCP server is for network class assignment, it acts as a proxy server between client and url accessing. The TCP server will first check in local cache to see if url exist if it does then return the html, else redirect request to url server.

Note:
This script is running HTTP 1.0, which means that for some server which are running HTTP 1.1 or others it might not work.

Usage:
`
Python fileWebProxy.py *IP*:*Port*
`
