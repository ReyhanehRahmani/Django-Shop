# 🛒 Django Shop — E-Commerce Backend

A complete **E-Commerce Backend API** built with **Django** and **Django REST Framework**.

This project provides a modular RESTful API for managing products, users, authentication, shopping carts, orders, comments, ratings, favorites, and more.

---

## 🚀 Features

### 🔐 Authentication & Authorization

* JWT-based authentication
* Phone number verification using OTP
* User registration and login
* Role-based access control
* Admin / Customer separation
* Protected API endpoints

### 👤 User Management

* User profile management
* Address management
* Favorite products
* User-specific data and permissions

### 🛍️ Product Management

* Product creation and management
* Multiple product colors
* Color-specific pricing
* Discounted prices
* Product features
* Multiple product images
* Main product image support

### 🛒 Shopping Cart

* Add products to cart
* Update cart item quantity
* Remove items from cart
* Calculate total price
* Calculate total price with discounts
* User-specific shopping carts

### 📦 Orders

* Order creation and processing
* Order items management
* Order total calculation
* Payment simulation
* User-specific order history

### 💬 Comments & Ratings

* Add comments to products
* Product rating system
* Update and delete your own comments
* Permission-based comment management

### ❤️ Favorites

* Add products to favorites
* Remove products from favorites
* User-specific favorite products

### 📚 API Documentation

* Swagger / OpenAPI documentation
* Easy API exploration and testing
* Documented endpoints

---

## 🧰 Tech Stack

| Technology               | Usage                |
| ------------------------ | -------------------- |
| 🐍 Python                | Programming Language |
| 🌐 Django                | Backend Framework    |
| 🚀 Django REST Framework | REST API Development |
| 🔑 JWT                   | Authentication       |
| 🗄️ SQLite               | Database             |
| 📚 Swagger / OpenAPI     | API Documentation    |
| 🔀 Git & GitHub          | Version Control      |
| 🧪 Postman               | API Testing          |

---

## 🏗️ Project Architecture

The project is organized into separate Django applications to keep the backend modular and maintainable.

```text
Django-Shop/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── shop/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── cart/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── comments/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── favorites/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── manage.py
└── requirements.txt
```

> The exact application structure may vary depending on the current version of the project.

---

## 🔑 Authentication

The API uses **JWT authentication** to protect authenticated endpoints.

The authentication flow is based on:

```text
User
 │
 ▼
Login / Register
 │
 ▼
JWT Access & Refresh Tokens
 │
 ▼
Authenticated API Requests
```

Protected endpoints require a valid access token.

Example:

```http
Authorization: Bearer <access_token>
```

---

## 📡 API Examples

### Get Products

```http
GET /api/shop/products/
```

### Get Product Details

```http
GET /api/shop/products/<id>/
```

### Add Item to Cart

```http
POST /api/cart/
```

Example request:

```json
{
    "color_id": 1,
    "quantity": 2
}
```

### Create Comment

```http
POST /api/shop/products/<product_id>/comments/
```

### Update / Delete Comment

```http
PUT /api/comments/<comment_id>/
PATCH /api/comments/<comment_id>/
DELETE /api/comments/<comment_id>/
```

> API paths may change as the project evolves.

---

## 📚 API Documentation

The project includes **Swagger / OpenAPI documentation** for exploring and testing the available API endpoints.

After running the project locally, open the Swagger endpoint configured in the project.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/ReyhanehRahmani/Django-Shop.git
cd Django-Shop
```

### 2. Create a virtual environment

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## 🧪 Testing

API endpoints can be tested using tools such as:

* Postman
* Swagger UI
* Browser / REST clients

Authentication-protected endpoints require a valid JWT access token.

---

## 📌 Project Highlights

This project demonstrates practical experience with:

* RESTful API development
* Django REST Framework
* JWT authentication
* Serializer validation
* Generic Views & Mixins
* Custom permissions
* Role-based access control
* Database relationships
* GenericForeignKey / ContentTypes
* Shopping cart logic
* Order processing
* API documentation
* Git & GitHub workflow

---

## 🎯 Future Improvements

Possible future improvements include:

* 💳 Real payment gateway integration
* 📧 Email notifications
* 🚀 Production deployment
* 🐳 Docker support
* ⚡ Redis & caching
* 🔄 Celery for asynchronous tasks
* 🧪 Automated tests
* 📊 Advanced API filtering and search

---

## 👩‍💻 Author

**Reyhaneh Rahmani**

🎓 Computer Engineering Student
💻 Django Backend Developer

* GitHub: [@ReyhanehRahmani](https://github.com/ReyhanehRahmani)
* LinkedIn: [Reyhaneh Rahmani](https://www.linkedin.com/in/reyhaneh-rahmani-80499a364/)
* Email: [reyhanehrahmanice@gmail.com](mailto:reyhanehrahmanice@gmail.com)

---

### ⭐ If you find this project useful, consider giving it a star!
