
#####################################################################
#
# s_cleanup.py
#
# Project   : OMNICLIENT
# Author(s) : Zafar Iqbal < zaf@sparc.space >
# Copyright : (C) 2021 SPARC PC < https://sparc.space/ >
#
# All rights reserved. No warranty, explicit or implicit, provided.
# SPARC PC is and remains the owner of all titles, rights
# and interests in the Software.
#
#####################################################################

import atexit

#####################################################################

from . import s_log  

#####################################################################

def cleanup( ) :
    s_log.write_msg( "CLEANUP" )

atexit.register( cleanup )
s_log.write_msg( "Registered cleanup" )



    