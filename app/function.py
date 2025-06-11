from datetime import datetime, timedelta

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pdfVerification(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'pdf'

def dateCounter():
    return datetime.utcnow() - timedelta(days=2)