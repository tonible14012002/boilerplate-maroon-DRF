
from core_apps.common.utils import db as common_db_utils
from core_apps.common.utils import models as common_model_utils
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class StoryInbox():
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.connection = None

    @classmethod
    def __make_send_stories_query(cls, user_id, story_ids, sender_id, ttls):
        row_insert_query = '''
            INSERT INTO db.story_inbox (user_id, story_id, owner_id)
            VALUES ('{user_id}', '{story_id}', '{owner_id}')
            USING TTL {ttl};
        '''
        insert_story_inbox_cql = f'''
            BEGIN BATCH
                {" ".join(list(map(
                    lambda story_id, index: row_insert_query.format(
                        user_id=user_id,
                        story_id=story_id,
                        owner_id=sender_id,
                        ttl=ttls[index]
                    ),
                    story_ids
                )))}
            APPLY BATCH
        '''
        return insert_story_inbox_cql

    @classmethod
    def __make_broadcast_story_query(cls, user_ids, story_id, sender_id, ttl):
        row_insert_query = '''
            INSERT INTO db.story_inbox (user_id, story_id, owner_id)
            VALUES ('{user_id}', '{story_id}', '{owner_id}')
            USING TTL {ttl};
        '''
        # add story inbox to self also
        insert_story_inbox_cql = f'''
            BEGIN BATCH
                {" ".join(list(map(
                    lambda user_id: row_insert_query.format(
                        user_id=user_id,
                        story_id=story_id,
                        owner_id=sender_id,
                        ttl=ttl
                    ),
                    user_ids
                )))}
                {row_insert_query.format(
                    user_id=sender_id,
                    story_id=story_id,
                    owner_id=sender_id,
                    ttl=ttl
                )}
            APPLY BATCH;
        '''
        return insert_story_inbox_cql

    @classmethod
    def __make_select_story_id_query(cls, user_id=None, owner_id=None):
        assert user_id or owner_id
        if owner_id:
            additional_condi = f"owner_id = '{owner_id}'"
        else:
            additional_condi = ''

        if user_id:
            condi1 = f"user_id = '{user_id}'"
        else:
            condi1 = ''

        return f'''
         SELECT story_id FROM db.story_inbox
         WHERE
         {condi1}
         { 'AND ' + additional_condi if additional_condi != '' else additional_condi}
         ALLOW FILTERING;
      '''

    def __make_connection(self):
        self.connection = common_db_utils.cassandra_connection()
        return self.connection

    def __close_connection(self):
        self.connection.close()

    def __cursor(self):
        return self.connection.cursor()

    def get_all_ids(self):
        story_ids = []
        try:
            self.__make_connection()
            query = StoryInbox.__make_select_story_id_query(self.user_id)
            print(query, flush=True)
            with self.__cursor() as cursor:
                story_ids = map(
                    lambda id_dic: id_dic['story_id'],
                    cursor.execute(
                        query
                    )
                )
            self.__close_connection()
        except Exception as e:
            print(e, flush=True)
            raise exceptions.NotFound()

        return story_ids

    def get_all_ids_from_sender(self, sender_id):
        story_ids = []
        try:
            self.__make_connection()
            query = StoryInbox.__make_select_story_id_query(self.user_id, sender_id)
            with self.__cursor() as cursor:
                story_ids = map(
                    lambda id_dic: id_dic['story_id'],
                    cursor.execute(
                        query
                    )
                )
            self.__close_connection()
        except Exception as e:
            print(e, flush=True)
            raise exceptions.NotFound()

        return story_ids

    def get_all_from_user(self, sender_id):
        UserStory = common_model_utils.get_user_story_model()
        return UserStory.from_ids(self.get_all_ids_from_sender(sender_id=sender_id))

    def get_all(self):
        UserStory = common_model_utils.get_user_story_model()
        return UserStory.from_ids(self.get_all_ids())

    def broadcast_story(self, story_id, ttl):
        sender = User.objects.get(id=self.user_id)
        follower_ids = sender.followers.values_list('id', flat=True)
        query = StoryInbox.__make_broadcast_story_query(
            user_ids=follower_ids,
            sender_id=sender.id,
            story_id=story_id,
            ttl=ttl)

        try:
            self.__make_connection()
            with self.__cursor() as cursor:
                cursor.execute(
                    query
                )
                self.connection.commit()
            self.__close_connection()
        except Exception as e:
            print("This is an Error after calling Cassandra:", e, flush=True)
            self.connection.rollback()

    def send_all_active_story_to_user(self, user_id):
        UserStory = StoryInbox.get_story_model()

        sender = User.objects.get(id=self.user_id)
        get_story_ids_query = self.__make_select_story_id_query(sender.id, sender.id)
        story_ids = []
        time_now = timezone.now()
        try:
            self.__make_connection()
            with self.__cursor() as cursor:
                story_ids = map(
                    lambda id_dic: id_dic['story_id'],
                    cursor.execute(
                        get_story_ids_query
                    )
                )
                stories = UserStory.from_ids(story_ids)
                ttls = [story.expired_data - time_now for story in stories]
                print(ttls)
                insert_query = self.__make_send_stories_query(
                    user_id=user_id,
                    story_ids=story_ids,
                    sender_id=sender.id,
                    ttls=ttls
                )
                cursor.execute(
                    insert_query
                )
                self.connection.commit()
            self.__close_connection()

        except Exception as e:
            print("Error", e, flush=True)
            self.connection.rollback()
