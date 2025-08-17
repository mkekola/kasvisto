import db

def get_categories():
    sql = "SELECT category FROM categories ORDER BY id"
    result = db.query(sql)
    return result


def add_plant(plant_name, light, care_info, user_id, categories):
    sql = "INSERT INTO plants (plant_name, light, care_info, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [plant_name, light, care_info, user_id])

    plant_id = db.last_insert_id()

    sql = "INSERT INTO plant_categories (plant_id, category) VALUES (?, ?)"
    for category in categories:
        db.execute(sql, [plant_id, category])


def get_category_by_id(plant_id=None):
    sql = "SELECT category FROM plant_categories WHERE plant_id = ?"
    return db.query(sql, [plant_id])


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
    result = db.query(sql, [plant_id])
    return result[0] if result else None


def update_plant(plant_id, plant_name, light, care_info):
    sql = """UPDATE plants  SET plant_name = ?,
                                light = ?,
                                care_info = ?
                            WHERE id = ?"""
    db.execute(sql, [plant_name, light, care_info, plant_id])


def delete_plant(plant_id):
    sql0 = "DELETE FROM plant_categories WHERE plant_id = ?"
    db.execute(sql0, [plant_id])
    sql = "DELETE FROM plants WHERE id = ?"
    db.execute(sql, [plant_id])


def find_plants(query):
    sql = """SELECT plants.id,
                    plants.plant_name,
                    plants.care_info
             FROM plants
             WHERE plants.plant_name LIKE ? OR plants.care_info LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
