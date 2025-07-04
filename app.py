from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'dbmsproject'
}

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)  # DictCursor for dictionary results

    def select(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return None

    def update(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount  # Return the number of affected rows
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            self.connection.rollback()
            return None

    def insert(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.lastrowid  # Return the last inserted ID
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            self.connection.rollback()
            return None

    def close(self):
        self.cursor.close()
        self.connection.close()

# Route to get all hospitals
@app.route('/get_hospitals', methods=['GET'])
def get_hospitals():
    db = Database()
    query = "SELECT * FROM hospitals_final"
    result = db.select(query)
    db.close()
    return jsonify(result)

# Route to get a specific hospital by ID
# @app.route('/get_hospital/<int:id>', methods=['GET'])
# def get_hospital(id):
#     db = Database()
#     query = "SELECT * FROM hospitals_final WHERE `Master ID` = %s"
#     params = (id,)
#     result = db.select(query, params)
#     db.close()
#     return jsonify(result[0]) if result else jsonify({'error': 'Hospital not found'}), 404

# Route to update a hospital's locality
@app.route('/update_hospital', methods=['POST'])
def update_hospital():
    data = request.get_json()
    hospital_name = data['hospital_name']
    new_locality = data['new_locality']
    
    db = Database()
    query = "UPDATE hospitals_final SET Locality = %s WHERE `Hospital Name` = %s"
    params = (new_locality, hospital_name)
    rows_affected = db.update(query, params)
    db.close()
    return jsonify({'rows_affected': rows_affected})

# Route to get all hospices
@app.route('/get_hospices', methods=['GET'])
def get_hospices():
    try:
        db = Database()
        query = "SELECT * FROM Hospice_Care_CentresFinal"
        result = db.select(query)
        db.close()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to fetch data'}), 500

# Route to get a specific hospice by ID
@app.route('/get_hospice/<int:id>', methods=['GET'])
def get_hospice(id):
    db = Database()
    query = "SELECT * FROM Hospice_Care_CentresFinal WHERE `Master ID` = %s"
    params = (id,)
    result = db.select(query, params)
    db.close()
    return jsonify(result[0]) if result else jsonify({'error': 'Hospice not found'}), 404

# Route to update a hospice's locality
@app.route('/update_hospice', methods=['POST'])
def update_hospice():
    data = request.get_json()
    hospice_name = data['hospice_name']
    new_locality = data['new_locality']
    
    db = Database()
    query = "UPDATE Hospice_Care_CentresFinal SET Locality = %s WHERE `Hospice Care Centre Name` = %s"
    params = (new_locality, hospice_name)
    rows_affected = db.update(query, params)
    db.close()
    return jsonify({'rows_affected': rows_affected})

# Route to get all nursing homes
@app.route('/get_nursing_homes', methods=['GET'])
def get_nursing_homes():
    try:
        db = Database()
        query = "SELECT * FROM Nursing_Care_Centers_Final"
        result = db.select(query)
        db.close()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to fetch data'}), 500

# Route to get all companions
@app.route('/get_companions', methods=['GET'])
def get_companions():
    try:
        db = Database()
        query = "SELECT * FROM Elderly_Care_Services_Final"
        result = db.select(query)
        db.close()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to fetch data'}), 500

# Route to get all pharmacies
@app.route('/get_pharmacies', methods=['GET'])
def get_pharmacies():
    try:
        db = Database()
        query = "SELECT * FROM Pharmacies_Final"
        result = db.select(query)
        db.close()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to fetch data'}), 500

# Route to get all volunteers
@app.route('/get_volunteers', methods=['GET'])
def get_volunteers():
    db = Database()
    query = "SELECT * FROM volunteers"
    result = db.select(query)
    db.close()
    return jsonify(result)

# Route to add a new volunteer
@app.route('/add_volunteer', methods=['POST'])
def add_volunteer():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    availability = data.get('availability')
    service = data.get('service')
    
    if not all([name, email, phone, availability, service]):
        return jsonify({'error': 'All fields are required'}), 400
    
    db = Database()
    query = "INSERT INTO volunteers (name, email, phone, availability, service) VALUES (%s, %s, %s, %s, %s)"
    params = (name, email, phone, availability, service)
    volunteer_id = db.insert(query, params)  # Use the `insert` method for the insert operation
    db.close()
    if volunteer_id:
        return jsonify({'id': volunteer_id}), 201
    else:
        return jsonify({'error': 'Failed to add volunteer'}), 500

# Route to test POST requests
@app.route('/test_post', methods=['POST'])
def test_post():
    return jsonify({'message': 'POST request successful!'})

if __name__ == '__main__':
    app.run(debug=True)
