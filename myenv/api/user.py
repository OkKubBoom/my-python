from flask import Blueprint, jsonify, request
from bson import ObjectId  # เพิ่มการ import ObjectId
from model.userModel import UserModel
from model.response_model import ResponseModel  # Import ResponseModel ที่ประกาศไว้

# สร้าง Blueprint สำหรับแยก API ของ User
user_bp = Blueprint('user_bp', __name__, url_prefix='/api')
user_model = UserModel()

# สร้างผู้ใช้ใหม่
@user_bp.route('/users', methods=['POST'])
def create_user():
    # รับข้อมูลจาก request body
    data = request.json
    email = data.get('user_email')
    password = data.get('user_password')

    # ตรวจสอบว่ามีข้อมูลที่จำเป็นครบถ้วน
    if not email or not password:
        response = ResponseModel(status='501', success=False, message='Missing email or password')
        return jsonify(response.to_dict()), 501

    # สร้างผู้ใช้ใหม่
    user_id = user_model.create_user(email, password)
    return jsonify({'status': 'User created', 'id': user_id}), 201

# ดึงข้อมูลผู้ใช้ทั้งหมด
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = user_model.get_all_users()
    return jsonify(users), 200

# อัพเดตข้อมูลผู้ใช้
@user_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    # รับข้อมูลจาก request body
    data = request.json
    email = data.get('user_email')
    password = data.get('user_password')

    # อัพเดตผู้ใช้ตามข้อมูลที่ส่งมา
    updated_count = user_model.update_user(id, email=email, password=password)

    if updated_count:
        return jsonify({'status': 'User updated'}), 200
    return jsonify({'status': 'User not found'}), 404

# ลบผู้ใช้
@user_bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    deleted_count = user_model.delete_user(id)

    if deleted_count:
        return jsonify({'status': 'User deleted'}), 200
    return jsonify({'status': 'User not found'}), 404

# ดึงข้อมูลผู้ใช้ตาม ID (GET /api/users/<id>)
@user_bp.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    # ตรวจสอบว่า ID ที่ได้รับมาถูกต้องหรือไม่
    if not ObjectId.is_valid(id):
        return jsonify({'status': 'error', 'message': 'Invalid user ID'}), 400

    user = user_model.get_user_by_id(id)

    if user:
        return jsonify(user), 200
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
