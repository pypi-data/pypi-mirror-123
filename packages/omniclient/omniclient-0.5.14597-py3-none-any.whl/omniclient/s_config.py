
#####################################################################
#
# s_confg.py
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

#####################################################################

from . import get_version
from . import s_log  

#####################################################################

config = { }

#####################################################################

config[ "omniclient/version" ] = get_version( )
config[ "omniclient/cwd" ] = os.getcwd( )
config[ "omniclient/scriptdir" ] = os.path.dirname(os.path.realpath(__file__))

#####################################################################

def get_config( ) :
    return config

def set_key( config_key , config_val ) :
    global config
    #s_log.write( "CONFIG SET_KEY " + config_key + " = " + str( config_val ) )
    config[ config_key ] = config_val
    return True

def get_key( config_key , default_val = None ) :
    #s_log.write_msg("GET KEY "+config_key)
    if( config_key in config ) :
        #s_log.write_msg("GET KEY FOUND")
        if config[ config_key ] != None :
            return config[ config_key ]
            
    #s_log.write_msg("GET KEY NULL")
    return default_val

def del_key( kn ) :
    #s_log.write_msg("GET KEY "+config_key)
    if( kn in config ) :
        #s_log.write_msg("GET KEY FOUND")
        config.pop( kn )
        return True
            
    #s_log.write_msg("GET KEY NULL")
    return False

def init_fromfile( config_path = "local_omniclient_config.json" , config_key = "omniclient" ) :

    global config

    #s_log.write( os.getcwd( ) + "," + config_path )

    try :

        with open( config_path ) as f :
            config_all = json.load( f )
    
    except IOError :

        s_log.write( "config init_fromfile IOError " + config_path )
        return False

    ####################################################################

    if config_key in config_all :
        config.update( config_all[ config_key ] )
        config["config/init_fromfile"]="yes"
    else :
        s_log.write( "ERROR config_key " + config_key )
        return False

    ####################################################################

    #s_log.write( "LOADED " + config_path )

    #s_log.write( config )

    return True

