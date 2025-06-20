from app.extensions import db

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    ic = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    pdf_filename = db.Column(db.String(255), nullable=True)
    hpnumber = db.Column(db.String(100), nullable=False)
    income = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    # Define relationship
    user = db.relationship('User', backref=db.backref('application', lazy=True))
    
    def __repr__(self):
        return f'<Application {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'ic': self.ic,
            'cgpa': self.cgpa,
            'pdf_url': f'/static/uploads/{self.pdf_filename}' if self.pdf_filename else None,
            'hpnumber': self.hpnumber,
            'income': self.income,
            'status': self.status
        }