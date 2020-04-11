from flask import Flask, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = '6bb282b8a4d88ec9e482482a90212682f02a6729dd72e72f'
app.permanent_session_lifetime = timedelta(days=365)
app.config.from_object('config')

from app import views