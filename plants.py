import db

def add_plant(plant_name, light, care_info, user_id):
    sql = "INSERT INTO plants (plant_name, light, care_info, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [plant_name, light, care_info, user_id])