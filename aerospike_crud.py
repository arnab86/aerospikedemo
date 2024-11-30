from flask import Flask, request, jsonify
import hashlib
import json
from dbconfig import Config
from aerospike_connection import AerospikeDBConnection

app = Flask(__name__)
def gethashfromhotelname(hotel_name):
    return hashlib.sha1(hotel_name.encode('utf-8')).hexdigest()
def getDBconn():
    hostname = Config.NLB_URL
    namespace = Config.NAMESPACE
    set_name = Config.SET_NAME
    db = AerospikeDBConnection(hostname=hostname,namespace=namespace,set_name=set_name)
    db.connect()
    return db

@app.route('/api/hotel', methods=['POST'])
def create_hotel():
    data = request.get_json()
    if not data or 'hotel_name' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    hotel_name = data.get('hotel_name')
    key = gethashfromhotelname(hotel_name)
    db = getDBconn()   
    # Create the key for the hotel
    try:
        db.create_record(key,data)
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.disconnect()
        return jsonify({'message': 'Hotel data created successfully!'}), 201
        

@app.route('/api/hotel/<hotel_name>', methods=['GET'])
def get_hotel(hotel_name):
    hotel_hash = gethashfromhotelname(hotel_name)
    db = getDBconn()
    try:
        response = db.fetch_record(hotel_hash)
        record = json.dumps(response)
        print(record)
        if record is not 'null':
            return record, 200
        else:
            return jsonify({'error': 'Hotel not found'}), 404
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.disconnect()
        
@app.route('/api/hotel/<hotel_name>', methods=['PUT'])
def update_user(hotel_name):
    hotel_hash = gethashfromhotelname(hotel_name)
    db = getDBconn()
    try:
        data = request.get_json()
        hotel_name = data.get('hotel_name')
        if not data or 'hotel_name' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        record = db.fetch_record(hotel_hash)
        if not record:
            return jsonify({'error': 'Hotel not found'}), 404
        if 'hotel_name' in data != 'hotel_name' in record:
            return jsonify({'error': 'Looks like it is a new hotel'}), 404
        db.update_record(hotel_hash, data)
        return jsonify({'message': 'User updated successfully!'}), 200
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.disconnect() 

@app.route('/api/hotel/<hotel_name>', methods=['DELETE'])
def delete_hotel(hotel_name):
    hotel_hash = gethashfromhotelname(hotel_name)
    db = getDBconn()
    try:
        response = db.fetch_record(hotel_hash)
        if not response:
            return jsonify({'error': 'Hotel not found'}), 404
        else:
            db.delete_record(hotel_hash)
            return jsonify({'message': 'User deleted successfully!'}), 200
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.disconnect()

if __name__ == '__main__':
    app.run(debug=True)