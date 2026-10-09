# Meeting Request & Tracking System

A lightweight, web-based application for managing organizational meeting requests. It allows employees to submit meeting requests with digital signatures and tracks their status, while providing administrators with a dashboard to approve, reject, or modify meeting details.

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture & Structure](#-architecture--structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [License](#-license)

## ✨ Features

### User Side (`index.html`)
- **Meeting Request Form:** Comprehensive form capturing requester details, meeting subject, goals, proposed date/time, duration, location, and type (In-person/Online/Combined).
- **Attendee Management:** Dynamic addition of attendees with Name and Department/Unit.
- **Digital Signature:** Integrated `SignaturePad` for capturing user signatures.
- **Emergency Requests:** A dedicated tab for urgent meetings that triggers an SMS notification to the CEO/Manager.
- **Tracking System:** Users can check the status of their requests using a unique tracking code.

### Admin Side (`admin.html` / `admin.php`)
- **Live Dashboard:** Real-time view of all meeting requests with status indicators (Pending, Approved, Rejected).
- **Request Management:** Admins can update status, modify proposed dates/locations, and add admin notes.
- **Live Search:** Instant filtering of requests by name, subject, or tracking code.
- **Notifications:** Browser-based notifications for new incoming requests.
- **Access Control:** Basic password protection via `admin.php` (Note: See Security Notes).

## 🛠 Tech Stack

- **Backend:** Python 3 with Flask
- **Database:** SQLite3 (Embedded, file-based)
- **Frontend:**
  - HTML5 / CSS3
  - Tailwind CSS (via CDN)
  - Vanilla JavaScript
  - FontAwesome (Icons)
  - SweetAlert2 (UI Alerts)
  - SignaturePad (Canvas drawing)

## 🏗 Architecture & Structure

The project follows a simple MVC-like structure suitable for small-scale internal tools.

```text
project_root/
│
├── app.py                  # Flask backend application & API endpoints
├── meetings.db             # SQLite database (auto-generated on first run)
├── templates/
│   ├── index.html          # Main user interface (Request & Tracking)
│   └── admin.html          # Admin dashboard interface
├── admin.php               # Simple PHP wrapper for password protection
└── README.md               # This file
```

### Database Schema (`meeting_requests` table)
- `id`: Auto-increment primary key.
- `tracking_code`: Unique string (e.g., `TRK-YYYYMMDD-XXXX`).
- `req_name`, `req_role`, `req_phone`: Requester details.
- `subject`, `goal`, `proposed_date`, `duration`, `location`: Meeting details.
- `meeting_type`, `priority`: Enums for type and urgency.
- `attendees`: JSON string containing list of attendees.
- `signature`: Base64 encoded image string.
- `status`: Current state (`در حال بررسی`, `موافقت شده`, `عدم موافقت`).
- `admin_notes`: Feedback from the administrator.
- `created_at`: Timestamp of creation.

## 📥 Installation & Setup

### Prerequisites
- Python 3.6+
- pip (Python Package Installer)

### Steps
1. **Clone or Download** the project files.
2. **Install Dependencies:**
   Although this project uses minimal dependencies, ensure Flask is installed:
   ```bash
   pip install flask
   ```
   *(Note: The frontend uses CDN links for Tailwind, FontAwesome, etc., so no npm/yarn installation is required.)*

3. **Initialize Database:**
   The database (`meetings.db`) is automatically created when the application starts for the first time.

4. **Run the Application:**
   ```bash
   python app.py
   ```
   The server will start at `http://127.0.0.1:5000`.

## 🚀 Usage

### For Users
1. Open `http://127.0.0.1:5000/` in your browser.
2. Fill out the **Meeting Request** form.
3. Draw your signature in the designated canvas.
4. Click **Submit**. You will receive a **Tracking Code**.
5. Use the **Track Request** tab to check the status later.

### For Administrators
1. Access the admin panel via `http://127.0.0.1:5000/admin`.
   - *Note: If using `admin.php`, enter the password defined in the script (default: `3112768a`) to load `admin.html`.*
2. Review incoming requests in the dashboard.
3. Click **Review** on a request to expand details.
4. Update the **Status**, **Date**, **Location**, or **Admin Notes**.
5. Click **Save** to update the request. The user will see these changes when they track their request.

## 📡 API Documentation

The backend exposes the following RESTful endpoints:

### 1. Create Meeting Request
- **Endpoint:** `POST /api/requests`
- **Body:** JSON object containing form fields (`req_name`, `subject`, `attendees` as array, `signature` as base64 string, etc.).
- **Response:**
  ```json
  {
    "status": "success",
    "message": "درخواست با موفقیت ثبت شد",
    "tracking_code": "TRK-20231027-1234"
  }
  ```

### 2. Track Request
- **Endpoint:** `GET /api/track/<tracking_code>`
- **Response:**
  ```json
  {
    "status": "success",
    "data": {
      "id": 1,
      "tracking_code": "TRK-20231027-1234",
      "status": "موافقت شده",
      "proposed_date": "1405/05/10",
      "location": "Room 101",
      "admin_notes": "Confirmed by Manager",
      ...
    }
  }
  ```

### 3. Admin: Get All Requests
- **Endpoint:** `GET /api/admin/requests`
- **Response:** List of all requests with parsed attendee JSON.

### 4. Admin: Update Request
- **Endpoint:** `PUT /api/admin/requests/<int:req_id>`
- **Body:** JSON with `status`, `proposed_date`, `location`, `admin_notes`.

### 5. Admin: Check for New Requests
- **Endpoint:** `GET /api/admin/check-new`
- **Response:** `{"latest_id": 15, "total_count": 15}` (Used for polling new notifications).
## 📝 License

This project is provided as-is for internal organizational use. No specific open-source license is declared in the source files.
