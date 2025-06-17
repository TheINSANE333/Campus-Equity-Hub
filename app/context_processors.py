from flask import session
import time
from app.function import getUnreadCount

def register_context_processors(app, flask_app_instance):
    """Register all template context processors."""
    
    @app.context_processor
    def inject_global_vars():
        if 'user_id' not in session:
            return dict(total_unread=0)
        
        user_id = session['user_id']
        
        # Cache logic here...
        cache_key = f'unread_count_{user_id}'
        cache_time_key = f'unread_count_time_{user_id}'
        
        if (cache_key not in session or 
            cache_time_key not in session or 
            time.time() - session[cache_time_key] > 300):
            
            session[cache_key] = getUnreadCount(flask_app_instance, user_id)
            session[cache_time_key] = time.time()
        
        return dict(total_unread=session[cache_key])