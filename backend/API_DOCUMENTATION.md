# BAC Hub Backend API Documentation

## Overview
This is a Django REST API for a BAC (Baccalauréat) Hub platform that manages educational resources, questions, and user interactions. The API supports JWT authentication and provides endpoints for user management, resource sharing, Q&A functionality, and image handling.

## Base URL
```
http://localhost:8000/
```

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## API Endpoints

### 1. Authentication Endpoints

#### Register User
```
POST /authentication/register/
```

**Request Body:**
```json
{
    "user": {
        "username": "string",
        "email": "string",
        "password": "string"
    },
    "field": "علوم تجريبية|رياضيات|تقني رياضي|تسيير و اقتصاد|آداب و فلسفة|لغات أجنبية",
    "city": "string (optional)",
    "school_name": "string (optional)"
}
```

**Response:**
```json
{
    "details": {
        "user": {
            "id": 1,
            "username": "string",
            "email": "string"
        },
        "field": "string",
        "city": "string",
        "school_name": "string",
        "xp": 0
    },
    "success": "user created successfully",
    "refresh": "string",
    "access": "string"
}
```

#### Login User
```
POST /authentication/login/
```

**Request Body:**
```json
{
    "email": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "refresh": "string",
    "access": "string"
}
```

#### Change Password
```
POST /authentication/change_password/
```
**Authentication Required**

**Request Body:**
```json
{
    "old_password": "string",
    "new_password": "string",
    "new_password_confirm": "string"
}
```

**Response:**
```json
{
    "message": "Password changed successfully"
}
```

#### Get New Access Token
```
POST /authentication/get_refresh/
```

**Request Body:**
```json
{
    "refresh": "string"
}
```

**Response:**
```json
{
    "access": "string"
}
```

### 2. User Management Endpoints

#### Get My Profile
```
GET /users/profile/me/view/
```
**Authentication Required**

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "string",
        "email": "string"
    },
    "field": "string",
    "city": "string",
    "school_name": "string",
    "xp": 0
}
```

#### Update My Profile
```
PUT /users/profile/me/update/
```
**Authentication Required**

**Request Body:**
```json
{
    "field": "string (optional)",
    "city": "string (optional)",
    "school_name": "string (optional)"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "string",
        "email": "string"
    },
    "field": "string",
    "city": "string",
    "school_name": "string",
    "xp": 0
}
```

#### Get All Profiles
```
GET /users/profile/all/
```

**Response:**
```json
[
    {
        "user": {
            "id": 1,
            "username": "string",
            "email": "string"
        },
        "field": "string",
        "city": "string",
        "school_name": "string",
        "xp": 0
    }
]
```

#### Get Specific Profile
```
GET /users/profile/{profile_id}/
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "string",
        "email": "string"
    },
    "field": "string",
    "city": "string",
    "school_name": "string",
    "xp": 0
}
```

### 3. Subjects Endpoints

#### Initialize Subjects (Admin Only)
```
GET /initialize_subjects/
```
**Note:** This endpoint should only be run once to populate the database with subjects.

**Response:**
```json
{
    "details": "success"
}
```

#### Get All Subjects
```
GET /subjects/
```

**Response:**
```json
{
    "علوم تجريبية": [
        {
            "id": 1,
            "name": "string",
            "field": ["علوم تجريبية"],
            "coefficient": 3
        }
    ],
    "رياضيات": [...],
    "تقني رياضي": [...],
    "تسيير و اقتصاد": [...],
    "آداب و فلسفة": [...],
    "لغات أجنبية": [...]
}
```

#### Get Subject by ID
```
GET /subjects/{sub_id}/
```

**Response:**
```json
{
    "id": 1,
    "name": "string",
    "field": ["string"],
    "coefficient": 3
}
```

#### Update Subject
```
PUT /subjects/{sub_id}/
```

**Request Body:**
```json
{
    "name": "string (optional)",
    "coefficient": "integer (optional)"
}
```

#### Delete Subject
```
DELETE /subjects/{sub_id}/
```

#### Get Subjects by Field
```
GET /subjects/field/?field={field_name}
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "string",
        "field": ["string"],
        "coefficient": 3
    }
]
```

### 4. Resources Endpoints

#### Get All Resources
```
GET /resources/all/
```

**Response:**
```json
{
    "EXAM": [
        {
            "id": 1,
            "author": 1,
            "name": "string",
            "description": "string",
            "subject": 1,
            "type": "EXAM",
            "labels": "string",
            "link": "string",
            "additional_link": "string",
            "created_at": "2024-01-01T00:00:00Z",
            "reports": 0
        }
    ],
    "SUMMARY": [...],
    "NOTES": [...],
    "TEXT_BOOKS": [...],
    "VIDEO": [...]
}
```

#### Get Resource by ID
```
GET /resources/{resource_id}/
```

**Response:**
```json
{
    "id": 1,
    "author": 1,
    "name": "string",
    "description": "string",
    "subject": 1,
    "type": "EXAM|SUMMARY|NOTES|TEXT_BOOKS|VIDEO",
    "labels": "string",
    "link": "string",
    "additional_link": "string",
    "created_at": "2024-01-01T00:00:00Z",
    "reports": 0
}
```

#### Get Resources by Author
```
GET /resources/author/{author_id}/
```

#### Get Resources by Subject
```
GET /resources/subject/{subject_id}/
```

#### Add Resource
```
POST /resources/add/
```
**Authentication Required**

**Request Body:**
```json
{
    "name": "string",
    "description": "string",
    "subject": 1,
    "type": "EXAM|SUMMARY|NOTES|TEXT_BOOKS|VIDEO",
    "labels": "string",
    "link": "string",
    "additional_link": "string (optional)"
}
```

#### Update Resource
```
PUT /resources/update/{resource_id}/
```
**Authentication Required**

**Request Body:**
```json
{
    "name": "string (optional)",
    "description": "string (optional)",
    "subject": 1 (optional),
    "type": "string (optional)",
    "labels": "string (optional)",
    "link": "string (optional)",
    "additional_link": "string (optional)"
}
```

#### Delete Resource
```
DELETE /resources/delete/{resource_id}/
```
**Authentication Required**

#### Report Resource
```
POST /resources/report/{resource_id}/
```

### 5. Questions Endpoints

#### Get Question by ID
```
GET /resources/question/{question_id}/
```

**Response:**
```json
{
    "id": 1,
    "author": 1,
    "subject": 1,
    "content": "string",
    "date_posted": "2024-01-01",
    "reports": 0
}
```

#### Add Question
```
POST /resources/question/add/
```
**Authentication Required**

**Request Body:**
```json
{
    "subject": 1,
    "content": "string"
}
```

#### Update Question
```
PUT /resources/question/update/{question_id}/
```
**Authentication Required**

**Request Body:**
```json
{
    "subject": 1 (optional),
    "content": "string (optional)"
}
```

#### Delete Question
```
DELETE /resources/question/delete/{question_id}/
```
**Authentication Required**

#### Report Question
```
POST /resources/question/report/{question_id}/
```

#### Get Questions by Subject
```
GET /resources/question/subject/{subject_id}/
```

#### Get Questions by Author
```
GET /resources/question/author/{author_id}/
```

### 6. Replies Endpoints

#### Get Reply by ID
```
GET /resources/reply/{reply_id}/
```

**Response:**
```json
{
    "id": 1,
    "content": "string",
    "date_posted": "2024-01-01",
    "reports": 0,
    "children": [...],
    "parent": null,
    "author": 1,
    "question": 1
}
```

#### Add Reply
```
POST /resources/reply/add/
```
**Authentication Required**

**Request Body:**
```json
{
    "question": 1,
    "parent": 1 (optional),
    "content": "string"
}
```

#### Update Reply
```
PUT /resources/reply/update/{reply_id}/
```
**Authentication Required**

**Request Body:**
```json
{
    "content": "string (optional)"
}
```

#### Delete Reply
```
DELETE /resources/reply/delete/{reply_id}/
```
**Authentication Required**

#### Report Reply
```
POST /resources/reply/report/{reply_id}/
```

#### Get Replies by Question
```
GET /resources/reply/question/{question_id}/
```

### 7. Image Management Endpoints

#### Get Question Images
```
GET /resources/question/images/{qst_id}/view/
```

**Response:**
```json
[
    {
        "id": 1,
        "img": "string (URL)",
        "question": 1
    }
]
```

#### Upload Images to Question
```
POST /resources/question/images/{qst_id}/upload/
```
**Authentication Required**

**Request Body:**
```
FormData with 'images' field containing multiple image files
```

#### Delete Question Images
```
DELETE /resources/question/images/{qst_id}/delete/
```
**Authentication Required**

**Request Body:**
```json
{
    "images_ids": "1,2,3"
}
```

#### Get Reply Images
```
GET /resources/reply/images/{reply_id}/view/
```

#### Upload Images to Reply
```
POST /resources/reply/images/{reply_id}/upload/
```
**Authentication Required**

**Request Body:**
```
FormData with 'images' field containing multiple image files
```

#### Delete Reply Images
```
DELETE /resources/reply/images/{reply_id}/delete/
```
**Authentication Required**

**Request Body:**
```json
{
    "images_ids": "1,2,3"
}
```

## Data Models

### User Model
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "password": "string (write-only)"
}
```

### Profile Model
```json
{
    "user": "User object",
    "field": "string (choices: علوم تجريبية, رياضيات, تقني رياضي, تسيير و اقتصاد, آداب و فلسفة, لغات أجنبية)",
    "city": "string (optional)",
    "school_name": "string (optional)",
    "xp": "integer (default: 0)"
}
```

### Subject Model
```json
{
    "id": "integer",
    "name": "string",
    "field": "array of strings",
    "coefficient": "integer"
}
```

### Resource Model
```json
{
    "id": "integer",
    "author": "integer (User ID)",
    "name": "string",
    "description": "string",
    "subject": "integer (Subject ID)",
    "type": "string (choices: EXAM, SUMMARY, NOTES, TEXT_BOOKS, VIDEO)",
    "labels": "string",
    "link": "string (URL)",
    "additional_link": "string (URL, optional)",
    "created_at": "datetime",
    "reports": "integer (default: 0)"
}
```

### Question Model
```json
{
    "id": "integer",
    "author": "integer (User ID)",
    "subject": "integer (Subject ID)",
    "content": "string",
    "date_posted": "date",
    "reports": "integer (default: 0)"
}
```

### Reply Model
```json
{
    "id": "integer",
    "question": "integer (Question ID)",
    "parent": "integer (Reply ID, optional)",
    "author": "integer (User ID)",
    "content": "string",
    "date_posted": "date",
    "reports": "integer (default: 0)",
    "children": "array of Reply objects"
}
```

### ImageQuestion Model
```json
{
    "id": "integer",
    "img": "string (URL)",
    "question": "integer (Question ID)"
}
```

### ImageReply Model
```json
{
    "id": "integer",
    "img": "string (URL)",
    "reply": "integer (Reply ID)"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "string",
    "details": "string"
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "error": "You are not the author of this resource"
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Authentication Flow

1. **Register**: Create a new user account
2. **Login**: Get access and refresh tokens
3. **Use Access Token**: Include in Authorization header for protected endpoints
4. **Refresh Token**: Get new access token when current one expires
5. **Change Password**: Update user password

## File Upload

For image uploads, use `multipart/form-data` with the field name `images` containing the image files.

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## Security Notes

- JWT tokens expire after 60 minutes (access) and 7 days (refresh)
- Passwords are hashed using Django's built-in password hashing
- File uploads are restricted to image files
- Content reporting system automatically removes content after 5 reports

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run the server:
```bash
python manage.py runserver
```

## Testing

Use tools like Postman or curl to test the API endpoints. Remember to include the Authorization header for protected endpoints:

```
Authorization: Bearer <your_access_token>
``` 