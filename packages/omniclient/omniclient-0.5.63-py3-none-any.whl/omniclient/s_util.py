
#####################################################################
#
# s_util.py
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
import pickle
from pathlib import Path

from . import s_log , s_config

#####################################################################

class NumpyEncoder( json.JSONEncoder ) :

    def default( self , obj ) :
        return  json.JSONEncoder.default( self , obj )
        #if isinstance( obj , numpy.integer ) :
        #    return int( obj )
        #elif isinstance( obj, numpy.floating ) :
        #    return float( obj)
        #elif isinstance( obj, numpy.ndarray ) :
        #    return obj.tolist( )
        #return json.JSONEncoder.default( self , obj )

def json_encode( data ) :
    return json.dumps( data , cls = NumpyEncoder )

#####################################################################

def pickle_load( fn ) :
    if( os.path.isfile( fn ) ) :
        s_log.write_msg( "FOUND " + fn )
        with open( fn , "rb" ) as f :
            return( pickle.load( f ) )
    else :
        return None
        
def pickle_save( datakey , data ) :
    f = open( "local_" + datakey + ".pkl" , "wb" )
    pickle.dump( run_response , f )
    f.close( )


 
def pathnotallowed( p ) :

    #s_log.write( p )

    p1 = os.path.normpath(p)
    #s_log.write( p1 )

    p2 = os.path.realpath(p1)
    #s_log.write( p2 )


#    base_dir = "/data/omniclient/"

    base_dir = s_config.get_key( "omniclient/cwd" , "/tmp")


    path_test = ( Path( base_dir ) / p2 ).resolve( ) 

    #s_log.write(str(Path(base_dir).resolve()))
    #s_log.write(str(path_test.parent))


    if( str( path_test.parent ).startswith( base_dir ) ) :
        return( False )

    return( True )

   