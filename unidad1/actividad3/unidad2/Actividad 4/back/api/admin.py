from django.contrib import admin
from .models.post import Post
from .models.clase import Clase
admin.site.register(Post)
admin.site.register(Clase)