BEGIN;
--
-- Add field is_test to myuser
--
ALTER TABLE "accounts_myuser" ADD COLUMN "is_test" boolean DEFAULT false NOT NULL;
ALTER TABLE "accounts_myuser" ALTER COLUMN "is_test" DROP DEFAULT;
COMMIT;
