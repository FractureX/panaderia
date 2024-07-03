# ---- PostgreSQL ----
from src.shared.utils import ids
from src.shared.utils.tables import SQLServerTables
from src.shared.config.Environment import get_environment_variables

_env = get_environment_variables()

# Payment type
POSTGRESQL_PAYMENT_TYPE_SELECT_ALL      = "SELECT * FROM public.payment_type ORDER BY name ASC; "
POSTGRESQL_PAYMENT_TYPE_SELECT_BY_ID    = "SELECT * FROM public.payment_type WHERE id = %s; "

# Product
POSTGRESQL_PRODUCT_INSERT                       = f"INSERT INTO [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.PRODUCT.value}] (name, description, price, id_category, id_status) OUTPUT INSERTED.* VALUES (?, ?, ?, ?, ?); "
POSTGRESQL_PRODUCT_SELECT_ALL                   = f"SELECT p.*, i.quantity FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.PRODUCT.value}] p INNER JOIN [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.INVENTORY.value}] i ON p.id = i.id_product WHERE p.id_status = {ids.SQLSERVER_STATUS_ACTIVE} ORDER BY p.name ASC, p.description ASC; "
POSTGRESQL_PRODUCT_SELECT_BY_ID                 = f"SELECT p.*, i.quantity FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.PRODUCT.value}] p INNER JOIN [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.INVENTORY.value}] i ON p.id = i.id_product WHERE p.id = ? AND p.id_status = {ids.SQLSERVER_STATUS_ACTIVE}; "
POSTGRESQL_PRODUCT_SELECT_BY_ID_CATEGORY        = f"SELECT p.*, i.quantity FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.PRODUCT.value}] p INNER JOIN [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.INVENTORY.value}] i ON p.id = i.id_product WHERE p.id_category = ? AND p.id_status = {ids.SQLSERVER_STATUS_ACTIVE}; "
POSTGRESQL_PRODUCT_UPDATE                       = f"UPDATE [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.PRODUCT.value}] SET name = ?, description = ?, price = ?, image = ?, id_category = ?, id_status = ?, updated_at = GETDATE() OUTPUT INSERTED.* WHERE id = ?; "
POSTGRESQL_PRODUCT_UPDATE_IMAGE                 = f"UPDATE [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.PRODUCT.value}] SET image = ? OUTPUT INSERTED.* WHERE id = ?; "
POSTGRESQL_PRODUCT_DELETE                       = f"DELETE FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.PRODUCT.value}] OUTPUT DELETED.* WHERE id = ?; "

# Product shop
POSTGRESQL_PRODUCT_SHOP_SELECT_BY_ID        = "SELECT * FROM public.product_shop WHERE id = %s; "
POSTGRESQL_PRODUCT_SHOP_INSERT              = "INSERT INTO public.product_shop (id_product, id_shop, stock) VALUES (%s, %s, %s) RETURNING id; "
POSTGRESQL_PRODUCT_SHOP_ADD_STOCK_UPDATE    = "UPDATE public.product_shop SET stock = stock + %s WHERE id = %s RETURNING id; "

# Category
POSTGRESQL_CATEGORY_SELECT_ALL      = f"SELECT * FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.CATEGORY.value}] ORDER BY name ASC; "

# Role
POSTGRESQL_ROLE_SELECT_ALL      = "SELECT * FROM public.role; "
POSTGRESQL_ROLE_SELECT_BY_ID    = "SELECT * FROM public.role WHERE id = %s; "
POSTGRESQL_ROLE_INSERT          = "INSERT INTO public.role (name) VALUES (%s) RETURNING id; "
POSTGRESQL_ROLE_UPDATE          = "UPDATE public.role SET name = %s WHERE id = %s RETURNING id; "
POSTGRESQL_ROLE_DELETE          = "DELETE FROM public.role WHERE id = %s RETURNING id; "

# Credential
POSTGRESQL_CREDENTIAL_SELECT_BY_ID  = "SELECT * FROM public.credentials WHERE id = %s; "
POSTGRESQL_CREDENTIAL_INSERT        = "INSERT INTO public.credential (email, password) VALUES (%s, %s) RETURNING id; "
POSTGRESQL_CREDENTIAL_UPDATE        = "UPDATE public.credential SET email = %s, password = %s WHERE email = (SELECT email FROM public.user WHERE id = %s) RETURNING id; "

# User
POSTGRESQL_USER_SELECT_ALL          = f"SELECT * FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.USER.value}] WHERE id_status = {ids.SQLSERVER_STATUS_ACTIVE} ORDER BY username ASC; "
POSTGRESQL_USER_SELECT_BY_ID        = f"SELECT * FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.USER.value}] WHERE id = ? AND id_status = {ids.SQLSERVER_STATUS_ACTIVE} ORDER BY username ASC; "
POSTGRESQL_USER_SELECT_BY_USERNAME  = f"SELECT * FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.USER.value}] WHERE username = ? AND id_status = {ids.SQLSERVER_STATUS_ACTIVE}; "
POSTGRESQL_USER_INSERT              = f"INSERT INTO [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.USER.value}] (username, password, email, id_role, id_status) OUTPUT INSERTED.* VALUES (?, ?, ?, ?, ?); "
POSTGRESQL_USER_UPDATE              = f"UPDATE [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.USER.value}] SET username = ?, password = ?, email = ?, updated_at = GETDATE(), id_role = ?, id_status = ? OUTPUT INSERTED.* WHERE id = ?; "
POSTGRESQL_USER_DELETE              = f"DELETE FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.USER.value}] OUTPUT DELETED.* WHERE id = ?; "

# Inventory
POSTGRESQL_INVENTORY_INSERT                 = f"INSERT INTO [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.INVENTORY.value}] (id_product, quantity, id_status) OUTPUT INSERTED.* VALUES (?, ?, ?); "
POSTGRESQL_INVENTORY_UPDATE_ADD             = f"UPDATE [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.INVENTORY.value}] SET quantity = quantity + ?, updated_at = GETDATE() OUTPUT INSERTED.* WHERE id_product = ?; "
POSTGRESQL_INVENTORY_SELECT_BY_ID_PRODUCT   = f"SELECT * FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.INVENTORY.value}] i INNER JOIN [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.PRODUCT.value}] p ON i.id_product = p.id WHERE p.id = ? AND p.id_status = {ids.SQLSERVER_STATUS_ACTIVE}; "
POSTGRESQL_INVENTORY_UPDATE_STOCK           = f"UPDATE [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.INVENTORY.value}] SET quantity = quantity - (SELECT quantity FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER_ITEM.value}] WHERE id_order = ? AND id_product = ?), updated_at = GETDATE() OUTPUT INSERTED.* WHERE id_product = ?; "

# Order
POSTGRESQL_ORDER_SELECT_ALL     = f"SELECT * FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER.value}] ORDER BY order_date ASC; "
POSTGRESQL_ORDER_SELECT_BY_ID   = f"SELECT * FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER.value}] WHERE id = ?; "
POSTGRESQL_ORDER_INSERT         = f"INSERT INTO [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER.value}] (id_user, id_status) OUTPUT INSERTED.* VALUES (?, {ids.SQLSERVER_STATUS_NO_PAGADO}); "
POSTGRESQL_ORDER_UPDATE_TOTAL   = f"UPDATE [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER.value}] SET total_amount = (SELECT SUM(oi.quantity * oi.price) FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER_ITEM.value}] oi WHERE id_order = ?), updated_at = GETDATE() OUTPUT INSERTED.* WHERE id = ?; "
POSTGRESQL_ORDER_UPDATE_PAGADO  = f"UPDATE [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER.value}] SET id_status = {ids.SQLSERVER_STATUS_PAGADO}, updated_at = GETDATE() OUTPUT INSERTED.* WHERE id = ?; "

# Order item
POSTGRESQL_ORDER_ITEM_INSERT                = f"INSERT INTO [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER_ITEM.value}] (id_order, id_product, quantity, price, id_status) OUTPUT INSERTED.* VALUES (?, ?, ?, ?, {ids.SQLSERVER_STATUS_NO_PAGADO}); "
POSTGRESQL_ORDER_ITEM_UPDATE_PAGADO         = f"UPDATE [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER_ITEM.value}] SET id_status = {ids.SQLSERVER_STATUS_PAGADO}, updated_at = GETDATE() OUTPUT INSERTED.* WHERE id_order = ?; "
POSTGRESQL_ORDER_ITEM_SELECT_BY_ID_ORDER    = f"SELECT id_product FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER_ITEM.value}] WHERE id_order = ?; "

# Invoice
POSTGRESQL_INVOICE_INSERT       = f"INSERT INTO [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.INVOICE.value}] (id_order, total_amount, id_status) OUTPUT INSERTED.* VALUES (?, (SELECT o.total_amount FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{SQLServerTables.ORDER.value}] o WHERE id = ?), {ids.SQLSERVER_STATUS_PAGADO}); "

# Status
POSTGRESQL_STATUS_SELECT_BY_ID = "SELECT * FROM public.status WHERE id = %s; "

# Institution
POSTGRESQL_INSTITUTION_SELECT_ALL           = "SELECT * FROM public.institution; "
POSTGRESQL_INSTITUTION_SELECT_BY_ID         = "SELECT * FROM public.institution WHERE id = %s; "
POSTGRESQL_INSTITUTION_SELECT_MAX_ID        = "SELECT * FROM public.institution LIMIT 1 ORDER BY id DESC; "
POSTGRESQL_INSTITUTION_INSERT               = "INSERT INTO public.institution (name, type, description, phone, email, id_ubication, id_status, image, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id; "
POSTGRESQL_INSTITUTION_UPDATE               = "UPDATE public.institution SET name = %s, type = %s, description = %s, phone = %s, email = %s, id_ubication = %s, id_status = %s, image = %s WHERE id = %s RETURNING id; "
POSTGRESQL_INSTITUTION_UPDATE_INACTIVATE    = f"UPDATE public.institution SET id_status = {ids.SQLSERVER_STATUS_INACTIVE} WHERE id = %s RETURNING id; "
POSTGRESQL_INSTITUTION_UPDATE_ACTIVATE      = f"UPDATE public.institution SET id_status = {ids.SQLSERVER_STATUS_ACTIVE} WHERE id = %s RETURNING id; "

# Credits history
POSTGRESQL_CREDITS_HISTORY_SELECT_BY_USER_ID    = "SELECT * FROM public.credits_history WHERE id = %s; "
POSTGRESQL_CREDITS_HISTORY_INSERT               = "INSERT INTO public.credits_history (movement_type, credits, id_user, id_user_cashier) VALUES (%s, %s, %s, %s) RETURNING id; "

# Membership
POSTGRESQL_MEMBERSHIP_SELECT_ALL                = "SELECT * FROM public.membership; "
POSTGRESQL_MEMBERSHIP_SELECT_BY_ID              = "SELECT * FROM public.membership WHERE id = %s; "
POSTGRESQL_MEMBERSHIP_SELECT_BY_INSTITUTION_ID  = "SELECT * FROM public.membership WHERE id_institution = %s; "
POSTGRESQL_MEMBERSHIP_INSERT                    = "INSERT INTO public.membership (shop_count, date_begin, date_end, id_institution, price) VALUES (%s, %s, %s, %s, %s) RETURNING id; "
POSTGRESQL_MEMBERSHIP_UPDATE                    = "UPDATE public.membership SET shop_count = %s, date_begin = %s, date_end = %s, price = %s WHERE id = %s RETURNING id; "

# Membership prices
POSTGRESQL_MEMBERSHIP_PRICE_SELECT_ALL              = "SELECT * FROM public.membership_price ORDER BY shop_count ASC; "
POSTGRESQL_MEMBERSHIP_PRICE_SELECT_BY_SHOP_COUNT    = "SELECT public.calculate_membership_price(%s) AS price; "
POSTGRESQL_MEMBERSHIP_PRICE_INSERT                  = "INSERT INTO public.membership_price (shop_count, price) VALUES (%s, %s) RETURNING id; "
POSTGRESQL_MEMBERSHIP_PRICE_UPDATE                  = "UPDATE public.membership_price SET shop_count = %s, price = %s WHERE id = %s RETURNING id; "

# Notification
POSTGRESQL_NOTIFICATION_SELECT_BY_USER_ID   = "SELECT public.notification.*, public.notification_detail.read FROM public.notification INNER JOIN public.notification_detail ON public.notification.id = public.notification_detail.id_notification WHERE public.notification_detail.id_user = %s ORDER BY public.notification.date DESC; "
POSTGRESQL_NOTIFICATION_INSERT              = "INSERT INTO public.notification (type, title, description, date, id_institution) VALUES (%s, %s, %s, NOW(), %s) RETURNING id; "

# Notification detail
POSTGRESQL_NOTIFICATION_DETAIL_INSERT   = "INSERT INTO public.notification_detail (id_notification, id_user, read) VALUES (%s, %s, false) RETURNING id; "

def getSelectQueryById(table: str) -> str:
    return f"SELECT * FROM [{_env.DATABASE_NAME.get('SQLServer')}].[dbo].[{table}] WHERE id = ?; "
