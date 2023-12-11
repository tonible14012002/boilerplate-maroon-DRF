CREATE KEYSPACE IF NOT EXISTS db
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS db.story_inbox (
    user_id TEXT,
    story_id TEXT,
    owner_id TEXT,
    PRIMARY KEY ((user_id, story_id, owner_id))
) WITH comment = 'Table with user_id and story_id and owner_id';