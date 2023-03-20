from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']

    @classmethod
    def validate(cls, data):
        is_valid = True
        # print(data)
        if len(data['name']) < 3:
            flash('Name must be at least 3 characters', 'name')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must be at least 3 characters', 'description')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Instructions must be at least 3 characters', 'instructions')
            is_valid = False
        if len(data['date']) < 1:
            flash('Date is required', 'date')
            is_valid = False
        if not 'under_30' in data:
            flash('Required field', 'under_30')
            is_valid = False
        return is_valid

    @classmethod
    def create_recipe(cls, data):
        query = """ INSERT INTO recipes (name, description, instructions, date, under_30, user_id) 
                    VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_30)s, %(user_id)s);"""
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_all_with_user(cls):
        query = """ SELECT * FROM recipes
                    JOIN users
                    ON users.id = recipes.user_id;"""
        results = connectToMySQL(DATABASE).query_db( query ) #grab list of all recipes
        # print(f"RESULTS >>>>>>{results}")
        recipes = [] #make empty list
        for recipe in results: #loop through results
            user_data = {
                'id': recipe['user_id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password']
            }
            Recipe.user = user.User(user_data)
            # print(Recipe.user.first_name)
            recipes.append(cls(recipe)) #push INSTANCE of each result into empty list
        # print(recipes)
        return recipes #return filled list of instances
    
    @classmethod
    def get_one(cls, recipe_id):
        data = {
            'id': recipe_id
        }
        query = """ SELECT * FROM recipes
                    JOIN users
                    ON users.id = recipes.user_id
                    WHERE recipes.id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db( query, data )
        for recipe in results: #loop through results
            user_data = {
                'id': recipe['user_id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password']
            }
            Recipe.user = user.User(user_data)
        this_recipe = cls(results[0])
        return this_recipe
    
    @classmethod
    def update(cls, data):
        query = """ UPDATE recipes
                    SET name = %()s, description = %()s, instructions = %()s, date = %()s, under_30 = %()s
                    WHERE recipe.id = %()s;"""
        return connectToMySQL(DATABASE).query_db( query, data )
    
    @classmethod
    def delete(cls, recipe_id):
        data = {
            'id' : recipe_id
        }
        query = """DELETE FROM recipes WHERE id = %(id)s; """
        return connectToMySQL(DATABASE).query_db( query, data )