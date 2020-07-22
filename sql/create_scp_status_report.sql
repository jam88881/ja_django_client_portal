CREATE TABLE "scp_status_report" (
	"id" SERIAL PRIMARY KEY,
	"report_date" DATE NULL DEFAULT NULL,
	"trello_board_id" TEXT NULL DEFAULT NULL,
	"trello_card_id" TEXT NULL DEFAULT NULL,
	"trello_card_name" TEXT NULL DEFAULT NULL,
	"tmetric_hours" REAL NULL DEFAULT NULL,
	"budget" REAL NULL DEFAULT NULL
)
;
COMMENT ON COLUMN "scp_status_reports"."id" IS '';
COMMENT ON COLUMN "scp_status_reports"."report_date" IS '';
COMMENT ON COLUMN "scp_status_reports"."trello_board_id" IS '';
COMMENT ON COLUMN "scp_status_reports"."trello_card_id" IS '';
COMMENT ON COLUMN "scp_status_reports"."trello_card_name" IS '';
COMMENT ON COLUMN "scp_status_reports"."tmetric_hours" IS '';
COMMENT ON COLUMN "scp_status_reports"."budget" IS '';
