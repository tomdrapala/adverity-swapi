import os
from django.conf import settings

BASE_DIR = getattr(settings, 'BASE_DIR', '')
PEOPLE_CSV_PATH = f"{BASE_DIR}/people_csv"


if not os.path.exists(PEOPLE_CSV_PATH):
    os.mkdir(PEOPLE_CSV_PATH)
