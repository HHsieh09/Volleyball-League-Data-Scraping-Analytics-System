import time
import typing
from loguru import logger
from sqlalchemy import engine
from volleyballdata import clients

def check_alive(connect: engine.base.Connection,):
    connect.execute("Select 1 + 1")

"""Automatically reconnect while the connection is malfunctioning"""
def reconnect(connect_func: typing.Callable,) -> engine.base.Connection:
    try:
        connect = connect_func
    except Exception as e:
        logger.info(f"{connect_func.__name__} reconnect, error: {e}")
    return connect

"""Check if the connection is still alive"""
def check_connect_alive(connect: engine.base.Connection,
                        connect_func: typing.Callable):
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            logger.info(f"{connect_func.__name__} connect, error: {e}")
            time.sleep(1)
            connect = reconnect(connect_func)
            return check_connect_alive(connect,connect_func)
        
class Router:
    def __init__(self):
        self._mysql_volleyballdata_conn = clients.get_mysql_volleyballdata_conn()
    
    def check_mysql_volleyballdata_conn_alive(self,):
        self._mysql_volleyballdata_conn = check_connect_alive(
            self._mysql_volleyballdata_conn,
            clients.get_mysql_volleyballdata_conn,
        )
        return self._mysql_volleyballdata_conn
    
    @property
    def mysql_volleyball_conn(self):
        """
        Use property to make sure that ever time 'connect' is accessed,
        a 'check alive' verification is performed to determine if the connection is still alive
        """
        return self.check_mysql_volleyballdata_conn_alive()