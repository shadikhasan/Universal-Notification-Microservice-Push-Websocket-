# 📦 Universal Notification Microservice (WebSocket + REST API)

This project is a **multi-tenant**, real-time **notification microservice** designed to work with any backend or frontend via API.

✅ Built with **Django**, **Django Channels**, **Redis**, and **WebSocket**  
✅ Ideal for sending **in-app real-time notifications**  
✅ Lightweight, secure, and extendable

---

## 🚀 Features

- 🔑 API key–based multi-tenant authentication
- 🌐 Real-time push notifications via WebSocket
- 📬 Send notifications through a secure REST API
- 📊 Optional delivery tracking (per user)
- 🔁 Redis-backed channel layer for high-speed messaging
- 🔐 Auto-generates API keys for each tenant
- 🧩 Easy to integrate with any frontend (React, Vue, Flutter, etc.)

---

## 🏗️ Tech Stack

| Layer     | Technology              |
|-----------|--------------------------|
| Backend   | Django, Django REST Framework |
| Realtime  | Django Channels, WebSocket   |
| Messaging | Redis (Channels Layer)       |
| DB        | PostgreSQL or SQLite         |
| Auth      | API Key per tenant           |

---

## 📁 Project Structure

```
notifications/
├── models.py         # Tenant, Notification, DeliveryStatus
├── views.py          # REST API for sending notifications
├── consumers.py      # WebSocket consumer
├── routing.py        # WebSocket routes
├── urls.py           # API routes
├── serializers.py
core/
├── asgi.py           # ASGI entry point
├── settings.py
```

---

## ⚙️ Installation

```bash
git clone https://github.com/shadikhasan/Universal-Notification-Microservice-Push-Websocket-.git
cd Universal-Notification-Microservice-Push-Websocket-
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🧪 Run Services

### 1. Start Redis
```bash
redis-server
```

### 2. Run Django + Daphne
```bash
python manage.py migrate
python manage.py createsuperuser
daphne -b 0.0.0.0 -p 8000 core.asgi:application
```

---

## 🔐 Tenant Setup

You can create a new tenant via Django admin at:
```
http://localhost:8000/admin
```

Each tenant will have a unique **API Key** auto-generated for them.

---

## 📬 Sending a Notification (REST API)

### URL:
```
POST /api/notifications/send/
```

### Headers:
```
Authorization: Api-Key <your-api-key>
Content-Type: application/json
```

### Body:
```json
{
  "title": "New Message",
  "message": "You have a new system alert!",
  "data": {
    "type": "alert",
    "priority": "high"
  }
}

```

---

## 📡 WebSocket Client Usage

### URL:
```
ws://localhost:8000/ws/notify/?api_key=<your-api-key>
```

### JS Example:
```js
const socket = new WebSocket("ws://localhost:8000/ws/notify/?api_key=myapp123apikey");

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("🔔 Notification:", data);
};
```

All clients connected to the same tenant will receive the notification in real-time.

---

## 🛡️ Security

- API key must be securely stored
- WebSocket clients are authenticated using the API key
- Unauthenticated or deleted tenants are rejected on connect

---

## 🧰 Extensibility

- 🔄 Add email/SMS/FCM integration
- 📥 Add offline storage or unread status
- 📈 Add analytics/logging on delivery
- 👥 Support user-specific channels

---

## 🧑‍💻 Author

**Shadik Hasan**  
🔗 GitHub: [@shadikhasan](https://github.com/shadikhasan)

---

## 📄 License

This project is licensed under the MIT License.
