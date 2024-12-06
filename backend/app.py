from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mdt_inventory.db'
CORS(app)
db = SQLAlchemy(app)

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

class MDT(db.Model):
    mdt_id = db.Column(db.String, primary_key=True)
    pc_serial = db.Column(db.String, nullable=False)
    pc_model = db.Column(db.String, nullable=False)
    aircard_ip = db.Column(db.String, nullable=False)
    pc_name = db.Column(db.String, nullable=False)
    term_id = db.Column(db.String, nullable=False)

class AuditLog(db.Model):
    log_id = db.Column(db.String, primary_key=True)
    action_performed = db.Column(db.String, nullable=False)
    performed_by = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

# API Routes
@app.route('/load-mdt-data', methods=['GET'])
def load_mdt_data():
    # Change the following path to the correct location of MDT INVENTORY.xlsx on your machine
    file_path = 'C:\\Users\\KC\\Documents\\data-management-final-project-main\\data\\MDT INVENTORY.xlsx'
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
def update_returned_tab():
    file_path = 'C:\\Users\\KC\\Documents\\data-management-final-project-main\\data\\MDT INVENTORY.xlsx'
    try:
        updated_data = request.json
        df = pd.DataFrame(updated_data)
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='Returned', index=False)
        return jsonify({'message': 'Data successfully updated in the Returned tab.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-report', methods=['GET'])
def generate_report():
    file_path = 'C:\\Users\\KC\\Documents\\data-management-final-project-main\\data\\MDT INVENTORY.xlsx'
    try:
        df = pd.read_excel(file_path, sheet_name='Returned', engine='openpyxl')
        csv_path = 'C:\\Users\\KC\\Documents\\data-management-final-project-main\\data\\Returned_Report.csv'
        df.to_csv(csv_path, index=False)
        return jsonify({'message': 'Report generated successfully!', 'path': csv_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
