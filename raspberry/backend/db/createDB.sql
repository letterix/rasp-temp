PRAGMA foreign_keys = OFF;


DROP TABLE IF EXISTS "installation";
CREATE TABLE "installation" (
  "serial_number" VARCHAR(45) NOT NULL,
  "model" VARCHAR(45) NOT NULL,
  PRIMARY KEY ("serial_number")
);

DROP TABLE IF EXISTS "user_role_enums";
CREATE TABLE "user_role_enums" (
  "role" varchar(50) NOT NULL,
  PRIMARY KEY ("role")
);
INSERT INTO "user_role_enums"("role") VALUES ("user");
INSERT INTO "user_role_enums"("role") VALUES ("technician");
INSERT INTO "user_role_enums"("role") VALUES ("admin");


DROP TABLE IF EXISTS "setting_types";
CREATE TABLE "setting_types" (
  "setting_name" varchar(50) NOT NULL,
  "min_value" float NOT NULL,
  "max_value" float NOT NULL,
  "default_value" float NOT NULL,
  "role" NOT NULL REFERENCES "user_role_enums"("role"),
  "group" int(10) DEFAULT NULL,
  "type" varchar(50) NOT NULL DEFAULT 'int',
  PRIMARY KEY ("setting_name")
); 

DROP TABLE IF EXISTS "settings";
CREATE TABLE "settings" (
	"installation" VARCHAR(128) NOT NULL REFERENCES "installation"("serial_number"),
	"setting_name" VARCHAR(50) NOT NULL REFERENCES "setting_types"("setting_name"),
	"value" FLOAT NOT NULL,
	PRIMARY KEY ("installation", "setting_name")
); 


DROP TABLE IF EXISTS "sync_queue";
CREATE TABLE "sync_queue" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "installation" varchar(100) NOT NULL,
  "table" varchar(100) NOT NULL,
  "method" varchar(100) NOT NULL,
  "data" TEXT NOT NULL,
  "prev" TEXT DEFAULT NULL,
  "last_sync_attempt" datetime DEFAULT NULL
); 


PRAGMA foreign_keys = ON;
