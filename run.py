#!/usr/bin/env python3

from app import app

if __name__ == "__main__":
    app.secret_key = '6bb282b8a4d88ec9e482482a90212682f02a6729dd72e72f'
    app.run()