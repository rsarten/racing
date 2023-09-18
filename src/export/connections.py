import sys
from psycopg2 import connect
from psycopg2 import OperationalError, errorcodes, errors
from psycopg2 import __version__ as psycopg2_version
from sqlalchemy import create_engine

def get_engine(password):
    return create_engine(f"postgresql+psycopg2://rory:{password}@localhost:5432/horse_racing")

def print_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occured
    line_num = traceback.tb_lineno

    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)
    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)
    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

def get_connection(password):
    try:
        conn = connect(
            database="horse_racing",
            host="localhost",
            user="rory",
            password=password,
            port="5432")
    except OperationalError as err:
        print_psycopg2_exception(err)
        conn = None
    return conn

