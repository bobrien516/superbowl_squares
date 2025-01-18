from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Dictionary to hold claimed squares: {square_number: email}
claimed_squares = {}

# Admin password for secure access (change as needed)
ADMIN_PASSWORD = "admin123"

@app.route('/')
def grid():
    return render_template('grid.html', claimed=claimed_squares.keys())

@app.route('/claim', methods=['POST'])
def claim_square():
    square = int(request.form['square'])
    email = request.form['email']

    if square in claimed_squares:
        return jsonify({"error": "This square has already been claimed."}), 400

    # Store the claimed square
    claimed_squares[square] = email
    return jsonify({"message": f"Square {square} claimed successfully!"})

@app.route('/admin', methods=['GET', 'POST'])
def admin_view():
    if request.method == 'POST':
        # Verify admin password
        password = request.form['password']
        if password != ADMIN_PASSWORD:
            return render_template('admin.html', error="Invalid password!")

        # If password is correct, show claimed squares
        return render_template('admin_dashboard.html', claimed_squares=claimed_squares)

    # Initial admin login form
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
