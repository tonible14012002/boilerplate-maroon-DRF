
from core_apps.common.utils import db as common_db_utils
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class StoryInbox():
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.connection = None

    @classmethod
    def __makes_send_query(cls, user_ids, story_id, sender_id, ttl):
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
    def __make_select_story_id_query(cls, user_id, owner_id):
        if owner_id:
            additional_condi = f"AND owner_id = '{owner_id}'"
        else:
            additional_condi = ''

        return f'''
         SELECT story_id FROM db.story_inbox
         WHERE user_id = '{user_id}'
         {additional_condi}
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
        return models.UserStory.from_ids(self.get_all_ids_from_sender(sender_id=sender_id))

    def get_all(self):
        return models.UserStory.from_ids(self.get_all_ids())

    def send_story(self, story_id, ttl):
        sender = User.objects.get(id=self.user_id)
        follower_ids = sender.followers.values_list('id', flat=True)
        query = StoryInbox.__makes_send_query(
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
