
#####################################################################
#
# omniclient.py
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
import io
import json

#####################################################################

from . import s_log , s_config , s_net , s_cache , s_util , s_db 

#####################################################################

s_log.write( "    ####    ####    ####    ####" )

#####################################################################

if( "OMNICLIENT_CONFIGURATION" in os.environ ) :
    s_config.init_fromfile( os.environ[ "OMNICLIENT_CONFIGURATION" ] , "omniclient" )
    s_log.write( "Loaded OMNICLIENT_CONFIGURATION " + os.environ[ "OMNICLIENT_CONFIGURATION" ] )

if( s_config.get_key( "config/init_fromfile" ) != "yes" ) :
    s_log.write( "WARNING Did not find OMNICLIENT_CONFIGURATION file" )
#    s_config.init_fromfile( )

#s_log.write( s_config.get_config( ) )

#####################################################################

def log_write( msg ) :
    s_log.write( msg )

def log_flush( ) :
    s_log.flush( )

def config_get( ) :
    return( s_config.get_config( ) )

def config_get_key( kn ) :
    return( s_config.get_key( kn ) )

def config_set_key( kn , kv ) :
    return( s_config.set_key( kn , kv ) )

def config_del_key( kn ) :
    return( s_config.del_key( kn ) )

def config_init_fromfile( config_path = "local_omniclient_config.json" , config_key = "omniclient" ) :
    return s_config.init_fromfile( config_path , config_key )

#####################################################################

def net_client_job_set( payload ) :
    return( s_net.client_job_set( payload ) )
def net_client_job_get( jid ) :
    return( s_net.client_job_get( jid ) )

