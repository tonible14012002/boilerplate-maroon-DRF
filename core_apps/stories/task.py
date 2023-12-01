from django.contrib.auth import get_user_model
from core_apps.common.utils import db as common_db_utils
import celery


User = get_user_model()


def get_insert_story_inbox_cql(user_pkids, story_pkid, ttl):
    row_insert_query = '''
        INSERT INTO db.story_inbox (user_id, story_id) VALUES ('{user_id}', '{story_id}') USING TTL {ttl};
    '''
    insert_story_inbox_cql = f'''
        BEGIN BATCH
            {" ".join(list(map(
                lambda user_pkid: row_insert_query.format(user_id=user_pkid, story_id=story_pkid, ttl=ttl),
                user_pkids
            )))}
        APPLY BATCH;
      '''
    return insert_story_inbox_cql


@celery.shared_task()
def boardcast_story_inbox(owner_pkid, story_pkid, ttl):
    owner = User.objects.get(pkid=owner_pkid)
    follower_ids = owner.followers.values_list('pkid', flat=True)

    connection = common_db_utils.cassandra_connection()
    with connection.cursor() as cursor:
        query = get_insert_story_inbox_cql(follower_ids, story_pkid, ttl)
        print(query, flush=True)
        try:
            cursor.execute(
                query
            )
            connection.commit()
        except Exception as e:
            print("Error:", e, flush=True)
            connection.rollback()
