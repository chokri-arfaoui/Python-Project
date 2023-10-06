from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models import user


class Recipe:
    def __init__(self, data_dict):
        self.id = data_dict['id']
        self.chef_id = data_dict['chef_id']
        self.name = data_dict['name']
        self.description = data_dict['description']
        self.cook_time = data_dict['cook_time']
        self.created_at = data_dict['created_at']
        self.updated_at = data_dict['updated_at']
        self.food_type = user.User.get_by_id({'id':self.chef_id}).food_type
        self.chef_name = user.User.get_by_id({'id':self.chef_id}).last_name

    @classmethod
    def create(cls, data_dict):
        query = """
        INSERT INTO recipes (chef_id, name, description, cook_time)
        VALUES (%(chef_id)s, %(name)s, %(description)s, %(cook_time)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data_dict)

    @classmethod
    def get_by_id(cls, data_dict):
        query = """SELECT * FROM recipes WHERE id=%(id)s;"""
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM recipes;"""
        result = connectToMySQL(DATABASE).query_db(query)
        return [cls(data) for data in result]
    

    @classmethod
    def get_recipes_by_reqid(cls, data):
        query = """
        SELECT r.* FROM recipes r
        JOIN responses resp ON r.id = resp.recipe_id
        WHERE resp.request_id = %(request_id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        recp = []
        for row in result:
            recp.append(cls(row))
        return recp

    # Add any additional class methods or static methods as needed for your application