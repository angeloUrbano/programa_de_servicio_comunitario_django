from django.contrib import admin
from .models import Categoria ,  Post , coment_post , Servicios , Censo_Servicios , Nombre_de_calle

# Register your models here.
admin.site.register(Categoria)

admin.site.register(Post)
admin.site.register(coment_post)
admin.site.register(Servicios)
admin.site.register(Censo_Servicios)
admin.site.register(Nombre_de_calle)
