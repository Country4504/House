from settings import db



class House(db.Model):
    
    __tablename__ = 'house_info'
    
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(255))
    
    rooms = db.Column(db.String(255))
    
    area = db.Column(db.String(255))
    
    price = db.Column(db.String(255))
    
    direction = db.Column(db.String(255))
    
    rent_type = db.Column(db.String(255))
    
    region = db.Column(db.String(255))
    
    block = db.Column(db.String(255))
    
    address = db.Column(db.String(255))
    
    traffic = db.Column(db.String(255))
    
    publish_time = db.Column(db.Integer)
    
    facilities = db.Column(db.TEXT)
    
    highlights = db.Column(db.TEXT)
    
    matching = db.Column(db.TEXT)
    
    travel = db.Column(db.TEXT)
    
    page_views = db.Column(db.Integer)
    
    landlord = db.Column(db.String(255))
    
    phone_num = db.Column(db.String(255))
    
    house_num = db.Column(db.String(255))

    
    def __repr__(self):
        return 'House: %s, %s' % (self.address, self.id)



class Recommend(db.Model):
    
    __tablename__ = 'house_recommend'
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer)
    
    house_id = db.Column(db.Integer)
    
    title = db.Column(db.String(255))
    
    address = db.Column(db.String(255))
    
    block = db.Column(db.String(255))
    
    score = db.Column(db.Integer)




class User(db.Model):
    
    __tablename__ = 'user_info'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100))
    
    password = db.Column(db.String(100))
    
    email = db.Column(db.String(100))
    
    addr = db.Column(db.String(100))
    
    collect_id = db.Column(db.String(250))
    
    seen_id = db.Column(db.String(250))

    
    def __repr__(self):
        return 'User: %s, %s' % (self.name, self.id)