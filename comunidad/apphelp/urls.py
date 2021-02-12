from django.urls import path
from .views import (inicio , Crear_Autor_Post , showNews , CreateComent , add_person_servis, 
 list_person_servis , contacto , UserDetail , update_profile , Create_senso ,
  Create_Senso_Steps_2 , ReportePersonasPDF2)

urlpatterns = [

	
	path('' , inicio.as_view(), name='index'), 
   
  path('crear_post', Crear_Autor_Post.as_view() , name= 'crear_post'),
  path('news/', showNews.as_view() , name="news_covi19"),
  path('createcoment/<int:pk>', CreateComent.as_view() , name="Create"),
  path('contacto/', contacto , name = "contacto" ),
  path('UserDetail/<int:pk>/', UserDetail.as_view() , name='UserDetail'),
  path('profile' , update_profile , name = 'update_profile'), 




   #url's persona servicio

  path('crear_persona/', add_person_servis.as_view() , name="crear_persona"),
  path('listar_persona/', list_person_servis.as_view() , name="listar_persona"),
  path('Create_senso/', Create_senso , name = "Create_senso" ),

  path('Senso_Steps_2/<str:street>/<str:service>', Create_Senso_Steps_2.as_view() , name='census_steps_2' ),
  path('ReporteSenso/', ReportePersonasPDF2.as_view() , name='census_steps_2' )



 ]