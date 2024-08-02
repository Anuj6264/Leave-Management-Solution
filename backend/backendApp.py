# Import necessary dependencies:
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import CORS
import holidays

app = Flask(__name__)
CORS(app)

# Configuration:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6264@localhost:5432/leave_management_system'
app.config['JWT_SECRET_KEY'] = 'bd65600d-8669-4903-8a14-af88203add65'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

migrate.init_app(app, db)


# Models:
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)


class Leave(db.Model):
    __tablename__ = 'leaves'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    leave_count = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')
    reason = db.Column(db.String(255), nullable=True)


# created database tables here:
with app.app_context():
    db.create_all()


# different Routes:

# For registering a employee/user or manager:
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    role = data.get('role')

    if not username or not password or not firstName or not lastName or not role:
        response = jsonify({'message': 'Username and password are required.'}), 400
        return response

    user = User(username=username, password=password, firstName=firstName, lastName=lastName, role=role)
    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User registered successfully.'}), 201
    return response


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
    return jsonify({'access_token': access_token, 'user': {'role': user.role}}), 200


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
        return jsonify({'message': 'Start date and End date are required.'}), 400

    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

    if to_date < from_date:
        return jsonify({'message': 'Invalid date range.'}), 400

    total_days = (to_date - from_date).days + 1

    if total_days > 15:
        return jsonify({'message': 'Date range should not exceed 15 days.'}), 400

    weekends = [5, 6]
    weekdays = [from_date + timedelta(days=i) for i in range(total_days) if
                (from_date + timedelta(days=i)).weekday() not in weekends]

    public_holidays = holidays.CountryHoliday('IN', years=from_date.year)
    leave_days = [day for day in weekdays if day not in public_holidays]
    leave_count = len(leave_days)

    user = User.query.get(user_id)

    leave = Leave(user_id=user_id, from_date=from_date, to_date=to_date, leave_count=leave_count,
                  firstName=user.firstName, lastName=user.lastName)
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
            'reason': leave.reason,
            'firstName': leave.firstName,
            'lastName': leave.lastName
        }
        leave_list.append(leave_data)

    return jsonify(leave_list), 200


@app.route('/api/leaves/all', methods=['GET'])
@jwt_required()
def get_all_leaves():
    user_id = get_jwt_identity()
    leaves = Leave.query.filter(Leave.user_id != user_id).all()
    leave_list = []

    for leave in leaves:
        leave_data = {
            'id': leave.id,
            'from_date': leave.from_date,
            'to_date': leave.to_date,
            'leave_count': leave.leave_count,
            'status': leave.status,
            'reason': leave.reason,
            'firstName': leave.firstName,
            'lastName': leave.lastName
        }
        leave_list.append(leave_data)

    return jsonify(leave_list), 200


# For accepting or rejecting a leave by manager:
@app.route('/api/leaves/<int:leave_id>', methods=['PATCH'])
@jwt_required()
def update_leave(leave_id):
    user_id = get_jwt_identity()
    data = request.json
    status = data.get('status')
    reason = data.get('reason')

    if not status or status not in ['accepted', 'rejected']:
        return jsonify({'message': 'Invalid status value. Must be "accepted" or "rejected".'}), 400

    leave = Leave.query.filter_by(id=leave_id).first()

    if not leave:
        return jsonify({'message': 'Leave not found.'}), 404

    leave.status = status
    leave.reason = reason
    db.session.commit()

    return jsonify({'message': 'Leave updated successfully.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
