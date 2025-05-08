import logging
from bson import ObjectId
from config.db import get_db
from datetime import datetime

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# สร้างโมเดล User
class UserModel:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['users']

    # ฟังก์ชันเพิ่มผู้ใช้ใหม่
    def create_user(self, email, password):
        logging.info("Called function: create_user")  # ใส่ log เมื่อเรียกฟังก์ชัน
        data = {
            'user_email': email,
            'user_password': password,
            'updated_at': datetime.utcnow()  # ใช้เวลาปัจจุบันในรูปแบบ UTC
        }
        result = self.collection.insert_one(data)
        logging.info(f"User created with id: {str(result.inserted_id)}")  # ใส่ log เมื่อสร้างสำเร็จ
        return str(result.inserted_id)

    # ฟังก์ชันดึงผู้ใช้ทั้งหมด
    def get_all_users(self):
        logging.info("Called function: get_all_users")  # ใส่ log เมื่อเรียกฟังก์ชัน
        users = list(self.collection.find())
        for user in users:
            user['_id'] = str(user['_id'])  # แปลง ObjectId เป็น string เพื่อให้ JSON รองรับ
        logging.info(f"Retrieved {len(users)} users")  # ใส่ log แสดงจำนวนผู้ใช้ที่ดึงมา
        return users

    # ฟังก์ชันอัพเดตผู้ใช้ตาม ID
    def update_user(self, user_id, email=None, password=None):
        logging.info(f"Called function: update_user for user_id: {user_id}")  # ใส่ log เมื่อเรียกฟังก์ชัน
        update_data = {}
        if email:
            update_data['user_email'] = email
        if password:
            update_data['user_password'] = password
        update_data['updated_at'] = datetime.utcnow()  # อัพเดตเวลาปัจจุบัน

        result = self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        logging.info(f"Updated {result.matched_count} user(s)")  # ใส่ log แสดงจำนวนผู้ใช้ที่อัพเดต
        return result.matched_count

    # ฟังก์ชันลบผู้ใช้ตาม ID
    def delete_user(self, user_id):
        logging.info(f"Called function: delete_user for user_id: {user_id}")  # ใส่ log เมื่อเรียกฟังก์ชัน
        result = self.collection.delete_one({'_id': ObjectId(user_id)})
        logging.info(f"Deleted {result.deleted_count} user(s)")  # ใส่ log แสดงจำนวนผู้ใช้ที่ถูกลบ
        return result.deleted_count

    # ฟังก์ชันดึงผู้ใช้ตาม ID
    def get_user_by_id(self, user_id):
        logging.info(f"Called function: get_user_by_id for user_id: {user_id}")  # ใส่ log เมื่อเรียกฟังก์ชัน
        if not ObjectId.is_valid(user_id):
            logging.error("Invalid ObjectId format")  # ใส่ log เมื่อ ObjectId ไม่ถูกต้อง
            return None
        user = self.collection.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])  # แปลง ObjectId เป็น string
            logging.info(f"User found: {user}")  # ใส่ log เมื่อพบผู้ใช้
        else:
            logging.info("User not found")  # ใส่ log เมื่อไม่พบผู้ใช้
        return user
