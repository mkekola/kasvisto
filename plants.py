import db


def add_plant(plant_name, light, care_info, user_id):
    sql = "INSERT INTO plants (plant_name, light, care_info, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [plant_name, light, care_info, user_id])


def get_plants():
    sql = "SELECT id, plant_name FROM plants ORDER BY id DESC"
    return db.query(sql)


def get_plant(plant_id):
    sql = """SELECT plants.id,
                    plants.plant_name, 
                    plants.light, 
                    plants.care_info,
                    users.id user_id,
                    users.username 
              FROM plants, users 
              WHERE plants.user_id = users.id AND 
                    plants.id = ?"""
    return db.query(sql, [plant_id])[0]


def update_plant(plant_id, plant_name, light, care_info):
    sql = """UPDATE plants  SET plant_name = ?, 
                                light = ?, 
                                care_info = ? 
                            WHERE id = ?"""
    db.execute(sql, [plant_name, light, care_info, plant_id])
