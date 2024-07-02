# ---- PostgreSQL ----
from src.shared.utils import ids
from src.shared.utils.tables import PostgreSQLTables

# Payment type
POSTGRESQL_PAYMENT_TYPE_SELECT_ALL      = "SELECT * FROM public.payment_type ORDER BY name ASC; "
POSTGRESQL_PAYMENT_TYPE_SELECT_BY_ID    = "SELECT * FROM public.payment_type WHERE id = %s; "

# Product
POSTGRESQL_PRODUCT_INSERT                       = "INSERT INTO public.product (id, name, description, price, min_quantity, image, id_category, id_institution, id_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id; "
POSTGRESQL_PRODUCT_SELECT_ALL                   = f"SELECT * FROM public.product WHERE id_status = {ids.SQLSERVER_STATUS_ACTIVE} ORDER BY name ASC, description ASC; "
POSTGRESQL_PRODUCT_SELECT_BY_ID                 = f"SELECT * FROM public.product WHERE id = %s AND id_status = {ids.SQLSERVER_STATUS_ACTIVE}; "
POSTGRESQL_PRODUCT_SELECT_BY_ID_INSTITUTION     = f"SELECT * FROM public.product WHERE id_institution = %s AND id_status = {ids.SQLSERVER_STATUS_ACTIVE} ORDER BY name ASC, description ASC; "
POSTGRESQL_PRODUCT_SELECT_BY_ID_SHOP            = f"SELECT public.product.*, public.product_shop.stock, public.product_shop.id AS id_product_shop, public.product_shop.id_shop FROM public.product INNER JOIN public.product_shop ON public.product.id = public.product_shop.id_product WHERE public.product_shop.id_shop = %s AND public.product.id_status = {ids.SQLSERVER_STATUS_ACTIVE} ORDER BY public.product.name ASC, public.product.description ASC; "
POSTGRESQL_PRODUCT_SELECT_BY_ID_PRODUCT_SHOP    = f"SELECT public.product.*, public.product_shop.stock, public.product_shop.id_shop, public.product_shop.id AS id_product_shop FROM public.product INNER JOIN public.product_shop ON public.product.id = public.product_shop.id_product WHERE public.product_shop.id = %s AND public.product.id_status = {ids.SQLSERVER_STATUS_ACTIVE} "
POSTGRESQL_PRODUCT_UPDATE                       = f"UPDATE public.product SET name = %s, description = %s, price = %s, min_quantity = %s, image = %s, id_category = %s, id_status = %s WHERE id = %s RETURNING id; "
POSTGRESQL_PRODUCT_UPDATE_INACTIVATE            = f"UPDATE public.product SET id_status = {ids.SQLSERVER_STATUS_INACTIVE} WHERE id = %s RETURNING id; "
POSTGRESQL_PRODUCT_UPDATE_ACTIVATE              = f"UPDATE public.product SET id_status = {ids.SQLSERVER_STATUS_ACTIVE} WHERE id = %s RETURNING id; "

# Product shop
POSTGRESQL_PRODUCT_SHOP_SELECT_BY_ID        = "SELECT * FROM public.product_shop WHERE id = %s; "
POSTGRESQL_PRODUCT_SHOP_INSERT              = "INSERT INTO public.product_shop (id_product, id_shop, stock) VALUES (%s, %s, %s) RETURNING id; "
POSTGRESQL_PRODUCT_SHOP_ADD_STOCK_UPDATE    = "UPDATE public.product_shop SET stock = stock + %s WHERE id = %s RETURNING id; "

# Category
POSTGRESQL_CATEGORY_SELECT_ALL      = "SELECT * FROM public.category ORDER BY name ASC; "
POSTGRESQL_CATEGORY_SELECT_BY_ID    = "SELECT * FROM public.category WHERE id = %s; "

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
POSTGRESQL_USER_SELECT_ALL          = f"SELECT * FROM {PostgreSQLTables.USER.value} WHERE id_status = {ids.SQLSERVER_STATUS_ACTIVE} ORDER BY username ASC; "
POSTGRESQL_USER_SELECT_BY_ID        = f"SELECT * FROM {PostgreSQLTables.USER.value} WHERE id = ? AND id_status = {ids.SQLSERVER_STATUS_ACTIVE} ORDER BY username ASC; "
POSTGRESQL_USER_SELECT_BY_EMAIL     = f"SELECT * FROM {PostgreSQLTables.USER.value} WHERE email = ? AND id_status = {ids.SQLSERVER_STATUS_ACTIVE}; "
POSTGRESQL_USER_INSERT              = f"INSERT INTO {PostgreSQLTables.USER.value} (username, password, email, id_role, id_status) OUTPUT Inserted.* VALUES (?, ?, ?, ?, ?); "
POSTGRESQL_USER_UPDATE              = f"UPDATE {PostgreSQLTables.USER.value} SET username = ?, password = ?, email = ?, updated_at = GETDATE(), id_role = ?, id_status = ? OUTPUT INSERTED.* WHERE id = ?; "
POSTGRESQL_USER_DELETE              = f"DELETE FROM {PostgreSQLTables.USER.value} WHERE id = %s RETURNING id; "

# Shop
POSTGRESQL_SHOP_INSERT                      = "INSERT INTO public.shop (name, phone, email, id_status, id_institution, id_ubication, image, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id; "
POSTGRESQL_SHOP_SELECT_ALL                  = "SELECT * FROM public.shop ORDER BY name ASC; "
POSTGRESQL_SHOP_SELECT_BY_ID                = "SELECT * FROM public.shop WHERE id = %s; "
POSTGRESQL_SHOP_SELECT_BY_INSTITUTION_ID    = "SELECT * FROM public.shop WHERE id_institution = %s; "
POSTGRESQL_SHOP_UPDATE                      = "UPDATE public.shop SET name = %s, phone = %s, email = %s, id_status = %s, image = %s WHERE id = %s RETURNING id; "

# Ubication
POSTGRESQL_UBICATION_SELECT_ALL     = "SELECT * FROM public.ubication ORDER BY name ASC; "
POSTGRESQL_UBICATION_SELECT_BY_ID   = "SELECT * FROM public.ubication WHERE id = %s ORDER BY name ASC; "
POSTGRESQL_UBICATION_INSERT         = "INSERT INTO public.ubication (name, latitude, longitude, cod_postal, id_parent) VALUES (%s, %s, %s, %s, %s) RETURNING id; "
POSTGRESQL_UBICATION_UPDATE         = "UPDATE public.ubication SET name = %s, latitude = %s, longitude = %s, cod_postal = %s, id_parent = %s WHERE id = %s RETURNING id; "

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
    return f"SELECT * FROM {table} WHERE id = ?; "
