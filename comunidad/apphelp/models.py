from django.db import models
from ckeditor.fields import  RichTextField
from django.contrib.auth.models import User
from user.models import Profile

# Create your models here.


class Categoria(models.Model): 

	nombre = models.CharField('Nombre de la Categoria' , max_length = 100, null=False , blank=False)
	estado = models.BooleanField('Categoria Activada/ Categoria no Activada' , default=True)
	fecha_creacion = models.DateField('Fecha de creacion ' , auto_now=False , auto_now_add=True)
	
	def __str__(self):
		return '{}'.format(self.nombre)   




class Post(models.Model):
	titulo = models.CharField( 'Titulo' ,max_length = 90, null=False , blank=False)		
	slug = models.SlugField(max_length = 100, null=False , blank=False)
	descripcion = models.CharField(max_length = 110, null=False , blank=False)
	imagen = models.ImageField(upload_to='post/photos')
	autor_de_post =models.ForeignKey(User , on_delete = models.CASCADE)
	profile= models.ForeignKey(Profile , on_delete = models.CASCADE)
	categoria = models.ForeignKey(Categoria , on_delete=models.CASCADE)
	estado= models.BooleanField('Publicado/No publicado' , default=True)
	fecha_creacion= models.DateField(auto_now=False , auto_now_add =True)

	def __str__(self):
		return '{} , {}'.format(self.titulo , self.id)

class coment_post(models.Model):

	comentario = models.CharField('comentario' ,max_length = 255, null=True , blank=True )
	autor_comentario = models.ForeignKey(User , on_delete=models.CASCADE)
	Post_comentario = models.ForeignKey(Post , on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.comentario)




class Servicios(models.Model):
	nombre_servicio = models.CharField(max_length = 50, null=False , blank=False)



	def __str__(self):

		return '{}'.format(self.nombre_servicio)



class Nombre_de_calle(models.Model):
	nombre_de_calle_persona = models.CharField(max_length = 50, null=False , blank=False)



	def __str__(self):

		return '{}'.format(self.nombre_de_calle_persona)		



class Censo_Servicios( models.Model):

	Nombre= models.CharField(max_length = 255, null=False , blank=False)
	apellidos = models.CharField(max_length = 255, null=False , blank=False)
	telefono = models.CharField(max_length = 12, null=False , blank=False)
	cedula = models.IntegerField()
	email = models.EmailField()
	numero_de_casa = models.IntegerField()
	cantidad_de_habitantes = models.IntegerField()
	servicio = models.ManyToManyField(Servicios)
	nombre_de_calle =  models.ForeignKey(Nombre_de_calle , on_delete=models.CASCADE )




	def __str__(self):

		return '{} , {} , {}'.format(self.Nombre , self.apellidos , self.email)



class reporte_generado(models.Model):

	persona = models.ForeignKey(Censo_Servicios , on_delete=models.CASCADE)
	servicio_seleccionado = models.ForeignKey(Servicios , on_delete=models.CASCADE)
	fecha_creacion= models.DateField(auto_now=False , auto_now_add =True)
	Pago= models.BooleanField('Pago realizado/Pago No realizado' , default=False)


