-- Tablas
--DROP DATABASE IF EXISTS proyecto;
--CREATE DATABASE proyecto;

DROP TABLE IF EXISTS [proyecto].[dbo].[order_item];
DROP TABLE IF EXISTS [proyecto].[dbo].[order];
DROP TABLE IF EXISTS [proyecto].[dbo].[invoice];
DROP TABLE IF EXISTS [proyecto].[dbo].[inventory];
DROP TABLE IF EXISTS [proyecto].[dbo].[product];
DROP TABLE IF EXISTS [proyecto].[dbo].[user];
DROP TABLE IF EXISTS [proyecto].[dbo].[role];
DROP TABLE IF EXISTS [proyecto].[dbo].[status];
DROP TABLE IF EXISTS [proyecto].[dbo].[category];

CREATE TABLE [proyecto].[dbo].[status] (
    id integer NOT NULL IDENTITY(1,1),
    name varchar(50) NOT NULL,
    CONSTRAINT PK_status PRIMARY KEY (id),
    CONSTRAINT UQ_status_name UNIQUE (name)
);

CREATE TABLE [proyecto].[dbo].[role] (
    id INT NOT NULL IDENTITY(1,1),
    name NVARCHAR(50) NOT NULL,
    CONSTRAINT role_pkey PRIMARY KEY (id),
    CONSTRAINT role_name_key UNIQUE (name)
);

CREATE TABLE [proyecto].[dbo].[category] (
    id INT NOT NULL IDENTITY(1,1),
    name NVARCHAR(50) NOT NULL,
    CONSTRAINT category_pkey PRIMARY KEY (id),
    CONSTRAINT category_name_key UNIQUE (name)
);

CREATE TABLE [proyecto].[dbo].[user] (
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
        REFERENCES [proyecto].[dbo].[role] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT user_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [proyecto].[dbo].[status] (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE [proyecto].[dbo].[product]
(
    id int IDENTITY(1,1) PRIMARY KEY,
    name varchar(128) NOT NULL,
    description varchar(255) NOT NULL,
    price numeric(12,2) NOT NULL DEFAULT 0.00,
    image varchar(255),
    created_at datetime2 NOT NULL DEFAULT GETDATE(),
    updated_at datetime2,
    id_category int NOT NULL,
    id_status int NOT NULL,
    CONSTRAINT product_name_description_key UNIQUE (name, description),
    CONSTRAINT FK_product_category FOREIGN KEY (id_category)
        REFERENCES dbo.category (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_product_status FOREIGN KEY (id_status)
        REFERENCES dbo.status (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE [proyecto].[dbo].[inventory] (
    id INT IDENTITY(1,1) NOT NULL,
    id_product INT NOT NULL,
    quantity NUMERIC(12, 2) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2,
    id_status INT NOT NULL,
    CONSTRAINT inventory_pkey PRIMARY KEY (id),
    CONSTRAINT inventory_id_product_key UNIQUE (id_product),
    CONSTRAINT inventory_id_product_fkey FOREIGN KEY (id_product) 
        REFERENCES [proyecto].[dbo].[product] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT inventory_id_status_fkey FOREIGN KEY (id_status) 
        REFERENCES [proyecto].[dbo].[status] (id) ON DELETE NO ACTION ON UPDATE NO ACTION 
);

CREATE TABLE [proyecto].[dbo].[order] (
    id INT IDENTITY(1,1) NOT NULL,
    order_date DATETIME2 NOT NULL DEFAULT GETDATE(),
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NULL,
    id_user INT NOT NULL,
    id_status INT NOT NULL,
    CONSTRAINT order_pkey PRIMARY KEY (id),
    CONSTRAINT order_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [proyecto].[dbo].[status] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT order_id_user_fkey FOREIGN KEY (id_user)
        REFERENCES [proyecto].[dbo].[user] (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE [proyecto].[dbo].[order_item] (
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
        REFERENCES [proyecto].[dbo].[order] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT order_items_id_product_fkey FOREIGN KEY (id_product)
        REFERENCES [proyecto].[dbo].[product] (id) ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT order_items_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [proyecto].[dbo].[status] (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE [proyecto].[dbo].[invoice] (
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
        REFERENCES [proyecto].[dbo].[order] (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT invoice_id_status_fkey FOREIGN KEY (id_status)
        REFERENCES [proyecto].[dbo].[status] (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

INSERT INTO [proyecto].[dbo].[role] (name) VALUES ('Administrador'), ('Personal'); 
INSERT INTO [proyecto].[dbo].[category] (name) VALUES ('Panadería'), ('Pastelería'), ('Bebidas'); 
INSERT INTO [proyecto].[dbo].[status] (name) VALUES ('Activo'), ('Inactivo'), ('Pagado'), ('No pagado'); 
INSERT INTO [proyecto].[dbo].[user] (username, password, email, id_role, id_status) VALUES ('administrador', '$2b$12$20bIutLFKlLo8ckty31fKe/wsjUNLS6C6TG6Q81CEVhRX1BkjEoJ2', 'administrador@gmail.com', 1, 1); 
