from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE


class Request:
    def __init__(self, data_dict):
        self.id = data_dict['id']
        self.custumer_id = data_dict['custumer_id']
        self.chef_id=data_dict['chef_id']
        self.description = data_dict['description']
        self.status = data_dict['status']
        self.created_at = data_dict['created_at']
        self.updated_at = data_dict['updated_at']

    @classmethod
    def create(cls, data_dict):
        query = """
        INSERT INTO requests (custumer_id, description, status,chef_id)
        VALUES (%(custumer_id)s, %(description)s, %(status)s, %(chef_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data_dict)
    
    @classmethod
    def get_by_id(cls, data_dict):
        query = """SELECT * FROM requests WHERE id=%(id)s;"""
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        return cls(result[0])

    @classmethod
    def get_by_userid(cls, data_dict):
        query = """SELECT * FROM requests WHERE custumer_id=%(custumer_id)s;"""
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        recp = []
        for row in result:
            recp.append(cls(row))
        return recp
    
    @classmethod
    def get_by_chefid(cls, data_dict):
        query = """SELECT * FROM requests WHERE chef_id=%(chef_id)s;"""
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        recp = []
        for row in result:
            recp.append(cls(row))
        return recp

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM requests;"""
        result = connectToMySQL(DATABASE).query_db(query)
        return [cls(data) for data in result]
    
    @classmethod
    def edit(cls, data):
        query = """
        UPDATE requests SET status = %(status)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    

    # Add any additional class methods or static methods as needed for your application