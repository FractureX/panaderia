from enum import Enum

from src.shared.config.Environment import get_environment_variables

_env = get_environment_variables()

class PostgreSQLTables(Enum):
    USER    = f'[{_env.DATABASE_NAME.get("SQLServer")}].[dbo].[user]'
