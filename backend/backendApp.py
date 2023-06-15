#I have imported necessary dependencies here:
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import holidays

app = Flask(__name__)

# Configuration:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6264@localhost:5432/leave_management_system'
app.config['JWT_SECRET_KEY'] = 'bd65600d-8669-4903-8a14-af88203add65'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Models:
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Leave(db.Model):
    __tablename__ = 'leaves'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    leave_count = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')
    reason = db.Column(db.String(255))


# I have Created database tables here:
with app.app_context():
    db.create_all()

# Different Routes:

# For registering a employee/user or manager:
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201

# For aunthenticating and login a employee/user or manager:
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({'message': 'Invalid username or password.'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

# For applying a leave for employee/user or manager with necessary checks of: 
# 1. weekends 
# 2. public holidays 
# 3. date range selectable can be 15 days at max
@app.route('/api/leaves', methods=['POST'])
@jwt_required()
def create_leave():
    user_id = get_jwt_identity()
    data = request.json
    from_date_str = data.get('from_date')
    to_date_str = data.get('to_date')

    if not from_date_str or not to_date_str:
        return jsonify({'message': 'From date and to date are required.'}), 400

    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

    if to_date < from_date:
        return jsonify({'message': 'Invalid date range.'}), 400

    total_days = (to_date - from_date).days + 1

    if total_days > 15:
        return jsonify({'message': 'Date range should not exceed 15 days.'}), 400

    weekends = [5, 6] 
    weekdays = [from_date + timedelta(days=i) for i in range(total_days) if (from_date + timedelta(days=i)).weekday() not in weekends]
 
    public_holidays = holidays.CountryHoliday('IN', years=from_date.year)
    leave_days = [day for day in weekdays if day not in public_holidays]
    leave_count = leave_days.count

    leave = Leave(user_id=user_id, from_date=from_date, to_date=to_date, leave_count=leave_count)
    db.session.add(leave)
    db.session.commit()

    return jsonify({'message': 'Leave created successfully.'}), 201

# For fetching the all the leaves corresponding to a employee/user:
@app.route('/api/leaves', methods=['GET'])
@jwt_required()
def get_leaves():
    user_id = get_jwt_identity()
    leaves = Leave.query.filter_by(user_id=user_id).all()
    leave_list = []

    for leave in leaves:
        leave_data = {
            'id': leave.id,
            'from_date': leave.from_date,
            'to_date': leave.to_date,
            'leave_count': leave.leave_count,
            'status': leave.status,
            'reason': leave.reason
        }
        leave_list.append(leave_data)

    return jsonify(leave_list), 200

if __name__ == '__main__':
    app.run()