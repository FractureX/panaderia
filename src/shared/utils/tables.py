from enum import Enum

from src.shared.config.Environment import get_environment_variables

_env = get_environment_variables()

class SQLServerTables(Enum):
    USER        = 'user'
    CATEGORY    = 'category'
    PRODUCT     = 'product'
    INVENTORY   = 'inventory'
    ORDER       = 'order'
    ORDER_ITEM  = 'order_item'
    INVOICE     = 'invoice'
