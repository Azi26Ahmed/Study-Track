import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import bcrypt
import logging
import datetime
import uuid
import os
from dotenv import load_dotenv
import secrets

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "study_track")

# Collection names
USERS_COLLECTION = os.getenv("USERS_COLLECTION", "users")
COURSES_COLLECTION = os.getenv("COURSES_COLLECTION", "courses")

# App settings
APP_NAME = "Study Track"
DEFAULT_THEME = "light"

# Password settings
PASSWORD_SALT_ROUNDS = 10 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5s timeout
    client.admin.command('ping')  # Test connection
    logger.info(f"Successfully connected to MongoDB at {MONGO_URI}")
except ConnectionFailure as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

# Access database and collections
db = client[DB_NAME]
users_collection = db[USERS_COLLECTION]
courses_collection = db[COURSES_COLLECTION]

# Ensure unique index on users' email
users_collection.create_index([("email", pymongo.ASCENDING)], unique=True)



# User operations

def create_user(email, password, name):
    """Create a new user with hashed password"""
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(PASSWORD_SALT_ROUNDS))
        user = {
            "email": email,
            "password": hashed_password,
            "name": name,
            "created_at": datetime.datetime.utcnow()
        }
        result = users_collection.insert_one(user)
        return str(result.inserted_id)
    except DuplicateKeyError:
        logger.warning(f"User with email {email} already exists")
        return None

def get_user_by_email(email):
    """Get user by email"""
    return users_collection.find_one({"email": email})

def verify_password(stored_password, provided_password):
    """Verify the password"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)



# Course operations

def add_course(user_id, course_data):
    """Add a course for a user"""
    try:
        course_data["user_id"] = user_id
        course_data["created_at"] = datetime.datetime.utcnow()
        course_data["updated_at"] = datetime.datetime.utcnow()
        
        if not course_data.get('url') or course_data.get('url') == "":
            unique_id = str(uuid.uuid4())
            course_data['url'] = f"manual_course_{unique_id}"
            course_data['url_generated'] = True
            
        result = courses_collection.insert_one(course_data)
        return str(result.inserted_id)
    except DuplicateKeyError:
        logger.warning(f"Course with URL {course_data.get('url')} already exists for user {user_id}")
        return None

def get_user_courses(user_id):
    """Get all courses for a user"""
    return list(courses_collection.find({"user_id": user_id}))

def get_course_by_id(course_id):
    """Get course by ID"""
    from bson.objectid import ObjectId
    return courses_collection.find_one({"_id": ObjectId(course_id)})

def update_course(course_id, update_data):
    """Update course data"""
    from bson.objectid import ObjectId
    update_data["updated_at"] = datetime.datetime.utcnow()
    return courses_collection.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": update_data}
    )

def delete_course(course_id):
    """Delete a course by ID"""
    from bson.objectid import ObjectId
    try:
        result = courses_collection.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count > 0:
            logger.info(f"Successfully deleted course with ID: {course_id}")
            return True
        else:
            logger.warning(f"No course found with ID: {course_id}")
            return False
    except Exception as e:
        logger.error(f"Error deleting course: {e}")
        return False

def update_video_status(course_id, section_index, video_index, completed):
    """Update the completion status of a video"""
    from bson.objectid import ObjectId
    return courses_collection.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": {
            f"sections.{section_index}.videos.{video_index}.completed": completed,
            "updated_at": datetime.datetime.utcnow()
        }}
    )
