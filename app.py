import os
import csv
import io
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from database import db, EAData
from sqlalchemy import func
from werkzeug.utils import secure_filename

app = Flask(__name__)

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# UPLOAD PATHS
UPLOAD_IMAGE_FOLDER = os.path.join(app.root_path, 'static', 'images')
UPLOAD_GEOJSON_FOLDER = os.path.join(app.root_path, 'static', 'ea_boundaries')

# ---------------------------
# LOGIN PAGE
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # ADMIN LOGIN
        if username == "admin" and password == "bridget":
            return redirect(url_for("dashboard"))

        # ENUMERATOR LOGIN
        elif username == "enumerator" and password == "enum123":
            return redirect(url_for("geofencing"))

    return render_template("login.html")


# ---------------------------
# ADMIN DASHBOARD
# ---------------------------
@app.route("/dashboard")
def dashboard():

    records = EAData.query.all()

    total_population = db.session.query(
        func.sum(EAData.estimated_population)
    ).scalar()

    total_households = db.session.query(
        func.sum(EAData.households)
    ).scalar()

    ea_count = EAData.query.count()

    return render_template(
        "index.html",
        records=records,
        total_population=total_population,
        total_households=total_households,
        ea_count=ea_count
    )


# ---------------------------
# ENUMERATOR GEOFENCING PAGE
# ---------------------------
@app.route("/geofencing")
def geofencing():

    records = EAData.query.all()

    return render_template(
        "geofencing.html",
        records=records
    )


# ---------------------------
# EA SEARCH API (FIXED)
# ---------------------------
@app.route("/search_ea", methods=["POST"])
def search_ea():

    data = request.get_json()
    geocode = data.get("geocode")

    ea = EAData.query.filter_by(geocode=geocode).first()

    if ea:

        return jsonify({
            "success": True,
            "ea_name": ea.ea_name,
            "population": ea.estimated_population,
            "households": ea.households,
            "latitude": ea.latitude,
            "longitude": ea.longitude,
            "image": ea.image_path,
            "boundary_file": ea.boundary_file
        })

    return jsonify({"success": False})


# ---------------------------
# EA CRUD & EXPORT/IMPORT API
# ---------------------------

@app.route("/add_ea", methods=["POST"])
def add_ea():
    try:
        geocode = request.form.get("geocode")
        ea_name = request.form.get("ea_name")
        latitude = float(request.form.get("latitude", 0))
        longitude = float(request.form.get("longitude", 0))
        estimated_population = int(request.form.get("estimated_population", 0))
        households = int(request.form.get("households", 0))
        
        # Handle files
        image_file = request.files.get("image_file")
        image_path = ""
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            os.makedirs(UPLOAD_IMAGE_FOLDER, exist_ok=True)
            image_file.save(os.path.join(UPLOAD_IMAGE_FOLDER, filename))
            image_path = f"/static/images/{filename}"
            
        boundary_file = request.files.get("boundary_file")
        boundary_path = ""
        if boundary_file and boundary_file.filename:
            filename = secure_filename(boundary_file.filename)
            os.makedirs(UPLOAD_GEOJSON_FOLDER, exist_ok=True)
            boundary_file.save(os.path.join(UPLOAD_GEOJSON_FOLDER, filename))
            boundary_path = f"/static/ea_boundaries/{filename}"

        existing = EAData.query.filter_by(geocode=geocode).first()
        if existing:
            return jsonify({"success": False, "message": f"Geocode '{geocode}' already exists."}), 400

        new_ea = EAData(
            geocode=geocode,
            ea_name=ea_name,
            latitude=latitude,
            longitude=longitude,
            estimated_population=estimated_population,
            households=households,
            image_path=image_path,
            boundary_file=boundary_path
        )
        db.session.add(new_ea)
        db.session.commit()
        return jsonify({"success": True, "message": "EA added successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/edit_ea/<int:ea_id>", methods=["POST"])
def edit_ea(ea_id):
    try:
        ea = EAData.query.get_or_404(ea_id)
        
        ea.geocode = request.form.get("geocode", ea.geocode)
        ea.ea_name = request.form.get("ea_name", ea.ea_name)
        ea.latitude = float(request.form.get("latitude", ea.latitude))
        ea.longitude = float(request.form.get("longitude", ea.longitude))
        ea.estimated_population = int(request.form.get("estimated_population", ea.estimated_population))
        ea.households = int(request.form.get("households", ea.households))
        
        image_file = request.files.get("image_file")
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            os.makedirs(UPLOAD_IMAGE_FOLDER, exist_ok=True)
            image_file.save(os.path.join(UPLOAD_IMAGE_FOLDER, filename))
            ea.image_path = f"/static/images/{filename}"
            
        boundary_file = request.files.get("boundary_file")
        if boundary_file and boundary_file.filename:
            filename = secure_filename(boundary_file.filename)
            os.makedirs(UPLOAD_GEOJSON_FOLDER, exist_ok=True)
            boundary_file.save(os.path.join(UPLOAD_GEOJSON_FOLDER, filename))
            ea.boundary_file = f"/static/ea_boundaries/{filename}"

        db.session.commit()
        return jsonify({"success": True, "message": "EA updated successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/delete_ea/<int:ea_id>", methods=["POST"])
def delete_ea(ea_id):
    try:
        ea = EAData.query.get_or_404(ea_id)
        db.session.delete(ea)
        db.session.commit()
        return jsonify({"success": True, "message": "EA deleted successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/export/csv")
def export_csv():
    records = EAData.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['geocode', 'ea_name', 'latitude', 'longitude', 'estimated_population', 'households', 'image_path', 'boundary_file'])
    for r in records:
        writer.writerow([r.geocode, r.ea_name, r.latitude, r.longitude, r.estimated_population, r.households, r.image_path, r.boundary_file])
    
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name='ea_records.csv'
    )


@app.route("/export/json")
def export_json():
    records = EAData.query.all()
    data = []
    for r in records:
        data.append({
            "geocode": r.geocode,
            "ea_name": r.ea_name,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "estimated_population": r.estimated_population,
            "households": r.households,
            "image_path": r.image_path,
            "boundary_file": r.boundary_file
        })
    
    mem = io.BytesIO()
    mem.write(json.dumps(data, indent=2).encode('utf-8'))
    mem.seek(0)
    return send_file(
        mem,
        mimetype='application/json',
        as_attachment=True,
        download_name='ea_records.json'
    )


@app.route("/import/csv", methods=["POST"])
def import_csv():
    file = request.files.get("csv_file")
    if not file or not file.filename.endswith('.csv'):
        return jsonify({"success": False, "message": "Invalid file format. Please upload a CSV."}), 400
    
    try:
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.DictReader(stream)
        
        required_headers = {'geocode', 'ea_name', 'latitude', 'longitude', 'estimated_population', 'households'}
        if not required_headers.issubset(set(reader.fieldnames or [])):
            return jsonify({"success": False, "message": "Missing required CSV columns."}), 400
        
        imported_count = 0
        for row in reader:
            geocode = row['geocode']
            if not geocode:
                continue
            
            ea = EAData.query.filter_by(geocode=geocode).first()
            if ea:
                ea.ea_name = row.get('ea_name', ea.ea_name)
                ea.latitude = float(row.get('latitude', ea.latitude))
                ea.longitude = float(row.get('longitude', ea.longitude))
                ea.estimated_population = int(row.get('estimated_population', ea.estimated_population))
                ea.households = int(row.get('households', ea.households))
                ea.image_path = row.get('image_path', ea.image_path)
                ea.boundary_file = row.get('boundary_file', ea.boundary_file)
            else:
                ea = EAData(
                    geocode=geocode,
                    ea_name=row.get('ea_name'),
                    latitude=float(row.get('latitude', 0.0)),
                    longitude=float(row.get('longitude', 0.0)),
                    estimated_population=int(row.get('estimated_population', 0)),
                    households=int(row.get('households', 0)),
                    image_path=row.get('image_path', ''),
                    boundary_file=row.get('boundary_file', '')
                )
                db.session.add(ea)
            imported_count += 1
        
        db.session.commit()
        return jsonify({"success": True, "message": f"Successfully processed {imported_count} records."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Failed to parse CSV: {str(e)}"}), 500


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # ensures DB exists
    app.run(debug=True)
