from flask import render_template, url_for, flash, session, redirect
from app.app_stub import Flask_App_Stub
from app.dbhandler import UserRepository
from app.routes.endpoint import Endpoint
import json

class Achievement(Endpoint):
    def __init__(self, app: Flask_App_Stub) -> None:
        super().__init__(app)

        self.route = '/achievement'
        self.endpoint = 'achievement'
        self.callback = self.achievement
        self.methods = ['GET', 'POST']

    def achievement(self):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))

        user_dbhandler = UserRepository(self.flask_app)
        user = user_dbhandler.query_user_id(session['user_id'])
        achievement_point = user.achievement_point

        user_achievement_level = user_dbhandler.get_update_user_achievement_level(session['user_id'])
        if user.achievement_level != user_achievement_level:
            user_dbhandler.update_achievement_level(session.get("user_id"), user_achievement_level)

        achievement_data = {
            "point": achievement_point
        }
        json_achievement_data = json.dumps(achievement_data)
        print(json_achievement_data)

        return render_template('achievement.html', user=user)