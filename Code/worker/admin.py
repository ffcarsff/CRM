from django.contrib import admin
from .models import user,agent,worker,userporfile
# Register your models here.
admin.site.register(user)
admin.site.register(agent)
admin.site.register(worker)
admin.site.register(userporfile)