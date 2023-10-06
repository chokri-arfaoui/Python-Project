from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE


class Response:
    def __init__(self, data_dict):
        self.request_id = data_dict['request_id']
        self.recipe_id = data_dict['recipe_id']

    @classmethod
    def create(cls, data_dict):
        query = """
        INSERT INTO responses (request_id, recipe_id)
        VALUES (%(request_id)s, %(recipe_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data_dict)