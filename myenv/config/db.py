import logging
from pymongo import MongoClient
from pymongo.errors import ConfigurationError  # ใช้ ConfigurationError แทน

# ตั้งค่าการบันทึก log
logging.basicConfig(level=logging.INFO)

def get_db():
    try:
        # พยายามเชื่อมต่อกับ MongoDB
        client = MongoClient("mongodb+srv://panicha:250917@cluster0.lovw9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        
        # เลือกฐานข้อมูล
        db = client['test']

        # ทดสอบการเชื่อมต่อ
        client.admin.command('ping')

        # ถ้าเชื่อมต่อสำเร็จ
        logging.info("Successfully connected to MongoDB.")
        return db
    
    except ConfigurationError as e:  # ใช้ ConfigurationError
        # ถ้าเกิดข้อผิดพลาดในการเชื่อมต่อ
        logging.error(f"Failed to connect to MongoDB: {e}")
        return None
