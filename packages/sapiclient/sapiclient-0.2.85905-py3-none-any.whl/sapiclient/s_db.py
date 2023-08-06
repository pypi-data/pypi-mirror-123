
#####################################################################
#
# s_db.py
#
# Project   : SAPICLIENT
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
db_dirty = False
db_con = False

#####################################################################

def setup( ) :

    global db_con

    if( db_con != False ) :
        if( db_con_check( ) ) :
            db_con.commit( )
            db_con.close( )
            db_con = False 
            #s_log.write( "Closed db_con" ) 

    db_filepath_setup( )

    if( os.path.isfile( db_filepath ) ) :
        os.remove( db_filepath )

    db_con_setup( )

    init_schema( )

    if( os.path.isfile( db_filepath ) ) :
        return( True )

    s_log.write( "False db_filepath isfile" ) 

    return( False )


def file_contents( ) :

    if not os.path.isfile( db_filepath ) :
        s_log.write( db_filepath + " NOT exists!" )
        return( False )

    with open( db_filepath , mode = "rb" ) as file : 
        db_filecontents = file.read( )

    return( db_filecontents )


def rewrite( payload ) :

    disconnect( )

    with open( db_filepath , "wb" ) as file:
        file.write( payload )

    reconnect( )

def reconnect( ) :

    global db_con

    if( db_con != False ) :
        if( db_con_check( ) ) :
            db_con.commit( )
            db_con.close( )
            db_con = False 
            #s_log.write( "Closed db_con" ) 

    db_con_setup( )

def disconnect( ) :

    global db_con

    if( db_con != False ) :
        if( db_con_check( ) ) :
            db_con.commit( )
            db_con.close( )
            db_con = False 
            #s_log.write( "Closed db_con" ) 

def db_con_setup( ) :

    global db_con

    if( db_con != False ) : return

    db_con = sqlite3.connect( db_filepath_get( ) )
    #db_con.row_factory = sqlite3.Row
    db_con.row_factory = lambda C, R: { c[0]: R[i] for i, c in enumerate(C.description) }

    #s_log.write( "OK db_con_setup" )

def db_con_check( ) :
    global db_con
    try :
        db_con.cursor( )
        return( True )
    except Exception as ex :
        return( False )

#####################################################################

def db_filepath_setup( ) :

    global db_filepath

    if( db_filepath != False ) :
        return

    dbworkspacedir = os.path.join( s_config.get_key( "sys/workspacedir" , "/tmp/sapiclient" ) + "/db" , "" )

    os.makedirs( dbworkspacedir , exist_ok = True )

    db_filepath = dbworkspacedir + s_config.get_key( "/config/session" ) + ".db" 

def db_filepath_get( ) :
    return( db_filepath )

#####################################################################

def db_dirty_get( ) :
    return( db_dirty )

#####################################################################

def sql_execute( sql ) :
    #s_log.write(sql)
    cur = db_con.cursor( )
    cur.execute( sql )
    db_con.commit( )

def sql_execute_parameters( sql , params_tuple ) :

    cur = db_con.cursor( )
    cur.execute( sql , params_tuple )
    db_con.commit( )

def sql_execute_fetchall( sql ) :
    cur = db_con.cursor( )
    cur.execute( sql )
    rows = cur.fetchall( )
    return( rows )

#####################################################################

def init_schema( ) :

    sql_execute( "CREATE TABLE sys ( sn text , svs text , svn real )" )
    sql_execute( "CREATE INDEX index_sys ON sys ( sn )" )

    sql_execute( "INSERT INTO sys VALUES ( 'ver' , null , 1 )" )
    sql_execute( "INSERT INTO sys VALUES ( 'serial' , 'ODS042e1919c5bd8f41cd8e1a2b8e455dd8f6fb00df0c3916d1137047a7aafc4c42' , null )" )

    ################################################################

    sql_execute( "CREATE TABLE files ( fp text , fc blob , fs integer , fh text )" )
    sql_execute( "CREATE INDEX index_files ON files ( fp )" )

    ################################################################

    sql_execute( "CREATE TABLE env ( eid integer PRIMARY KEY AUTOINCREMENT , en text , ev text )" )
    sql_execute( "CREATE INDEX index_env ON env ( eid , en )" )

    ################################################################

    sql_execute( "CREATE TABLE stdio ( sid integer PRIMARY KEY AUTOINCREMENT , sk integer , sv text )" )
    sql_execute( "CREATE INDEX index_stdio ON stdio ( sid , sk )" )

    ################################################################

    sql_execute( "CREATE TABLE args ( aid integer PRIMARY KEY AUTOINCREMENT , av text )" )
    sql_execute( "CREATE INDEX index_args ON args ( aid )" )

    ################################################################

    sql_execute( "CREATE TABLE stacks ( sid integer PRIMARY KEY AUTOINCREMENT , sk integer , sv text )" )
    sql_execute( "CREATE INDEX index_stacks ON stacks ( sid , sk )" )

    ################################################################

    sql_execute( "CREATE TABLE meta ( mn text , mv text )" )
    sql_execute( "CREATE INDEX index_meta ON meta ( mn )" )

    ################################################################

    sql_execute( "CREATE TABLE templates ( tid integer PRIMARY KEY AUTOINCREMENT , tp text , tk text , tv text )" )
    sql_execute( "CREATE INDEX index_templates ON templates ( tid , tp )" )

#####################################################################

def sys_get( sn ) :

    sql = "SELECT * FROM sys where sn='" + sn + "' limit 1"
    rows = sql_execute_fetchall( sql )

    if( len( rows ) != 1 ) : return( False )

    row = rows[ 0 ]

    if( row[ "svs" ] == None ) : return( row[ "svn" ] )
    if( row[ "svn" ] == None ) : return( row[ "svs" ] )
    
    return( False )

#####################################################################

def stacks_push( sv_data , sk = 0 ) :

    sv = s_util.json_encode( sv_data )

    sql = "INSERT INTO stacks VALUES ( null , " + str( sk ) + " , '" + sv + "' )"
    sql_execute( sql ) 

    return( True )

def stacks_pop( sk = 0 ) :

    sql = "SELECT * FROM stacks where sk=" + str( sk ) + " order by sid desc limit 1" 
    rows = sql_execute_fetchall( sql )

    if( len( rows ) != 1 ) :
        return( False )

    row = rows[ 0 ]
   
    sid = row[ "sid" ]
    sv_dict = json.loads( row[ "sv" ] )

    sql = "DELETE FROM stacks where sid=" + str( sid ) + " limit 1"
    sql_execute( sql )

    return( sv_dict )    

def stacks_peek( sk = 0 ) :

    sql = "SELECT * FROM stacks where sk=" + str( sk ) + " order by sid asc" 
    rows = sql_execute_fetchall( sql )

    return( rows )    

def stacks_peekall( ) :

    sql = "SELECT * FROM stacks order by sid asc" 
    rows = sql_execute_fetchall( sql )

    return( rows )  

def stacks_flush( sk = 0 ) :

    sql = "DELETE FROM stacks where sk = " + str( sk ) 
    sql_execute( sql )

    return( True )    

def stacks_truncate( ) :

    sql = "DELETE from stacks" 
    sql_execute( sql )

    return( True )    

def stacks_count( sk = 0 ) :

    sql = "SELECT COUNT(*) as count FROM stacks where sk=" + str( sk ) 
    rows = sql_execute_fetchall( sql )

    if( len( rows ) != 1 ) :
        return( False )

    row=rows[0]
    return( row[ "count" ] )

#####################################################################

def env_add( en , ev ) :

    sql = "INSERT INTO env VALUES ( null, '" + en + "' , '" + ev + "' )"
    sql_execute( sql )

    return( True )

def env_get_all( ) :
    
    sql = "SELECT * FROM env order by eid"
    rows = sql_execute_fetchall( sql )

    return( rows )  

#####################################################################

def meta_set( mn , mv_in ) :

    mv = s_util.json_encode( mv_in )

    sql = "INSERT INTO meta VALUES ( '" + str( mn ) + "', '" + mv + "' )"
    sql_execute( sql )

    return( True )

def meta_get( mn ) :

    sql =  "SELECT * FROM meta where mn='" + mn + "' limit 1" 
    rows = sql_execute_fetchall( sql )

    if( len( rows ) != 1 ) : return( False )

    row = rows[ 0 ]

    return( json.loads( row[ "mv" ] ) )

####################################################################

def args_add( av ) :

    sql = "INSERT INTO args VALUES ( null , '" + av + "' )" 
    sql_execute( sql )
    return( True )

def args_get_all( ) :
    sql = "SELECT * FROM args order by aid asc" 
    rows = sql_execute_fetchall( sql )
    return( rows )  

####################################################################

def stdio_add( sk , sv ) :
    sql = "INSERT INTO stdio VALUES ( null , " + str( sk ) + " , '" + sv + "' )" 
    sql_execute( sql )
    return( True )

def stdio_get( sk ) :
    sql = "SELECT * FROM stdio where sk=" + str( sk ) + " order by sid asc" 
    rows = sql_execute_fetchall( sql )
    return( rows )    

def stdio_flush( sk = 0 ) :

    sql = "DELETE FROM stdio where sk = " + str( sk ) 
    sql_execute( sql )

    return( True )    

def stdio_truncate( ) :

    sql = "DELETE from stdio" 
    sql_execute( sql )

    return( True )    

####################################################################

def file_add( fp ) :

    if( s_util.pathnotallowed( fp ) ) : return( False )

    ####################################################################

    if not os.path.isfile( fp ) :
        s_log.write( fp + " NOT found!" )
        return( False )

    fs = os.path.getsize( fp )

    with open( fp , mode = "rb" ) as file : 
        fc = file.read( )

    fh = hashlib.md5( fc ).hexdigest( )

    ####################################################################

    sql = "INSERT INTO files ( fp , fc , fs , fh ) VALUES (?, ?, ?, ?)"
    data_tuple = ( fp , fc , fs , fh )

    sql_execute_parameters( sql , data_tuple )

    return( True )

def file_dict2json( fp , fdict ) :

    if( s_util.pathnotallowed( fp ) ) : return( False )

    fc = s_util.json_encode( fdict )

    fs = len( fc )
    fh = hashlib.md5( fc.encode( "utf-8" ) ).hexdigest( )

    sql = "INSERT INTO files ( fp , fc , fs , fh ) VALUES (?, ?, ?, ?)"
    data_tuple = ( fp , fc , fs , fh )
    sql_execute_parameters( sql , data_tuple )

    return( True )

def file_get( fp ) :

    sql =  "SELECT * FROM files where fp='" + fp + "' limit 1" 
    rows = sql_execute_fetchall( sql )

    if( len( rows ) != 1 ) : return( False )

    row = rows[ 0 ]
    return( row )

def file_delete( fp ) :

    sql = "DELETE FROM files where fp='" + fp + "' limit 1"
    sql_execute( sql )

    return( True )    

####################################################################

def templates_set( tp , tk , tv ) :

    if( s_util.pathnotallowed( tp ) ) : return( False )

    sql = "INSERT INTO templates VALUES ( null , '" + tp + "' , ' " + tk + "' , '" + tv + "' )"  
    sql_execute( sql )
    return( True )

def templates_get( ) :
    sql = "SELECT * FROM templates order by tid asc" 
    rows = sql_execute_fetchall( sql )
    return( rows ) 

def templates_truncate( ) :

    sql = "DELETE from templates" 
    sql_execute( sql )

    return( True )   
