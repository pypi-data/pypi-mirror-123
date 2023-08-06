
#####################################################################
#
# sapiclient.py
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

from . import s_log , s_config , s_net , s_cache , s_util , s_db 

#####################################################################

s_log.write( "    ####    ####    ####    ####" )

#####################################################################

s_config.setup( )
s_db.setup( )

#####################################################################

def ready( ) :
    if( not s_config.config_ready_get( ) ) :
        return( False )

    return( True )

#####################################################################

# DATA
# TIMEOUT
def process( d = { } , waittimeout = 10 ) :

    s_db.setup( )

    #####################################################################

    f = s_db.meta_set( "_" , d ) 

    if( not f ) :
        s_log.write( "false meta_add " + k , "process" )
        return( False )

    #####################################################################
    jid = s_net.client_jobset( )
    if(not jid):
        s_log.write( "false client_jobset jid" , "process" )
        return( True )

    if( not s_net.client_jobwait( jid , waittimeout ) ) :
        s_log.write( "false client_jobwait" , "process" )
        return( False )



    return( s_db.meta_get( "_" ) )