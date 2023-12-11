BEGIN;
--
-- Add field expire_date to userstory
--
ALTER TABLE "story" ADD COLUMN "expire_date" timestamp with time zone NULL;
COMMIT;
