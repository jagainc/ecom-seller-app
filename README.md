# 🏩 Ecom Seller App

![GitHub repo size](https://img.shields.io/github/repo-size/jagainc/ecom-seller-app?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/jagainc/ecom-seller-app?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/jagainc/ecom-seller-app?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/jagainc/ecom-seller-app?style=flat-square)

A modern desktop application for **e-commerce sellers** to manage products, orders, and gain sales insights. Built with **PyQt6 frontend**, **Java Spring Boot backend**, and **JFreeChart** for rich data visualization.

---

## ✨ Features

* 📦 **Inventory Management** – Add, update, and remove product listings.
* 📈 **Sales Analytics** – Visualized insights using **JFreeChart**.
* 📋 **Order Tracking** – View and update customer order status.
* 💬 **Seller Dashboard** – Clean, responsive UI for daily operations.
* 🔄 **REST API Integration** between Java and Python components.
* 🔐 **Authentication System** (login-based access).

---

## 📸 Preview

> *(Screenshots coming soon! Add preview images here from your app’s UI)*

---

## 🛠 Tech Stack

**Frontend**
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge\&logo=qt\&logoColor=white)

**Backend**
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge\&logo=java\&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge\&logo=spring-boot\&logoColor=white)

**Visualization & Tools**
![JFreeChart](https://img.shields.io/badge/JFreeChart-003B6F?style=for-the-badge\&logo=chartmogul\&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge\&logo=mysql\&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge\&logo=postman\&logoColor=white)

---

## 📦 Installation

### 🔧 Prerequisites

* Python 3.8+
* Java 11+
* Maven
* PyQt6 (`pip install pyqt6`)
* `requests` module (`pip install requests`)

---

### 🚀 Setup Instructions

#### Clone the Repository

```bash
git clone https://github.com/jagainc/ecom-seller-app.git
cd ecom-seller-app
```

#### 🖥️ Frontend (PyQt GUI)

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

#### 🌐 Backend (Java Spring Boot)

```bash
cd backend
./mvnw spring-boot:run
```

Backend runs at: `http://localhost:8080/`

---

## 📊 API Overview

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/api/products`    | List all products   |
| POST   | `/api/products`    | Add a new product   |
| PUT    | `/api/orders/{id}` | Update order status |
| GET    | `/api/analytics`   | Get chart data      |

---

## 👌 Contributing

Contributions are welcome!
To contribute:

1. Fork this repo
2. Create a new branch (`feature/your-feature`)
3. Commit your changes
4. Push and create a PR


## 👤 Author

**Jagadeeshwaran**
📧 [Email](mailto:jagadeeshwaranps2005@gmail.com)
🔗 [GitHub](https://github.com/jagainc)

---
