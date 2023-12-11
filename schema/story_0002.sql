BEGIN;
--
-- Alter field media_url on userstory
--
ALTER TABLE "story" ALTER COLUMN "media_url" TYPE varchar(2000);
COMMIT;
