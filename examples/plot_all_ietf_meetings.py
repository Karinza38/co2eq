from co2eq.meeting import IETFMeetingList
from conf import CONF

## building a meeting serie 
ietf_meeting_list = IETFMeetingList( conf=CONF ) 
## building all graphs
ietf_meeting_list.plot_all()
## building web pages in md format
## url is the URL under which you have:
## * IETF or ALL with figures for all IETFs
## * IETF72, IETF73... each individual IETF meetings
## Jekyll local installation uses 'http://127.0.0.1:4000/IETF/' as the base URL
## gh-pages uses https://mglt.github.io/co2eq/IETF
## the leap theme seems to be the only one that generates a TOC
## ietf_meeting_list.www_md( 'http://127.0.0.1:4000/IETF/', toc=False)
ietf_meeting_list.www_md( 'https://mglt.github.io/co2eq/IETF/', toc=False)

