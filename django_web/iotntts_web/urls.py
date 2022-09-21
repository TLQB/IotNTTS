from django.urls import path,include  
from .import views
urlpatterns = [
	path(r"",views.home),
	path(r"data-realtime",views.home),
	path(r"data-warning",views.dataWarning),
	path(r"control-motor",views.controlMotor),
	path(r"settings",views.settings),
	path(r"manager",views.manager),
	path(r"login",views.login),
	path(r"logout",views.logout),
	path("ajax/getData",views.getData,name ="getData"),
	path('my-ajax-test/', views.onoffmotor),

]