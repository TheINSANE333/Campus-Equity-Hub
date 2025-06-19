from flask import session
import time
from app.function import getUnreadCount, getUnreadNotifications

# Configuration for different notification types
NOTIFICATION_CONFIGS = {
    'total_unread': {
        'function': getUnreadCount,
        'cache_key': 'unread_count',
        'cache_duration': 1
    },

    'unread_notifications': {
        'function': getUnreadNotifications,
        'cache_key': 'unread_messages',
        'cache_duration': 1
    },
}


def register_context_processors(app, flask_app_instance):
    """Register all template context processors."""
    
    @app.context_processor
    def inject_global_vars():
        if 'user_id' not in session:
            return {key: 0 for key in NOTIFICATION_CONFIGS.keys()}
        
        user_id = session['user_id']
        current_time = time.time()
        result = {}
        
        for template_var, config in NOTIFICATION_CONFIGS.items():
            cache_key = f"{config['cache_key']}_{user_id}"
            cache_time_key = f"{config['cache_key']}_time_{user_id}"

            if (cache_key not in session or 
                cache_time_key not in session or 
                current_time - session[cache_time_key] > config['cache_duration']):
                
                session[cache_key] = config['function'](flask_app_instance, user_id)
                session[cache_time_key] = current_time
            
            result[template_var] = session[cache_key]

        return result