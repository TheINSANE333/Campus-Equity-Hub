from datetime import datetime, timedelta
from app.chat_dbhandler import ChatRepository

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

def getUnreadCount(app, user_id):
    chat_dbHandler = ChatRepository(app)
    return chat_dbHandler.get_total_unread(user_id)