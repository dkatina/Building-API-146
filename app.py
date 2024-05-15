from flask import Flask, jsonify, request #importing the Flask class
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from db_connection import db_connection, Error

app = Flask(__name__)
ma = Marshmallow(app)

#Creating the Customer Table Schema, to define the structure of data
class CustomerSchema(ma.Schema):
    id = fields.Int(dump_only=True) #dump_only means we dont input data for this field
    customer_name = fields.String(required=True) #required means to be valid need a value
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("customer_name", "email", "phone")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@app.route('/') #Defining a simple home route, which recieves requests
def home():
    return "Welcome to the Flask Party" #returning a response 


#Reading all Customer data via GET request
@app.route('/customers', methods=['GET'])
def get_customers():
    conn = db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)

            #writing my query to get all users
            query = "SELECT * FROM Customer"

            cursor.execute(query)

            customers = cursor.fetchall()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return customers_schema.jsonify(customers)
            
#Creating a new customer with a POST request
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    conn = db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            #new_customer datails
            new_customer = (customer_data['customer_name'], customer_data['email'], customer_data['phone'])

            #query
            query = "INSERT INTO Customer (customer_name, email, phone) VALUES (%s, %s, %s)"

            #Execute query with new_customer data
            cursor.execute(query, new_customer)
            conn.commit()

            return jsonify({'Message': "New Customer Added Successfully!"}), 201
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database Connection failed"}), 500
    
@app.route('/customers/<int:id>', methods=['PUT']) #-- dynamic route, whos endpoint will change with different query parameters
def update_customer(id):

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM Customer WHERE id = %s"
            cursor.execute(check_query, (id,))
            customer = cursor.fetchone()
            if not customer:
                return jsonify({"Error": "Customer not found"}), 404

            #unpacking the updated customer info
            updated_customer = (customer_data['customer_name'], customer_data['email'], customer_data['phone'], id)

            #update query
            query = "UPDATE Customer SET customer_name = %s, email = %s, phone = %s WHERE id = %s"

            cursor.execute(query, updated_customer)
            conn.commit()

            return jsonify({"Message": f"Successfully updated User {id}"}), 200
        
        except Error as e:
            return jsonify({"Error": "Internal Server Error"}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database Connection Failed!"}), 500
    
#Deleting customer with a DELETE request
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):

    conn = db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM Customer WHERE id = %s"
            cursor.execute(check_query, (id,))
            customer = cursor.fetchone()
            if not customer:
                return jsonify({"Error": "Customer not found"}), 404
            
            query = "DELETE FROM Customer WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()

            #return a response
            return jsonify({"Message": f"Customer {id} was Destroyed!"})
        except Error as e:
            return jsonify({"Error": "Internal Server Error"}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database Connection Failed!"}), 500
    






if __name__ == '__main__': #idom to verify we're running this selected file, and not allow running if imported 
    app.run(debug=True)