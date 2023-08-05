
#####################################################################
#
# s_db.py
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
import hashlib
import sqlite3

from . import s_log , s_config , s_util

#####################################################################

db_filepath = False


def init_db_filepath( ) :
    global db_filepath
    if(db_filepath!=False): return

    log_workspacedir = s_config.get_key( "sys/workspacedir" , "/tmp")

    # FIXME TODO
    os.makedirs( log_workspacedir , exist_ok = True )

    # Add trailing slash
    db_filepath = os.path.join( log_workspacedir , "" ) +  "omniclient.db" 

    #s_log.write( db_filepath )


def filepath_get( ) :
    return( db_filepath )


def reset( ) :
   
    #s_log.write( "db reset" )

    init_db_filepath( )

    if( os.path.isfile( db_filepath ) ) :
        #s_log.write( "db_filepath exists... deleting..." ) 
        os.remove( db_filepath )

    #s_log.write( "db_filepath creating..." ) 

    init_schema( )

    if( os.path.isfile( db_filepath ) ) :
        return( True )

    s_log.write( "False db_filepath isfile" ) 
    return( False )


def init_schema( ) :

    #s_log.write( "db init_schema" )

    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )

    ################################################################

    # OK
    cur.execute( ''' CREATE TABLE sys ( sn text , svs text , svn real ) ''' )
    cur.execute( "CREATE INDEX index_sys ON sys ( sn ) ;" )

    cur.execute( "INSERT INTO sys VALUES ( 'ver' , null , 1 )" )
    cur.execute( "INSERT INTO sys VALUES ( 'serial' , 'ODS042e1919c5bd8f41cd8e1a2b8e455dd8f6fb00df0c3916d1137047a7aafc4c42' , null )" )

    ################################################################

    cur.execute( ''' CREATE TABLE files ( fp text , fc blob , fs integer , fh text ) ''' )
    cur.execute( "CREATE INDEX index_files ON files ( fp ) ;" )

    ################################################################

    # OK
    cur.execute( ''' CREATE TABLE env ( en text , ev text ) ''' )
    cur.execute( "CREATE INDEX index_env ON env ( en ) ;" )

    ################################################################

    # OK
    cur.execute( ''' CREATE TABLE stdio ( sid integer PRIMARY KEY AUTOINCREMENT , sk integer , sv text ) ''' )
    cur.execute( "CREATE INDEX index_stdio ON stdio ( sid , sk ) ;" )

    ################################################################

    # OK
    cur.execute( ''' CREATE TABLE args ( aid integer PRIMARY KEY AUTOINCREMENT , av text ) ''' )
    cur.execute( "CREATE INDEX index_args ON args ( aid ) ;" )

    ################################################################

    # OK
    cur.execute( ''' CREATE TABLE stacks ( sid integer PRIMARY KEY AUTOINCREMENT , sk integer , sv text ) ''' )
    cur.execute( "CREATE INDEX index_stacks ON stacks ( sid , sk ) ;" )

    ################################################################

    # OK
    cur.execute( ''' CREATE TABLE meta ( mn text , mvs text , mvn real ) ''' )
    cur.execute( "CREATE INDEX index_meta ON meta ( mn ) ;" )

    ################################################################

    # OK
    cur.execute( ''' CREATE TABLE templates ( tid integer PRIMARY KEY AUTOINCREMENT , tp text , tk text , tv real ) ''' )
    cur.execute( "CREATE INDEX index_templates ON templates ( tid , tp ) ;" )


    con.commit( )
    con.close( )


def sys_get( sn ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "SELECT svs , svn FROM sys where sn='" + sn + "' limit 1" )
    rows = cur.fetchall( )
    con.close( )
    if( len( rows ) != 1 ) : return( False )
    #s_log.write( rows )
    if( rows[ 0 ][ 0 ] == None ) : return( rows[ 0 ][ 1 ] )
    if( rows[ 0 ][ 1 ] == None ) : return( rows[ 0 ][ 0 ] )
    return(False)

def stacks_push( sv_dict , sk = 0 ) :
    sv = s_util.json_encode( sv_dict )
    #s_log.write(sv)
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "INSERT INTO stacks VALUES ( null , " + str( sk ) + " , '" + sv + "' )" )
    con.commit( )
    con.close( )
    return(True)

def stacks_pop( sk = 0 ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "SELECT sid , sv FROM stacks where sk=" + str( sk ) + " order by sid desc limit 1" )
    rows = cur.fetchall( )
    
    #s_log.write( rows )

    if( len( rows ) != 1 ) :
        con.close( )
        return( False )
   
    sid=rows[ 0 ][ 0 ]
    sv_dict=json.loads(rows[ 0 ][ 1 ])

    cur.execute( "DELETE FROM stacks where sid=" + str( sid ) + " limit 1" )
    con.commit( )
    con.close( )
    return( sv_dict )    


def stacks_getall( sk = 0 ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "SELECT sv FROM stacks where sk=" + str( sk ) + " order by sid asc" )
    rows = cur.fetchall( )
    con.close( )

    #s_log.write( rows )

    data = [ ]
    
    for row in rows :
        s_log.write( row[ 0 ] )
        data.append( json.loads( row[ 0 ] ) )

    #s_log.write( data )

    return( data )    

def stacks_count( sk = 0 ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "SELECT COUNT(*) FROM stacks where sk=" + str( sk ) )
    rows = cur.fetchall( )
    con.close( )
    #s_log.write(rows)
    if( len( rows ) != 1 ) :
        con.close( )
        return( False )
    return( rows[ 0 ][ 0 ] )


def env_add( en , ev ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "INSERT INTO env VALUES ( '" + en + "' , '" + ev + "' )" )
    con.commit( )
    con.close( )
    return(True)

def env_get_all( ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "SELECT * FROM env" )
    rows = cur.fetchall( )
    con.close( )
    s_log.write( rows )
    return( rows )  

def meta_add( mn , mv ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )

    if( isinstance( mv , str ) ) :
        cur.execute( "INSERT INTO meta VALUES ( '" + mn + "' , '" + mv + "' , null )" )
    else:
        cur.execute( "INSERT INTO meta VALUES ( '" + mn + "' , null , " + str( mv ) + " )" )

    
    con.commit( )
    con.close( )
    return(True)

def meta_get( mn ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )

    #cur.execute( "INSERT INTO meta VALUES ( null , " + str( dk ) + " , '" + dv + "' )" )
    cur.execute( "SELECT mvs , mvn FROM meta where mn='" + mn + "' " )
    rows = cur.fetchall( )
    con.close( )
    #s_log.write( rows )

    if( len( rows ) != 1 ) : return( False )
    #s_log.write( rows )
    if( rows[ 0 ][ 0 ] == None ) : return( rows[ 0 ][ 1 ] )
    if( rows[ 0 ][ 1 ] == None ) : return( rows[ 0 ][ 0 ] )

    return(False)


def meta_add_asjson( mn , mv_data ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )

    mv = s_util.json_encode(mv_data)
    cur.execute( "INSERT INTO meta VALUES ( '" + mn + "' , '" + mv + "' , null )" )

    
    con.commit( )
    con.close( )
    return(True)

def meta_get_jsondecoded( mn ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )

    #cur.execute( "INSERT INTO meta VALUES ( null , " + str( dk ) + " , '" + dv + "' )" )
    cur.execute( "SELECT mvs FROM meta where mn='" + mn + "' " )
    rows = cur.fetchall( )
    con.close( )
    #s_log.write( rows )

    if( len( rows ) != 1 ) : return( False )
    #s_log.write( rows )

    meta_data = json.loads(rows[0][0])

    #if( rows[ 0 ][ 0 ] == None ) : return( rows[ 0 ][ 1 ] )
    #if( rows[ 0 ][ 1 ] == None ) : return( rows[ 0 ][ 0 ] )

    return(meta_data)

####################################################################

def args_add( av ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "INSERT INTO args VALUES ( null , '" + av + "' )" )
    con.commit( )
    con.close( )
    return(True)

def args_get_all( ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "SELECT av FROM args order by aid asc" )
    rows = cur.fetchall( )
    con.close( )
    s_log.write( rows )
    return( rows )  

####################################################################

def stdio_add( sk , sv ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "INSERT INTO stdio VALUES ( null , " + str( sk ) + " , '" + sv + "' )" )
    con.commit( )
    con.close( )
    return(True)

def stdio_get_bysk( sk ) :
    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    cur.execute( "SELECT * FROM stdio where sk=" + str( sk ) + " order by sid asc" )
    rows = cur.fetchall( )
    con.close( )
    s_log.write( rows )
    return( rows )    

def file_add( fp ) :

    if(s_util.pathnotallowed(fp)): return(False)

    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )

    if not os.path.isfile( fp ) :
        s_log.write( fp + " NOT exists!" )
        return( False )

    fs = os.path.getsize( fp )

    with open( fp , mode = "rb" ) as file : 
        fc = file.read( )

    fh = hashlib.md5( fc ).hexdigest( )

    sql = """ INSERT INTO files ( fp , fc , fs , fh ) VALUES (?, ?, ?, ?)"""

    data_tuple = ( fp , fc , fs , fh )
    cur.execute( sql , data_tuple )

    con.commit( )
    con.close( )

    return( True )

def file_dict2json( fp , fdict ) :

    if( s_util.pathnotallowed( fp ) ) : return( False )

    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )


    fc = s_util.json_encode( fdict )
    s_log.write(fc)

    fs = len(fc)
    fh = hashlib.md5( fc.encode('utf-8') ).hexdigest( )

    s_log.write(fs)
    s_log.write(fh)

    sql = """ INSERT INTO files ( fp , fc , fs , fh ) VALUES (?, ?, ?, ?)"""

    data_tuple = ( fp , fc , fs , fh )
    cur.execute( sql , data_tuple )

    con.commit( )
    con.close( )

    return( True )

def file_get( fp ) :

    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )

    cur.execute( "SELECT fc FROM files where fp='" + fp + "' limit 1" )
    rows = cur.fetchall( )
    con.close( )
    #s_log.write( rows )

    if( len( rows ) != 1 ) : return( False )
    #s_log.write( rows )
    return( rows[ 0 ][ 0 ] )



def templates_add( tp , tk , tv ) :

    if(s_util.pathnotallowed(tp)): return(False)

    con = sqlite3.connect( db_filepath )
    cur = con.cursor( )
    sql = "INSERT INTO templates VALUES ( null , '" + tp + "' , ' " + tk + "' , '" + tv + "' )"  
    s_log.write(sql)
    cur.execute( sql )
    con.commit( )
    con.close( )
    return(True)

