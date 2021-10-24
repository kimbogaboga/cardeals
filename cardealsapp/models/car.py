from cardealsapp.config.mysqlconnection import connectToMySQL
from flask import flash
from cardealsapp.models import user

class Car:
    db_name = 'cardeals'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.price = db_data['price']
        self.model = db_data['model']
        self.make = db_data['make']
        self.year = db_data['year']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.seller_id = None
        self.buyer_id = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO cars (price, model, make, year, description, created_at, updated_at, seller_id, buyer_id) VALUES (%(price)s,%(model)s,%(make)s, %(year)s, %(description)s, NOW(), NOW(),%(seller_id)s, NULL);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_cars = []
        for row in results:
            all_cars.append( cls(row) )
        return all_cars

    @classmethod
    def get_seller_cars_complete(cls, data):
        query = "SELECT * FROM cars JOIN users ON cars.seller_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        new_cars = []
        if len(results) ==0:
            return new_cars
        else:
            for car in results:
                user_data ={
                    "id": car['users.id'],
                    "first_name": car['first_name'],
                    "last_name": car['last_name'],
                    "email": car['email'],
                    "password": car['password'],
                    "created_at": car['users.created_at'],
                    "updated_at": car['users.updated_at']
                }
                userhere = user.User(user_data)
                new_car = cls(car)
                new_car.user_id = userhere
                new_cars.append(new_car)
            return new_cars

    @classmethod
    def get_buyer_cars_complete(cls, data):
        query = "SELECT * FROM cars JOIN users ON cars.buyer_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        new_cars = []
        if len(results) ==0:
            return new_cars
        else:
            for car in results:
                user_data ={
                    "id": car['users.id'],
                    "first_name": car['first_name'],
                    "last_name": car['last_name'],
                    "email": car['email'],
                    "password": car['password'],
                    "created_at": car['users.created_at'],
                    "updated_at": car['users.updated_at']
                }
                userhere = user.User(user_data)
                new_car = cls(car)
                new_car.buyer_id = userhere
                new_cars.append(new_car)
            return new_cars

    @classmethod
    def get_all_cars_to_sell(cls):
        query = "SELECT * FROM cars JOIN users ON cars.seller_id = users.id"
        results = connectToMySQL(cls.db_name).query_db(query)
        new_cars = []
        if len(results) ==0:
            return new_cars
        else:
            for car in results:
                user_data ={
                    "id": car['users.id'],
                    "first_name": car['first_name'],
                    "last_name": car['last_name'],
                    "email": car['email'],
                    "password": car['password'],
                    "created_at": car['users.created_at'],
                    "updated_at": car['users.updated_at']
                }
                userhere = user.User(user_data)
                #userhere is a user object 
                new_car = cls(car)
                # new car is a car object
                new_car.seller_id = userhere
                # I'm putting a user object into seller_id, which has other attributes
                
                new_cars.append(new_car)
            return new_cars

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_one_complete(cls,data):
        query = "SELECT * FROM cars JOIN users ON cars.seller_id = users.id WHERE cars.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        car = cls(results[0])
        user_data ={
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }
        userhere = user.User(user_data)
        car.seller_id = userhere
        return car

    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, make=%(make)s, year =%(year)s, description = %(description)s,created_at = NOW(),updated_at=NOW(), seller_id = %(seller_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def purchase(cls, data):
        query = "UPDATE cars SET buyer_id = %(buyer_id)s WHERE cars.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_car(data):
        is_valid = True
        if len(data['model']) < 1:
            is_valid = False
            flash("Must not be blank", "car")
        if len(data['make']) < 1:
            is_valid = False
            flash("Must not be blank", "car")
        if len(data['description']) < 1:
            is_valid = False
            flash("Must not be blank", "car")
        if int(data['year']) <=0:
            is_valid = False
            flash("Year must be greater than 0!")
        if int(data['price']) <=0:
            is_valid = False
            flash("Price must be greater than 0!")
        return is_valid