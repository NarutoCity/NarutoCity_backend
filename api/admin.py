from django.contrib import admin

from django.db.models.base import ModelBase
from api import models

# 筛选models中Model类的子类，统一注册到django.admin中
register_list = []
for item_str in dir(models):
    item = getattr(models, item_str)
    if type(item) == ModelBase:
        register_list.append(item)

admin.site.register(register_list)
