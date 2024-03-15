from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ayush#9310",
    database="user"
)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ayush#9310',
    'database': 'user'
}
# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Example query: Select all rows from a table


@app.route('/data', methods=['GET'])
def get_books():
        cursor.execute("SELECT * FROM registration")
   
        # Convert result to a list of dictionaries
        cities = [{'id': row[0], 'name': row[1], 'country': row[2]} for row in cursor]
        return jsonify(cities)



# Function to execute SQL query
def execute_query(query, values):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # Execute the SQL query
        cursor.execute(query, values)
        
        # Commit the transaction
        connection.commit()
        
        # Close cursor and connection
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        return str(e)

# Define a route for the POST API endpoint
@app.route('/registration', methods=['POST'])
def register():
    # Get JSON data from the request
    json_data = request.json
    
    # Check if JSON data is provided
    if json_data:
        # Extract data from JSON
        id = json_data.get('id')
        fname = json_data.get('fname')
        lname = json_data.get('lname')
        age = json_data.get('age')
        
        # Check if all required fields are provided
        if id is None or fname is None or lname is None or age is None:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Define SQL query
        query = "INSERT INTO registration (id, fname, lname, age) VALUES (%s, %s, %s, %s)"
        
        # Define values to insert
        values = (id, fname, lname, age)
        
        # Execute the query
        success = execute_query(query, values)
        
        if success:
            return jsonify({'message': 'Registration successful'}), 201
        else:
            return jsonify({'error': 'Failed to register'}), 500
    else:
        return jsonify({'error': 'No JSON data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)


