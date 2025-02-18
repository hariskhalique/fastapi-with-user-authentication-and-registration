# **FastAPI with User Authentication, Registration, and Kafka Integration**

## **📌 Overview**
This project is a **FastAPI-based User Authentication Microservice** following **Hexagonal Architecture**.  
It supports **user registration, authentication, event-driven messaging using Kafka, and dependency injection** using **FastAPI, Beanie (MongoDB ODM), and JWT authentication**.

---

## **📂 Project Structure**
The project follows the **Hexagonal Architecture (Ports and Adapters Pattern)**:

```
app/
│── adapters/                            # External interfaces (Adapters Layer)
│   ├── out/                              # Outbound adapters (Infrastructure Layer)
│   │   ├── database/                     # Database-related files
│   │   │   ├── entities/                 # MongoDB Models (Beanie)
│   │   │   ├── repositories/             # Database Repositories
│   │   │   ├── db.py                      # Database Configuration
│   ├── http/                             # HTTP Adapters (API Routes)
│   │   ├── auth_routes.py                # Authentication API Endpoints
│── application/                          # Application Layer (Use Cases)
│   ├── use_cases/
│   │   ├── register_use_case.py          # Handles user registration
│   ├── dependencies/
│   │   ├── auth_dependencies.py          # FastAPI dependencies
│── domain/                               # Business logic (Services & Repositories)
│   ├── services/
│   │   ├── auth_service.py               # Handles authentication logic
│── infrastructure/                        # Infrastructure Layer
│   ├── kafka/                             # Kafka Producer & Consumer
│   │   ├── kafka_service.py               # Kafka producer for event publishing
│   │   ├── kafka_consumer.py              # Kafka consumer for listening to events
│── main.py                               # FastAPI Application Entry
```

---

## **⚡ Features**
✅ **User Registration** – Stores users in MongoDB with hashed passwords.  
✅ **User Authentication** – Implements JWT-based authentication.  
✅ **Hexagonal Architecture** – Ensures separation of concerns (Use Cases, Services, Repositories).  
✅ **Dependency Injection** – Uses `FastAPI Depends()` for clean service injection.  
✅ **Beanie ODM (MongoDB)** – Handles user storage efficiently.  
✅ **Event-Driven Architecture with Kafka** – Publishes and consumes user registration events.  
✅ **Swagger UI Support** – API documentation at `http://127.0.0.1:8000/docs`.

---

## **🚀 Installation & Setup**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/haris-khalique2001/fastapi-with-user-authentication-and-registration.git
cd fastapi-with-user-authentication-and-registration
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Start MongoDB and Kafka Using Docker**
If you don’t have MongoDB and Kafka installed, run:
```sh
docker-compose up -d
```
_(Make sure `docker-compose.yml` includes Kafka, Zookeeper, and MongoDB configurations)_

### **4️⃣ Start FastAPI Server**
```sh
uvicorn main:app --reload
```
Now, the API will be available at:
- 🚀 **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 🔍 **Redoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## **📌 API Endpoints**
### **🔹 User Registration (With Kafka)**
```http
POST /auth/register
```
#### **Request Body**
```json
{
    "email": "test@example.com",
    "username": "testuser",
    "password": "securepassword"
}
```
#### **Response**
```json
{
    "message": "User registered successfully",
    "user_id": "123456789"
}
```

_(Kafka Event: `USER_REGISTERED` will be published)_

---

### **🔹 Kafka Consumer Listening to Events**
```sh
docker-compose logs -f kafka
```
When a user registers, Kafka will log:
```
Received message: {'event': 'USER_REGISTERED', 'user_id': 'xyz', 'email': 'test@example.com'}
Processing new user registration: xyz
```

---

## **🔐 Authentication & Security**
- **Password Hashing**: Uses `bcrypt` to securely store passwords.
- **JWT Authentication**: Tokens are generated using `pyJWT` and validated in protected routes.
- **OAuth2 Bearer Token**: Enables authentication in Swagger UI.

---

## **🛠️ Technologies Used**
| Technology  | Purpose |
|------------|---------|
| **FastAPI** | Web framework for building APIs |
| **Beanie** | MongoDB ODM for asynchronous operations |
| **Pydantic** | Data validation and serialization |
| **bcrypt** | Secure password hashing |
| **JWT (pyJWT)** | Token-based authentication |
| **aiokafka** | Asynchronous Kafka event messaging |
| **Uvicorn** | ASGI server for FastAPI |
| **Docker** | Containerized MongoDB and Kafka |

---

## **💡 Design Patterns Used**
- **Hexagonal Architecture** – Clean separation between application, domain, and infrastructure layers.
- **Event-Driven Architecture** – Kafka-based messaging for inter-service communication.
- **Dependency Injection** – Uses `Depends()` to inject `AuthService`, `UserRepository`, and `RegisterUseCase`.
- **Repository Pattern** – `UserRepository` abstracts database operations.
- **Use Case Pattern** – `RegisterUseCase` encapsulates user registration logic.

---

## **🛠️ Running Tests**
To run unit tests:
```sh
pytest tests/
```

---

## **📌 Future Improvements**
- Add refresh token support.
- Implement role-based access control (RBAC).
- Introduce background tasks for sending emails.
- Implement retries and error handling in Kafka consumers.

---

## **📝 Contributing**
1. **Fork the repository**.
2. **Create a feature branch** (`git checkout -b feature-name`).
3. **Commit changes** (`git commit -m "Added new feature"`).
4. **Push to GitHub** (`git push origin feature-name`).
5. **Create a pull request**.

---

## **📜 License**
This project is licensed under the **MIT License**.

---

## **📧 Contact**
📩 **Email**: haris_khalique2001@yahoo.com  
🐙 **GitHub**: [haris-khalique2001](https://github.com/haris-khalique2001)