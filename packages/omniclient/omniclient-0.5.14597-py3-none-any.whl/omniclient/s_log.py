
#####################################################################
#
# s_log.py
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

import os
import json
from datetime import datetime
import uuid
import hashlib
from . import s_config 

#####################################################################

log_filepath = False
log_traceid = False

def init( ) :

    global log_traceid
    global log_filepath

    if( log_traceid != False ) : return

    log_workspacedir = s_config.get_key( "sys/workspacedir" , "/tmp")

    # FIXME TODO
    os.makedirs( log_workspacedir , exist_ok = True )

    # Add trailing slash
    log_filepath = os.path.join( log_workspacedir , "" ) + "omniclient.log" 

    log_traceid = "TRI" + hashlib.sha256( str( uuid.uuid4( ) ).encode( "utf-8" )  ).hexdigest( )


def get_traceid( ) :
    return( log_traceid )

def default_json( t ) :
    return f'{t}'

def write( msg_raw , context = "-" ) :

    init( )

    msg = msg_raw

    if( msg == None ) : msg = "!NONE!"
    
    if( isinstance( msg , list ) ) :
        msg = ",".join( map( str , msg ) )
    
    if( isinstance( msg , dict ) ) :
        # FIXME TODO use util json note numpy stuff
        msg = json.dumps( msg , default = default_json , indent=4, sort_keys=True)

    if( isinstance( msg , ( int , float , bool ) ) ) :
        msg = str( msg )

    msg = log_traceid + ":::" + datetime.now( ).strftime( "%Y_%m_%d-%H_%M_%S" ) + ":::" + context + ":::" + msg
    with open( log_filepath , "a+" , 1 ) as log_file :
        log_file.write( msg + "\n" )

def flush( ) :
    if os.path.isfile( log_filepath ) :
        os.remove( log_filepath )

