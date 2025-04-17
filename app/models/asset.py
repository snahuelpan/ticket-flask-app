from app import db

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # computadora, monitor, impresora, etc.
    model = db.Column(db.String(80))
    serial_number = db.Column(db.String(80), unique=True)
    purchase_date = db.Column(db.Date)
    warranty_expiration = db.Column(db.Date)
    status = db.Column(db.String(20), default='activo')  # activo, inactivo, en_mantenimiento, dado_de_baja
    location = db.Column(db.String(120))
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Asset {self.id}: {self.name} ({self.asset_type})>'

class Software(Asset):
    __tablename__ = 'software_assets'
    
    id = db.Column(db.Integer, db.ForeignKey('assets.id'), primary_key=True)
    license_key = db.Column(db.String(120))
    license_expiration = db.Column(db.Date)
    version = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Software {self.id}: {self.name} v{self.version}>'