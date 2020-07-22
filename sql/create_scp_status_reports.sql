--for postgres
CREATE TABLE "scp_status_reports" (
	"id" INTEGER NOT NULL DEFAULT 'nextval(''status_reports_id_seq1''::regclass)',
	"report_date" DATE NULL DEFAULT NULL,
	"trello_board_id" VARCHAR(20) NULL DEFAULT NULL,
	"trello_card_id" VARCHAR(20) NULL DEFAULT NULL,
	"trello_card_name" VARCHAR(200) NULL DEFAULT NULL,
	"tmetric_hours" REAL(24) NULL DEFAULT NULL,
	"budget" REAL(24) NULL DEFAULT NULL
)
;
COMMENT ON COLUMN "status_reports"."id" IS '';
COMMENT ON COLUMN "status_reports"."report_date" IS '';
COMMENT ON COLUMN "status_reports"."trello_board_id" IS '';
COMMENT ON COLUMN "status_reports"."trello_card_id" IS '';
COMMENT ON COLUMN "status_reports"."trello_card_name" IS '';
COMMENT ON COLUMN "status_reports"."tmetric_hours" IS '';
COMMENT ON COLUMN "status_reports"."budget" IS '';
