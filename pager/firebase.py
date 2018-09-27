import os

import firebase_admin
from firebase_admin import credentials

from openPagerServer import settings

firebase_credentials_file = os.path.join(settings.BASE_DIR, 'config', 'serviceAccountKey.json')
cred = credentials.Certificate(firebase_credentials_file)
firebase_app = firebase_admin.initialize_app(cred)
