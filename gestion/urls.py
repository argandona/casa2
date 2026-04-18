from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sst/', views.sst_list, name='sst_list'),
    path('sst/cargar-excel/', views.cargar_excel_suministros, name='cargar_excel_suministros'),
    path('suministros/', views.suministro_list, name='suministro_list'),
    path('suministros/<int:suministro_id>/actualizar/', views.actualizar_suministro, name='actualizar_suministro'),
    path('suministro/agregar-adicional/', views.agregar_suministro_adicional, name='agregar_suministro_adicional'),
    path('sst/<int:sst_id>/info/', views.obtener_info_sst, name='obtener_info_sst'),
    path('suministros/<int:suministro_id>/eliminar/', views.eliminar_suministro, name='eliminar_suministro'),
    path('sst/buscar/', views.buscar_sst, name='buscar_sst'),
    path('suministros/descargar-excel/', views.descargar_excel_suministros, name='descargar_excel_suministros'),
    path('reportes/productividad/', views.reporte_productividad, name='reporte_productividad'),
    path('suministros/importar-excel/', 
         views.importar_excel_suministros, 
         name='importar_excel_suministros'),
    
    path('suministros/plantilla-importacion/', 
         views.descargar_plantilla_importacion, 
         name='descargar_plantilla_importacion'),
    path('mapa/suministros/', views.mapa_suministros, name='mapa_suministros'),
    
    path('liquidacion/', views.liquidacion_list, name='liquidacion_list'),
    path('liquidacion/<int:sst_id>/cambiar-estado/', views.cambiar_estado_liquidacion, name='cambiar_estado_liquidacion'),
    path('liquidacion/<int:sst_id>/actualizar-observacion/', views.actualizar_observacion_liquidacion, name='actualizar_observacion_liquidacion'),

     path('liquidacion/descargar-excel/', views.descargar_excel_liquidacion, name='descargar_excel_liquidacion'),


    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('', views.dashboard, name='dashboard_home'), 
]