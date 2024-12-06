from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mdt_inventory.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with a strong secret key
CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Models
class Location(db.Model):
    location_id = db.Column(db.String, primary_key=True)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.String, nullable=False)

class Department(db.Model):
    department_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location_id = db.Column(db.String, db.ForeignKey('location.location_id'))
    location = db.relationship('Location', backref='departments')

class User(db.Model):
    user_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    rank = db.Column(db.String)
    unit_number = db.Column(db.String)
    star_number = db.Column(db.String)
    department_id = db.Column(db.String, db.ForeignKey('department.department_id'))
    department = db.relationship('Department', backref='users')

class MDT(db.Model):
    mdt_id = db.Column(db.String, primary_key=True)
    pc_serial = db.Column(db.String, nullable=False)
    pc_model = db.Column(db.String, nullable=False)
    aircard_ip = db.Column(db.String, nullable=False)
    pc_name = db.Column(db.String, nullable=False)
    term_id = db.Column(db.String, nullable=False)

class Assignment(db.Model):
    assignment_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'))
    mdt_id = db.Column(db.String, db.ForeignKey('mdt.mdt_id'))
    date_assigned = db.Column(db.Date, nullable=False)
    date_returned = db.Column(db.Date)
    status = db.Column(db.String, nullable=False)
    user = db.relationship('User', backref='assignments')
    mdt = db.relationship('MDT', backref='assignments')

class AuditLog(db.Model):
    log_id = db.Column(db.String, primary_key=True)
    action_performed = db.Column(db.String, nullable=False)
    performed_by = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

# Authentication and Role-Based Access Control
users_roles = {
    "admin": "Admin",
    "user": "User"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    role = users_roles.get(username)  # Simulate a role-based system
    if role:
        token = create_access_token(identity={'username': username, 'role': role})
        return jsonify({'access_token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity['role'] != required_role:
                abort(403, description="Access forbidden")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# API Routes
@app.route('/add-user', methods=['POST'])
@role_required('Admin')
def add_user():
    try:
        data = request.json
        new_user = User(
            user_id=data['user_id'],
            name=data['name'],
            rank=data.get('rank'),
            unit_number=data.get('unit_number'),
            star_number=data.get('star_number'),
            department_id=data['department_id']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load-mdt-data', methods=['GET'])
@jwt_required()
def load_mdt_data():
    # Change the following path to the correct location of MDT INVENTORY.xlsx on your machine
    file_path = 'C:\\Users\\KC\\Desktop\\Data Management - final project\\data\\MDT INVENTORY.xlsx'
    # Example: file_path = 'C:\\path_to_your_folder\\MDT INVENTORY.xlsx'
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df.rename(columns={
            'NAME': 'name',
            'STAR #': 'star_number',
            'UNIT': 'unit',
            'PC SERIAL': 'pc_serial',
            'PC MODEL#': 'pc_model',
            'AIRCARD IP': 'aircard_ip',
            'PC NAME': 'pc_name',
            'TERM ID': 'term_id'
        }, inplace=True)
        data = df.to_dict(orient='records')
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found. Ensure the file path is correct.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update-returned-tab', methods=['POST'])
@jwt_required()
def update_returned_tab():
    # Change the following path to the correct location of MDT INVENTORY.xlsx on your machine
    file_path = 'C:\\Users\\KC\\Desktop\\Data Management - final project\\data\\MDT INVENTORY.xlsx'
    # Example: file_path = 'C:\\path_to_your_folder\\MDT INVENTORY.xlsx'
    try:
        updated_data = request.json
        df = pd.DataFrame(updated_data)
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='Returned', index=False)
        return jsonify({'message': 'Data successfully updated in the Returned tab.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-report', methods=['GET'])
@jwt_required()
def generate_report():
    # Change the following path to the correct location of MDT INVENTORY.xlsx on your machine
    file_path = 'C:\\Users\\KC\\Desktop\\Data Management - final project\\data\\MDT INVENTORY.xlsx'
    # Example: file_path = 'C:\\path_to_your_folder\\MDT INVENTORY.xlsx'
    try:
        df = pd.read_excel(file_path, sheet_name='Returned', engine='openpyxl')
        # Change the following path to where you want the report to be saved
        csv_path = 'C:\\Users\\KC\\Desktop\\Data Management - final project\\data\\Returned_Report.csv'
        # Example: csv_path = 'C:\\path_to_your_folder\\Returned_Report.csv'
        df.to_csv(csv_path, index=False)
        return jsonify({'message': 'Report generated successfully!', 'path': csv_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
