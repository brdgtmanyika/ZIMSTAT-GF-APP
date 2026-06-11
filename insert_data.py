from app import app
from database import db, EAData

with app.app_context():

    # =========================
    # EA 1
    # =========================
    ea1 = EAData(
        geocode="9211950020",
        ea_name="EA 020",
        latitude=-17.8353512,
        longitude=31.1935856,
        estimated_population=493,
        households=127,
        image_path="/static/images/ea1.jpg",
        boundary_file="/static/ea_boundaries/ea1.geojson"
    )

    # =========================
    # EA 2
    # =========================
    ea2 = EAData(
        geocode="9211950030",
        ea_name="EA 030",
        latitude=-17.8353512,
        longitude=31.1934073,
        estimated_population=415,
        households=112,
        image_path="/static/images/ea2.jpg",
        boundary_file="/static/ea_boundaries/ea2.geojson"
    )

    # =========================
    # EA 3
    # =========================
    ea3 = EAData(
        geocode="9211950040",
        ea_name="EA 040",
        latitude=-17.8349654,
        longitude=31.1950176,
        estimated_population=233,
        households=82,
        image_path="/static/images/ea3.jpg",
        boundary_file="/static/ea_boundaries/ea3.geojson"
    )

    # =========================
    # EA 4
    # =========================
    ea4 = EAData(
        geocode="9211950050",
        ea_name="EA 050",
        latitude=-17.8345194,
        longitude=31.1949511,
        estimated_population=460,
        households=125,
        image_path="/static/images/ea4.jpg",
        boundary_file="/static/ea_boundaries/ea4.geojson"
    )

    # =========================
    # EA 5
    # =========================
    ea5 = EAData(
        geocode="9211950120",
        ea_name="EA 120",
        latitude=-17.8308583,
        longitude=31.1958348,
        estimated_population=462,
        households=106,
        image_path="/static/images/ea5.jpg",
        boundary_file="/static/ea_boundaries/ea5.geojson"
    )

    # =========================
    # EA 6
    # =========================
    ea6 = EAData(
        geocode="9211950150",
        ea_name="EA 150",
        latitude=-17.8280837,
        longitude=31.1940671,
        estimated_population=351,
        households=97,
        image_path="/static/images/ea6.jpg",
        boundary_file="/static/ea_boundaries/ea6.geojson"
    )

    # =========================
    # EA 7
    # =========================
    ea7 = EAData(
        geocode="9211950170",
        ea_name="EA 170",
        latitude=-17.8295197,
        longitude=31.1937585,
        estimated_population=336,
        households=90,
        image_path="/static/images/ea7.jpg",
        boundary_file="/static/ea_boundaries/ea7.geojson"
    )

    # =========================
    # EA 8
    # =========================
    ea8 = EAData(
        geocode="9211950310",
        ea_name="EA 310",
        latitude=-17.8273469,
        longitude=31.1911051,
        estimated_population=303,
        households=80,
        image_path="/static/images/ea8.jpg",
        boundary_file="/static/ea_boundaries/ea8.geojson"
    )

    # =========================
    # EA 9
    # =========================
    ea9 = EAData(
        geocode="9211950450",
        ea_name="EA 450",
        latitude=-17.8336900,
        longitude=31.1895440,
        estimated_population=392,
        households=99,
        image_path="/static/images/ea9.jpg",
        boundary_file="/static/ea_boundaries/ea9.geojson"
    )

    # =========================
    # EA 10
    # =========================
    ea10 = EAData(
        geocode="9211950270",
        ea_name="EA 270",
        latitude=-17.8327889,
        longitude=31.1908912,
        estimated_population=388,
        households=101,
        image_path="/static/images/ea10.jpg",
        boundary_file="/static/ea_boundaries/ea10.geojson"
    )

    # =========================
    # ADD ALL RECORDS
    # =========================
    db.session.add(ea1)
    db.session.add(ea2)
    db.session.add(ea3)
    db.session.add(ea4)
    db.session.add(ea5)
    db.session.add(ea6)
    db.session.add(ea7)
    db.session.add(ea8)
    db.session.add(ea9)
    db.session.add(ea10)

    # =========================
    # SAVE TO DATABASE
    # =========================
    db.session.commit()

    print("All 10 EA records inserted successfully")
