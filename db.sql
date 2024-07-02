-- Tablas
DROP TABLE IF EXISTS [panaderia].[dbo].[order_item];
DROP TABLE IF EXISTS [panaderia].[dbo].[order];
DROP TABLE IF EXISTS [panaderia].[dbo].[invoice];
DROP TABLE IF EXISTS [panaderia].[dbo].[inventory];
DROP TABLE IF EXISTS [panaderia].[dbo].[product];
DROP TABLE IF EXISTS [panaderia].[dbo].[user];
DROP TABLE IF EXISTS [panaderia].[dbo].[role];
DROP TABLE IF EXISTS [panaderia].[dbo].[status];
DROP TABLE IF EXISTS [panaderia].[dbo].[category];

CREATE TABLE dbo.status
(
    id integer NOT NULL IDENTITY(1,1),
    name varchar(50) NOT NULL,
    CONSTRAINT PK_status PRIMARY KEY (id),
    CONSTRAINT UQ_status_name UNIQUE (name)
);

CREATE TABLE [panaderia].[dbo].[role] (
    id INT NOT NULL IDENTITY(1,1),
    name NVARCHAR(50) NOT NULL,
    CONSTRAINT role_pkey PRIMARY KEY (id),
    CONSTRAINT role_name_key UNIQUE (name)
);

CREATE TABLE [panaderia].[dbo].[category] (
    id INT NOT NULL IDENTITY(1,1),
    name NVARCHAR(50) NOT NULL,
    CONSTRAINT category_pkey PRIMARY KEY (id),
    CONSTRAINT category_name_key UNIQUE (name)
);

CREATE TABLE [panaderia].[dbo].[user] (
    id INT NOT NULL IDENTITY(1,1),
    username NVARCHAR(50) NOT NULL,
    password NVARCHAR(255) NOT NULL,
    email NVARCHAR(255) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2,
    id_role INT NOT NULL,
    id_status INT NOT NULL,
    CONSTRAINT user_pkey PRIMARY KEY (id),
    CONSTRAINT user_email_key UNIQUE (email),
    CONSTRAINT user_username_key UNIQUE (username),
    CONSTRAINT user_id_role_fkey FOREIGN KEY (id_role)
        REFERENCES [panaderia].[dbo].[role] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT user_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [panaderia].[dbo].[status] (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE [panaderia].[dbo].[product](
    id INT IDENTITY(1,1) NOT NULL,
    price NUMERIC(12, 2) NOT NULL DEFAULT (0.00),
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2,
    id_category INT NOT NULL,
    id_status INT NOT NULL,
    CONSTRAINT product_pkey PRIMARY KEY(id),
    CONSTRAINT product_id_category_fkey FOREIGN KEY (id_category)
        REFERENCES [panaderia].[dbo].[category] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT product_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [panaderia].[dbo].[status] (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE [panaderia].[dbo].[inventory](
    id INT IDENTITY(1,1) NOT NULL,
    id_product INT NOT NULL,
    quantity NUMERIC(12, 2) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2,
    id_status INT NOT NULL,
    CONSTRAINT inventory_pkey PRIMARY KEY (id),
    CONSTRAINT inventory_id_product_key UNIQUE (id_product),
    CONSTRAINT inventory_id_product_fkey FOREIGN KEY (id_product) 
        REFERENCES [panaderia].[dbo].[product] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT inventory_id_status_fkey FOREIGN KEY (id_status) 
        REFERENCES [panaderia].[dbo].[status] (id) ON DELETE NO ACTION ON UPDATE NO ACTION 
);

CREATE TABLE [panaderia].[dbo].[order] (
    id INT IDENTITY(1,1) NOT NULL,
    order_date DATETIME2 NOT NULL DEFAULT GETDATE(),
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NULL,
    id_user INT NOT NULL,
    id_status INT NOT NULL,
    CONSTRAINT order_pkey PRIMARY KEY (id),
    CONSTRAINT order_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [panaderia].[dbo].[status] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT order_id_user_fkey FOREIGN KEY (id_user)
        REFERENCES [panaderia].[dbo].[user] (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE [panaderia].[dbo].[order_item] (
    id INT IDENTITY(1,1) NOT NULL,
    id_order INT NOT NULL,
    id_product INT NOT NULL,
    quantity NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    price NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NULL,
    id_status INT NOT NULL,
    CONSTRAINT order_items_pkey PRIMARY KEY (id),
    CONSTRAINT order_items_id_order_fkey FOREIGN KEY (id_order)
        REFERENCES [panaderia].[dbo].[order] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT order_items_id_product_fkey FOREIGN KEY (id_product)
        REFERENCES [panaderia].[dbo].[product] (id) ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT order_items_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [panaderia].[dbo].[status] (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE [panaderia].[dbo].[invoice] (
    id INT IDENTITY(1,1) NOT NULL,
    id_order INT NOT NULL,
    invoice_date DATETIME2 NOT NULL DEFAULT GETDATE(),
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NULL,
    id_status INT NOT NULL,
    CONSTRAINT invoice_pkey PRIMARY KEY (id),
    CONSTRAINT invoice_id_order_key UNIQUE (id_order),
    CONSTRAINT invoice_id_order_fkey FOREIGN KEY (id_order)
        REFERENCES [panaderia].[dbo].[order] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT invoice_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [panaderia].[dbo].[status] (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);
