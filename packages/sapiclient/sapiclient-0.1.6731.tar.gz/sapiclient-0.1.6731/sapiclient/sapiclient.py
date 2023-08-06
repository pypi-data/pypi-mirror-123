
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

import os
import io
import json

#####################################################################

from . import s_log , s_config , s_net , s_cache , s_util , s_db 

#####################################################################

isready = True

#####################################################################

s_log.write( "    ####    ####    ####    ####" )

#####################################################################

if not s_config.init( ) :
    isready = False
    s_log.write( "Not ready!" )

#s_log.write( s_config.get_config( ) )

#####################################################################

def ready( ) :
    return( isready )

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

def config_init_fromfile( config_path = "local_sapiclient_config.json" , config_key = "sapiclient" ) :
    return s_config.init_fromfile( config_path , config_key )

#####################################################################

def net_client_job_set( payload ) :
    return( s_net.client_job_set( payload ) )
def net_client_job_get( jid ) :
    return( s_net.client_job_get( jid ) )

