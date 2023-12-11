BEGIN;
--
-- Add field alt_text to userstory
--
ALTER TABLE "story" ADD COLUMN "alt_text" varchar(200) DEFAULT '' NOT NULL;
ALTER TABLE "story" ALTER COLUMN "alt_text" DROP DEFAULT;
--
-- Add field caption to userstory
--
ALTER TABLE "story" ADD COLUMN "caption" varchar(200) DEFAULT '' NOT NULL;
ALTER TABLE "story" ALTER COLUMN "caption" DROP DEFAULT;
--
-- Add field view_option to userstory
--
ALTER TABLE "story" ADD COLUMN "view_option" varchar DEFAULT 'EVERYONE' NOT NULL;
ALTER TABLE "story" ALTER COLUMN "view_option" DROP DEFAULT;
COMMIT;
