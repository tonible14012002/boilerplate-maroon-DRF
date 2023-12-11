BEGIN;
--
-- Remove field expired from userstory
--
ALTER TABLE "story" DROP COLUMN "expired" CASCADE;
--
-- Add field status to userstory
--
ALTER TABLE "story" ADD COLUMN "status" varchar(50) DEFAULT 'NEW' NOT NULL;
ALTER TABLE "story" ALTER COLUMN "status" DROP DEFAULT;
COMMIT;
