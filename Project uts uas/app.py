from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS

# Inisialisasi Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Konfigurasi database (sesuaikan dengan XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Default XAMPP user
app.config['MYSQL_PASSWORD'] = ''  # Kosongkan jika tanpa password
app.config['MYSQL_DB'] = 'flask_db'

mysql = MySQL(app)

@app.route("/biografi")
def biografi():
    return render_template("biografi.html")

# Route Home
@app.route("/")
def home():
    return render_template("index.html")

# CREATE (Tambah data mobil)
@app.route('/cars', methods=['POST'])
def add_car():
    try:
        data = request.json
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cars (jenis_mobil, tahun_rilis, asal_mobil, warna, mesin) VALUES (%s, %s, %s, %s, %s)",
                       (data['jenis_mobil'], data['tahun_rilis'], data['asal_mobil'], data['warna'], data['mesin']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Car added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ (Tampilkan semua data mobil)
@app.route('/cars', methods=['GET'])
def get_cars():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cars")
        rows = cursor.fetchall()
        cursor.close()
        cars = [{'id': row[0], 'jenis_mobil': row[1], 'tahun_rilis': row[2], 'asal_mobil': row[3], 'warna': row[4], 'mesin': row[5]} for row in rows]
        return jsonify(cars)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# READ BY ID (Tampilkan data mobil berdasarkan ID)
@app.route('/cars/<int:id>', methods=['GET'])
def get_car_by_id(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cars WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            car = {
                'id': row[0],
                'jenis_mobil': row[1],
                'tahun_rilis': row[2],
                'asal_mobil': row[3],
                'warna': row[4],
                'mesin': row[5]
            }
            return jsonify(car)
        else:
            return jsonify({'message': 'Car not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE (Edit data mobil)
@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    try:
        data = request.json
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE cars SET jenis_mobil = %s, tahun_rilis = %s, asal_mobil = %s, warna = %s, mesin = %s WHERE id = %s",
                       (data['jenis_mobil'], data['tahun_rilis'], data['asal_mobil'], data['warna'], data['mesin'], id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Car updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE (Hapus data mobil)
@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM cars WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Car deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
