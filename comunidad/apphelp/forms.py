from django import forms

from apphelp.models import  Post , Categoria , coment_post , Censo_Servicios ,  Servicios , Nombre_de_calle




class form_street(forms.ModelForm):

	class Meta:
		model = Censo_Servicios
		fields =['nombre_de_calle']

		labels={
			'nombre_de_calle':'Nombre Calle',


		}

		widgets = {

			'nombre_de_calle': forms.Select()


		}


class form_service(forms.Form):
    Servicios= forms.ModelChoiceField(
        queryset=Servicios.objects.all(),
        required=False,
        empty_label="No preference",
        label="Crearcategoria")











class Add_person_servicio(forms.ModelForm):
	class Meta:
		model = Censo_Servicios
		fields = ['Nombre' , 'apellidos' , 'cedula' , 'telefono', 'email' ,
		'numero_de_casa' ,
		'cantidad_de_habitantes',
		'servicio',
		'nombre_de_calle'
		]
		labels = {
			'Nombre': 'Nombre',
			'apellido' :'Apellidos',
			'cedula':  'Cedula',
			'telefono': 'Telefono',
			'email': 'Email',
			'numero_de_casa' : 'Nro de casa',
			'cantidad_de_habitantes' : 'Nro de habitantes',




		}





class CreateNewComent(forms.Form):

	comentario = forms.CharField(max_length=500 , required=True)
	



class CrearPost(forms.Form):

	titulo = forms.CharField(max_length=255, required=True)
	descripcion = forms.CharField(max_length=500 , required=True)
	imagen= forms.ImageField() 

	


class Crearcategoria(forms.Form):
    Categoria= forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="No preference",
        label="Crearcategoria")




class ProfileForm(forms.Form):

	website = forms.URLField(max_length=100 , required=True)
	biography = forms.CharField(max_length=500 , required=False)
	phone_number = forms.CharField(max_length=20 , required=False)
	picture= forms.ImageField()     









		




		