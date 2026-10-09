from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime
import random
import string
import json
import os

app = Flask(__name__)
DB_FILE = "meetings.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meeting_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_code TEXT UNIQUE NOT NULL,
            req_name TEXT NOT NULL,
            req_role TEXT NOT NULL,
            req_phone TEXT NOT NULL,
            subject TEXT NOT NULL,
            goal TEXT,
            proposed_date TEXT NOT NULL,
            duration TEXT,
            location TEXT,
            meeting_type TEXT NOT NULL,
            priority TEXT NOT NULL,
            attendees TEXT,
            extra_notes TEXT,
            signature TEXT,
            status TEXT DEFAULT 'در حال بررسی',
            admin_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def generate_tracking_code():
    today = datetime.date.today().strftime("%Y%m%d")
    rand_str = ''.join(random.choices(string.digits, k=4))
    return f"TRK-{today}-{rand_str}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/api/requests", methods=["POST"])
def create_request():
    try:
        data = request.json
        tracking_code = generate_tracking_code()
        
        attendees_str = json.dumps(data.get("attendees", []), ensure_ascii=False)
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO meeting_requests (
                tracking_code, req_name, req_role, req_phone, subject, goal,
                proposed_date, duration, location, meeting_type, priority,
                attendees, extra_notes, signature
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tracking_code,
            data.get("req_name"),
            data.get("req_role"),
            data.get("req_phone"),
            data.get("subject"),
            data.get("goal"),
            data.get("proposed_date"),
            data.get("duration"),
            data.get("location"),
            data.get("meeting_type", "حضوری"),
            data.get("priority", "عادی"),
            attendees_str,
            data.get("extra_notes"),
            data.get("signature")
        ))
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "درخواست با موفقیت ثبت شد",
            "tracking_code": tracking_code
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/track/<tracking_code>", methods=["GET"])
def track_request(tracking_code):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meeting_requests WHERE tracking_code = ?", (tracking_code.strip(),))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({"status": "error", "message": "درخواستی با این کد پیگیری پیدا نشد."}), 404
    
    item = dict(row)
    if item.get("attendees"):
        try:
            item["attendees"] = json.loads(item["attendees"])
        except:
            item["attendees"] = []
            
    return jsonify({"status": "success", "data": item})

@app.route("/api/admin/requests", methods=["GET"])
def get_all_requests():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meeting_requests ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for row in rows:
        item = dict(row)
        if item.get("attendees"):
            try:
                item["attendees"] = json.loads(item["attendees"])
            except:
                item["attendees"] = []
        result.append(item)
        
    return jsonify({"status": "success", "data": result})

@app.route("/api/admin/requests/<int:req_id>", methods=["PUT"])
def update_request(req_id):
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE meeting_requests
        SET status = ?,
            proposed_date = ?,
            location = ?,
            admin_notes = ?
        WHERE id = ?
    """, (
        data.get("status"),
        data.get("proposed_date"),
        data.get("location"),
        data.get("admin_notes"),
        req_id
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "اطلاعات درخواست بروزرسانی شد."})

@app.route("/api/admin/check-new", methods=["GET"])
def check_new_requests():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id), COUNT(*) FROM meeting_requests")
    max_id, count = cursor.fetchone()
    conn.close()
    return jsonify({"latest_id": max_id or 0, "total_count": count or 0})

if __name__ == "__main__":
    init_db()
    print("برنامه با موفقیت آماده شد. آدرس: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
