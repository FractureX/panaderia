import re
import pyodbc
from psycopg2.extras import NamedTupleCursor
from psycopg2 import errors
from typing import Any
from pydantic import PositiveInt
from fastapi import status
import json

from src.shared.config.Environment import get_environment_variables
from src.shared.models.database.idatabase import IDatabase
from src.shared.models.response.response import getJsonResponse
from src.shared.models.response.messages import getDataAlreadyExists

# Runtime Environment Configuration
env = get_environment_variables()

class SQLServer(IDatabase):
    @staticmethod
    def get_connection():
        # Construir la cadena de conexión
        connection_string = f'DRIVER={{SQL Server}};SERVER={env.DATABASE_HOSTNAME["SQLServer"]};DATABASE={env.DATABASE_NAME["SQLServer"]};UID={env.DATABASE_USERNAME["SQLServer"]};PWD={env.DATABASE_PASSWORD["SQLServer"]}'
        connection = pyodbc.connect(connection_string)
        try:
            yield connection
        finally:
            connection.close()
    
    @staticmethod
    def select(conn: pyodbc.Connection, query: str, vars: tuple | None = None, print_data = False) -> list[dict] | Exception:
        print("---------- Select ----------")
        if print_data:
            print(f"query: {query}")
            print(f"vars: {str(vars)}")
        returnValue: list[dict] = []
        try:
            mycursor: pyodbc.Cursor = conn.cursor()
            if vars:
                mycursor.execute(query, vars)
            else:
                mycursor.execute(query)
            columns = [column[0] for column in mycursor.description]
            for row in mycursor.fetchall():
                row_dict = dict(zip(columns, row))
                returnValue.append(row_dict)
        except Exception as e:
            print("Exception")
            print(str(e))
            print("--------------------------------------------")
            returnValue = e
        finally:
            if mycursor: mycursor.close()
            return returnValue
    
    @staticmethod
    def insert(conn: pyodbc.Connection, query: str, vars: tuple, print_data = False) -> bool | Exception:
        print("---------- Insert ----------")
        returnValue: list[dict] = []
        if (vars[0]) == 0: del(vars[0])
        if print_data:
            print(f"query: {query}")
            print(f"vars: {str(vars)}")
        try:
            mycursor: pyodbc.Cursor = conn.cursor()
            mycursor.execute(query, vars)
            columns = [column[0] for column in mycursor.description]
            for row in mycursor.fetchall():
                row_dict = dict(zip(columns, row))
                returnValue.append(row_dict)
        except errors.UniqueViolation as e:
            print("errors.UniqueViolation")
            print(e)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_409_CONFLICT, success=False, message=SQLServer.__filter_postgresql_error_message(e), data={})
        except Exception as e:
            print("Exception")
            print(e)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=SQLServer.__filter_postgresql_error_message(e), data={})
        finally:
            if mycursor: mycursor.close()
            return returnValue

    @staticmethod
    def update(conn: pyodbc.Connection, query: str, vars: tuple | None = None, print_data = False) -> bool | Exception:
        print("---------- Update ----------")
        if print_data:
            print(f"query: {query}")
            print(f"vars: {str(vars)}")
        returnValue: Any
        try:
            mycursor: pyodbc.Cursor = conn.cursor()
            if (vars is not None):
                mycursor.execute(query, vars)
            else:
                mycursor.execute(query=query)
            returnValue = len(mycursor.fetchall()) > 0
        except errors.UniqueViolation as e:
            print("errors.UniqueViolation")
            print(e.pgerror)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_409_CONFLICT, success=False, message=SQLServer.__filter_postgresql_error_message(e), data={})
        except Exception as e:
            print("Exception")
            print(e.pgerror)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=e.pgerror, data={})
        finally:
            if mycursor: mycursor.close()
            return returnValue

    @staticmethod
    def delete(conn: pyodbc.Connection, query: str, id: PositiveInt, print_data = False) -> bool | Exception:
        print("---------- Update ----------")
        if print_data:
            print(f"query: {query}")
            print(f"id: {id}")
        returnValue: Any
        try:
            mycursor: pyodbc.Cursor = conn.cursor()
            mycursor.execute(query, (id,))
            conn.commit()
            returnValue = len(mycursor.fetchall()) > 0
        except Exception as e:
            print("Exception")
            print(e.pgerror)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=e.pgerror, data={})
        finally:
            if mycursor: mycursor.close()
            return returnValue

    @staticmethod
    def __filter_postgresql_error_message(e: Exception) -> str:
        returnValue = str(e)
        if isinstance(e, errors.UniqueViolation):
            returnValue = ""
            matches_lang = (
                r'Key \((.*?)\)=\((.*?)\) already exists', 
                r'Ya existe la llave \((.*?)\)=\((.*?)\)'
            )
            for match_lang in matches_lang:
                matches = re.findall(match_lang, e.pgerror)
                if matches:
                    for match in matches:
                        columns = match[0].split(', ')
                        values = match[1].split(', ')
                        for column, value in zip(columns, values):
                            returnValue += ("\n" if len(returnValue) > 0 else "") + getDataAlreadyExists(dataName=value)
        print("Epa")
        return returnValue
