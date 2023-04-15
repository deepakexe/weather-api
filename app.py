from flask import Flask, request, jsonify
import mysql.connector
import os

# Create MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Deep@011",
  database="weather"
)

# Create Flask app
app = Flask(__name__)

# Endpoint to get all records
@app.route('/records', methods=['GET'])
def get_records():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM record")
    records = cursor.fetchall()
    cursor.close()
    return jsonify(records)

# Endpoint to find a record by its city
@app.route('/records/<city>', methods=['GET'])
def get_record(city):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM record WHERE city = %s", (city,))
    record = cursor.fetchone()
    cursor.close()
    if record:
        return jsonify(record)
    else:
        return jsonify({"error": "User not found"}), 404

# Endpoint to create a new record
@app.route('/records', methods=['POST'])
def create_record():
    data = request.get_json()
    city =  data.get('city')
    temp = data.get('temperature')
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO records (city, temperature) VALUES (%s, %s)", (city, temp))
    mydb.commit()
    cursor.close()
    return jsonify({"message": "record created successfully"}), 201

# Endpoint to update an existing record by city
@app.route('/records/<city>', methods=['PUT'])
def update_record(city):
    data = request.get_json()
    temp = data.get('temperature')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM record WHERE city = %s", (city,))
    record = cursor.fetchone()
    cursor.close()
    if record:
        cursor.execute("UPDATE record SET temperature = %s WHERE city = %s", (temp, city))
        mydb.commit()
        cursor.close()
        return jsonify({"message": "record updated successfully"}) 
    else:
        return jsonify({"message": "record doesn't exist,Create a new one."}), 404

# Endpoint to delete a record by city
@app.route('/records/<city>', methods=['DELETE'])
def delete_record(city):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM record WHERE city = %s", (city,))
    record = cursor.fetchone()
    cursor.close()
    if record:
        cursor.execute("DELETE FROM record WHERE city = %s", (city,))
        mydb.commit()
        cursor.close()
        return jsonify({"message": "record deleted successfully"})
    else:
        return jsonify({"message": "record doesn't exist"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

