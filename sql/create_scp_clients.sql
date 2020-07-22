CREATE TABLE "scp_clients" (
	"id" SERIAL PRIMARY KEY,
	"name" TEXT NOT NULL,
	"logo_image" BYTEA NULL DEFAULT NULL
)
;
COMMENT ON COLUMN "scp_clients"."id" IS '';
COMMENT ON COLUMN "scp_clients"."name" IS '';
COMMENT ON COLUMN "scp_clients"."logo_image" IS '';
