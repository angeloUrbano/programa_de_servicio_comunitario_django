from django.shortcuts import render , redirect , HttpResponseRedirect 
from django.urls import reverse

from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import  View ,TemplateView , ListView , UpdateView ,CreateView , DeleteView
from django.http import HttpRequest , HttpResponse
from .models import ( Post ,  coment_post , Categoria , Censo_Servicios , Nombre_de_calle ,
 Servicios , reporte_generado)
from user.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse_lazy


from .forms  import (ProfileForm , CrearPost , CreateNewComent , Add_person_servicio,
form_street , form_service  , Crearcategoria)	





from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas

from reportlab.lib import colors

from reportlab.platypus import Table , TableStyle





class inicio(TemplateView):

	template_name= "index.html"



class Crear_Autor_Post(CreateView):  


	model= Post
	second_model= Categoria
	third_model = User
	cuarto_modelo = Profile



	second_form_class= CrearPost
	third_form_class=Crearcategoria



	template_name='post/crear_post.html'

	def get_context_data(self , **kwargs): 

		


		context = {}
		
		context['form2']= self.second_form_class
		context['form3']= self.third_form_class
		
		
		
		
		return context

	def post(self , request, *args , **kwargs):
		
		form2= self.second_form_class(request.POST , request.FILES)
		form3= self.third_form_class(request.POST)
		
		
		
		
		
		if form2.is_valid() and form3.is_valid():
			print("el form es validooooo")
			variable_form2= form2.cleaned_data
			variable=form3.cleaned_data

			categoria_name= ""

			for clave in variable:

				categoria_name = variable[clave]
				print("por quiiiiii andooooooooo")


			Person = self.third_model.objects.get(pk = request.user.id)
			categoria_add = self.second_model.objects.get(nombre = categoria_name)
			perfil = self.cuarto_modelo.objects.get(id = request.user.id) 

			post = self.model()#intancia del modelo para poder guardar

			post.titulo = variable_form2['titulo']
			post.descripcion = variable_form2['descripcion']
			post.imagen = variable_form2['imagen']
			post.autor_de_post = Person
			post.profile = perfil 
			post.categoria = categoria_add
			

			post.save()
			

			print("estoy aqui")

			return redirect('help:news_covi19')
			
		else:
			print("estoy en el get")
			return 	render(request , self.template_name)



class showNews(View):
	model= Post
	template_name= "post/news.html"


	def get_queryset(self):

	 	return self.model.objects.filter(estado=True)

	def get_context_data(self , **kwargs):

		context= {}
		context['info']= self.get_queryset()
		return context

	def get(self , request , *args , **kwargs):

		return render(request , self.template_name , self.get_context_data())



class CreateComent(View):

	model= Post
	second_model= coment_post
	third_form_class = User
	form_class=  CreateNewComent
	template_name= 'post/detail_post.html'


	def get_object( self , **kwargs):
		var = self.model.objects.get(id=self.kwargs['pk'])		

		return var


	def get_queryset(self):

		try:

			return self.second_model.objects.get(Post_comentario =self.get_object().id).all()

		except Exception as e:

			return self.second_model.objects.filter(Post_comentario =self.get_object().id)
		

	

	def get_context_data(self , **kwargs):

		context= {}
		context['info']= self.get_object()
		context['date']= self.get_queryset()
		context['form']=self.form_class
		print(context['date'])
		return context



	def  get(self , request , *args , **kwargs):
		print(request.user.id)


		return render(request , self.template_name , self.get_context_data())


	def post(self , request , *args , **kwargs):

		create_coment_new=self.second_model()
		form= self.form_class(request.POST)


		#form.Post_comentario = self.get_object().id
		#print(form)
		tipo = self.third_form_class.objects.get(pk = request.user.id)
		tipo2 = self.model.objects.get(pk = self.get_object().id)
		if form.is_valid():
			data= form.cleaned_data
			create_coment_new.comentario = data['comentario']
			create_coment_new.autor_comentario = tipo
			create_coment_new.Post_comentario = tipo2

			create_coment_new.save()

			return render(request , self.template_name , self.get_context_data())
		else:
			

			return render(request , "post/news.html")


	

	
	
def contacto(request):

	if request.method =="POST":

		subjects= request.POST["asunto"]

		message= request.POST["mensaje"] + " " + request.POST["email"]
		email_from=settings.EMAIL_HOST_USER

		RECIPIENT_LIST=["coroemma@hotmail.com" , "trabajofiends@gmail.com"]

		send_mail(subjects , message , email_from , RECIPIENT_LIST)

		return render(request , "post/gracias.html")
	
	return render(request, "post/contacto.html")





class UserDetail(DeleteView):
	
	
	template_name= 'post/detail_user.html'
	pk_url_kwargs= 'pk'	


	queryset= User.objects.all()

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		user = self.get_object()

		"""
		segun la documentacion esta funcion self.get_object() de encarga de hacer
		el query segun el objeto que nosotros le pasamos 
		"""
		context['posts']= Post.objects.filter(autor_de_post=user).order_by('-fecha_creacion')
		return context






def update_profile(request):
	profile= request.user.profile #esto es por la relacion onetoone a user

	if request.method=='POST':
		form= ProfileForm(request.POST , request.FILES)#request.FILES POR QUE LOS DATOS DE IMAGEN ESTAN ALLI
		if form.is_valid():

			data= form.cleaned_data 
			#import pdb;pdb.set_trace()
			profile.website= data['website']
			profile.biography= data['biography']
			profile.phone_number= data['phone_number']
			profile.picture= data['picture']
			profile.save() 
			url = reverse('help:UserDetail' , kwargs={'pk':request.user.pk})
			#reverse contruye una url  lo uso ya que redirec no permite kwargs
			return redirect(url)
			#el kwargs es por que la vista detail resive un argumento


	else:
		form= ProfileForm()

	profile= request.user.profile
	return render(request , 'post/update_profile.html',{'profile':profile,'user':request.user , 'form': ProfileForm}	)












"""
 I THIS AREA I WILL make THE CODE TO THE  CENSUS.................

"""









class add_person_servis(CreateView):

	model = Censo_Servicios
	form_class = Add_person_servicio
	template_name = 'senso/crear_persona.html'
	success_url = reverse_lazy('help:listar_persona')


class list_person_servis(ListView): 

	model= Censo_Servicios
	template_name = 'senso/listar_persona.html'





def  Create_senso(request):

	if request.method == 'POST':


		var_street  = form_street(request.POST)
		var_service = form_service(request.POST)


		if var_street.is_valid() and var_service.is_valid():


			data = var_street.cleaned_data

			street_name=""
			for clave in data:
				street_name= data[clave]

			print(street_name)
			data2 = var_service.cleaned_data

			service_name=""
			for clave in data2:
				service_name= data2[clave]
			print("auiiiiiii")	
			print(service_name)

			


			url = reverse('help:census_steps_2' ,  kwargs={'street':street_name ,
				'service':service_name})
			return redirect(url)

	else:

	
		var_street  = form_street()
		var_service = form_service()

	return render(request , 'senso/Create_senso.html' , {'var_street':var_street ,
			'var_service':var_service} )



class Create_Senso_Steps_2(ListView):

	model = Censo_Servicios
	second_model = Nombre_de_calle
	third_model = Servicios
	template_name= 'senso/listar_persona_senso.html'



	def get_context_data(self , **kwargs):
		

		var1= self.third_model.objects.get(nombre_servicio=self.kwargs['service'])
		var2= self.second_model.objects.get(nombre_de_calle_persona=self.kwargs['street'])


		

		

		
		context = super().get_context_data(**kwargs)
		context['personas']= self.model.objects.filter(nombre_de_calle=var2.id )
		print(var1)

		

		
		return context 
 

	
	def post( self , request , *args , **kwargs ):

		var1= self.third_model.objects.get(nombre_servicio=self.kwargs['service'])
		var2= self.second_model.objects.get(nombre_de_calle_persona=self.kwargs['street'])


		email= self.model.objects.filter(nombre_de_calle=var2.id ,
		 servicio=var1.id )


		

		acction = False
		


		#I will to save the report

		 

		
		acumulador=0
		for elemento in range(len(email)):
			report = reporte_generado() 
			print(email[elemento])
			report.persona = email[elemento]
			report.servicio_seleccionado = var1
			report.save()
		
			acumulador +=1
			report=0

		print("acumulador")	
		print(acumulador)	
		#________________________________	

		RECIPIENT_LIST=[]

		for dato in email:
			RECIPIENT_LIST.append(dato.email)

		print(RECIPIENT_LIST)
		




		subjects= request.POST["asunto"]
		message= request.POST["mensaje"] 
		email_from=settings.EMAIL_HOST_USER

		

		send_mail(subjects , message , email_from , RECIPIENT_LIST)

		return render(request , "post/gracias.html")




class ReportePersonasPDF2(View):

	def tabla (self, pdf , y):
		encabezados=('Nombre' , 'Apellido', 'Cedula' , 'Servicio' , 'PagoRalizado' )
		detalles=[(persona.persona.Nombre , persona.persona.apellidos , persona.persona.cedula , persona.servicio_seleccionado.nombre_servicio  , persona.Pago ) for persona in reporte_generado.objects.all()]
		detalles_orden= Table([encabezados] + detalles , colWidths=[80])
		detalles_orden.setStyle(TableStyle(
			[

			('ALIGN' , (0,0) , (3,0) ,'CENTER' ),
			('GRID' , (0,0) , (-1 , -1 ) , 1 , colors.black ),
			('FONTSIZE' , (0,0) , (-1 , -1 ) , 10 ),
			]
			))

		detalles_orden.wrapOn(pdf , 800 , 600)
		detalles_orden.drawOn(pdf , 60 , y)



	def cabecera(self, pdf):
		#archivo_imagen=settings.MEDIA_ROOT+'/imagenesss/angeloo.jpg'
		#pdf.drawImage(archivo_imagen, 40 , 750 , 120 , 90 , preserveAspectRatio=True)
		pdf.setFont("Helvetica" , 16 )
		pdf.drawString(250, 790, u"Unefa")
		pdf.setFont("Helvetica" , 14 )
		pdf.drawString(200, 770, u"Reporte de Senso")


	def get (self , request , *args , **kwargs):
		response = HttpResponse(content_type='application/pdf')
		buffer = BytesIO()
		pdf= canvas.Canvas(buffer)
		self.cabecera(pdf)
		y =600
		self.tabla(pdf , y)
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response		


	
		





		
















	 	





