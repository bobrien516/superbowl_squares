from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

def get_db_connection():
    return sqlite3.connect('superbowl_squares.db')

app = Flask(__name__)


# Dictionary to hold claimed squares: {square_number: email}
claimed_squares = {}

# Admin password for secure access (change as needed)
ADMIN_PASSWORD = "admin123"


@app.route('/')
def grid():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT square_number, initials FROM squares")
        claimed = {row[0]: row[1] for row in cursor.fetchall()}
    finally:
        connection.close()

    return render_template('grid.html', claimed=claimed)

@app.route('/claim', methods=['POST'])
def claim_square():
    try:
        data = request.get_json()  # Use JSON parsing for the POST request payload
        square = int(data['square'])
        email = data['email']
        initials = data['initials'].upper()
        
        # Rest of the logic remains the same
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the square is already claimed
        cursor.execute("SELECT email FROM squares WHERE square_number = ?", (square,))
        result = cursor.fetchone()
        if result:
            return jsonify({"error": "This square has already been claimed."}), 400

        # Insert the claimed square
        cursor.execute("INSERT INTO squares (square_number, email, initials) VALUES (?, ?, ?)", 
                       (square, email, initials))
        connection.commit()

    except KeyError as e:
        return jsonify({"error": f"Missing data: {e}"}), 400
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        connection.close()

    return jsonify({"message": f"Square {square} claimed successfully!"})

@app.route('/admin', methods=['GET', 'POST'])
def admin_view():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != ADMIN_PASSWORD:
            return render_template('admin.html', error="Invalid password!")

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT square_number, email FROM squares")
            claimed_squares = dict(cursor.fetchall())
        finally:
            connection.close()

        return render_template('admin_dashboard.html', claimed_squares=claimed_squares)

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
