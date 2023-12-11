BEGIN;
--
-- Create model Profile
--
CREATE TABLE "profile" ("pkid" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "id" uuid NOT NULL UNIQUE, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "avatar" varchar(2000) NOT NULL, "gender" varchar(20) NOT NULL, "country" varchar(2) NOT NULL, "city" varchar(200) NOT NULL, "_nickname" varchar(100) NULL UNIQUE, "user_id" bigint NOT NULL UNIQUE);
ALTER TABLE "profile" ADD CONSTRAINT "profile_user_id_2aeb6f6b_fk_accounts_myuser_pkid" FOREIGN KEY ("user_id") REFERENCES "accounts_myuser" ("pkid") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "profile__nickname_b2c733ee_like" ON "profile" ("_nickname" varchar_pattern_ops);
COMMIT;