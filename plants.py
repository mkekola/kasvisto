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

def add_comment(plant_id, user_id, content):
    sql = "INSERT INTO comments (plant_id, user_id, content) VALUES (?, ?, ?)"
    db.execute(sql, [plant_id, user_id, content])

def get_comments(plant_id):
    sql = """SELECT comments.content, comments.user_id, users.username
             FROM comments JOIN users ON comments.user_id = users.id
             WHERE comments.plant_id = ?"""
    return db.query(sql, [plant_id])

def get_images(plant_id):
    sql = "SELECT id FROM images WHERE plant_id = ?"
    return db.query(sql, [plant_id])

def add_image(plant_id, image):
    sql = "INSERT INTO images (plant_id, image) VALUES (?, ?)"
    db.execute(sql, [plant_id, image])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def remove_image(plant_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND plant_id = ?"
    db.execute(sql, [image_id, plant_id])

def get_category_by_id(plant_id=None):
    sql = "SELECT category FROM plant_categories WHERE plant_id = ?"
    return db.query(sql, [plant_id])


def get_plants():
    sql = """SELECT plants.id, 
                    plants.plant_name, 
                    users.id user_id, 
                    users.username 
                FROM plants JOIN users ON plants.user_id = users.id 
                ORDER BY plants.id DESC"""
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


def update_plant(plant_id, plant_name, light, care_info, selected_categories):
    sql = """UPDATE plants  SET plant_name = ?,
                                light = ?,
                                care_info = ?
                            WHERE id = ?"""
    db.execute(sql, [plant_name, light, care_info, plant_id])

    sql = "DELETE FROM plant_categories WHERE plant_id = ?"
    db.execute(sql, [plant_id])

    sql = "INSERT INTO plant_categories (plant_id, category) VALUES (?, ?)"
    for category in selected_categories:
        db.execute(sql, [plant_id, category])


def delete_plant(plant_id):
    sql0 = "DELETE FROM plant_categories WHERE plant_id = ?"
    db.execute(sql0, [plant_id])
    sql1 = "DELETE FROM images WHERE plant_id = ?"
    db.execute(sql1, [plant_id])
    sql2 = "DELETE FROM comments WHERE plant_id = ?"
    db.execute(sql2, [plant_id])
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
