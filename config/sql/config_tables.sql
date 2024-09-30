DROP TABLE IF EXISTS config_event;

CREATE TABLE config_event (
	event_id INTEGER PRIMARY KEY AUTOINCREMENT
	, event_name NVARCHAR(100) NULL
	, event_start_date DATE NULL
	, event_end_date DATE NULL
 );

DROP TABLE IF EXISTS config_format;

CREATE TABLE config_format(
	format_id INTEGER PRIMARY KEY AUTOINCREMENT
	, format_name NVARCHAR(100) NULL
);

DROP TABLE IF EXISTS config_source_type;

CREATE TABLE config_source_type (
	source_type_id INTEGER PRIMARY KEY AUTOINCREMENT
	, source_type_name NVARCHAR(100) NULL
);

DROP TABLE IF EXISTS config_source;

CREATE TABLE config_source(
	source_id INTEGER PRIMARY KEY AUTOINCREMENT
	, event_id INTEGER NOT NULL REFERENCES config_event(event_id)
	, source_type_id INTEGER NOT NULL REFERENCES config_source_type(source_type_id)
	, format_id INTEGER NOT NULL REFERENCES config_format(format_id)
	, source_name NAVARCHAR(100) NULL
	, url NVARCHAR(500) NULL
);

DROP TABLE IF EXISTS config_api_parameter;

CREATE TABLE config_api_parameter (
	api_patameter_id INTEGER PRIMARY KEY AUTOINCREMENT
	, source_id INTEGER NOT NULL REFERENCES config_source(source_id)
	, api_patameter NVARCHAR(500) NULL
);

ALTER TABLE config_source RENAME TO config_source_old;

DROP TABLE IF EXISTS config_source;

CREATE TABLE config_source(
	source_id INTEGER PRIMARY KEY AUTOINCREMENT
	, event_id INTEGER NOT NULL REFERENCES config_event(event_id)
	, source_type_id INTEGER NOT NULL REFERENCES config_source_type(source_type_id)
	, format_id INTEGER NOT NULL REFERENCES config_format(format_id)
	, source_name NAVARCHAR(100) NULL
	, url NVARCHAR(500) NULL
);

DROP TABLE IF EXISTS config_source_old;

DROP TABLE IF EXISTS config_api_parameter;

CREATE TABLE config_api_parameter (
	api_patameter_id INTEGER PRIMARY KEY AUTOINCREMENT
	, source_id INTEGER NOT NULL REFERENCES config_source(source_id)
	, api_patameter NVARCHAR(500) NULL
);

