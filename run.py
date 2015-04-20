#!/usr/bin/env python3

from cookierun import app

app.config.from_pyfile('../config.cfg')

app.run()
