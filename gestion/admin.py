from django.contrib import admin
from .models import (
    Insumos, UnidadTransporte, CargoEmpleado, Actividad, Distrito,
    TipoIdentificacion, Epp, EstadoSST, EstadoSuministro, SST,
    Suministro, Empleado, HistorialSueldo, EmpleadoEpp,
    ProgramacionPersonalSST, SSTInsumo, ProgramacionTransporteSST,EstadoLiquidacion
)


@admin.register(Insumos)
class InsumosAdmin(admin.ModelAdmin):
    list_display = ('nombre_insumo', 'unidad_medida', 'precio', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre_insumo',)


@admin.register(UnidadTransporte)
class UnidadTransporteAdmin(admin.ModelAdmin):
    list_display = ('nombre_transporte', 'placa', 'tipo_vehiculo', 'costo_por_hora', 'activo')
    list_filter = ('tipo_vehiculo', 'activo')
    search_fields = ('nombre_transporte', 'placa')


@admin.register(CargoEmpleado)
class CargoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_cargo', 'descripcion')
    search_fields = ('nombre_cargo',)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre_actividad', 'descripcion')
    search_fields = ('nombre_actividad',)


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('nombre_distrito',)
    search_fields = ('nombre_distrito',)


@admin.register(TipoIdentificacion)
class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo',)
    search_fields = ('nombre_tipo',)


@admin.register(Epp)
class EppAdmin(admin.ModelAdmin):
    list_display = ('nombre_epp', 'unidad_medida', 'costo')
    search_fields = ('nombre_epp',)


@admin.register(EstadoSST)
class EstadoSSTAdmin(admin.ModelAdmin):
    list_display = ('estado', 'descripcion', 'color')
    search_fields = ('estado',)


@admin.register(EstadoSuministro)
class EstadoSuministroAdmin(admin.ModelAdmin):
    list_display = ('estado_suministro', 'descripcion', 'color')
    search_fields = ('estado_suministro',)


class SuministroInline(admin.TabularInline):
    model = Suministro
    extra = 0
    fields = ('item', 'suministro', 'no_ot', 'direccion', 'distrito', 'estado_suministro')


@admin.register(SST)
class SSTAdmin(admin.ModelAdmin):
    list_display = ('sst', 'distrito', 'estado_sst', 'monto_proyectado', 'monto_real', 'created_at')
    list_filter = ('estado_sst', 'distrito', 'created_at')
    search_fields = ('sst', 'direccion')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SuministroInline]
    fieldsets = (
        ('Información Básica', {
            'fields': ('sst', 'direccion', 'distrito', 'estado_sst')
        }),
        ('Montos', {
            'fields': ('monto_proyectado', 'monto_real')
        }),
        ('Fechas', {
            'fields': ('inicio_real', 'fin_real', 'fecha_entrega_reporte_electrico_liquidacion',
                      'fecha_entrega_reporte_civil_liquidacion', 'fecha_entrega_reporte_a_area_de_liquidacion',
                      'fecha_liquidacion_sistema')
        }),
        ('Observaciones', {
            'fields': ('observacion',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Suministro)
class SuministroAdmin(admin.ModelAdmin):
    list_display = ('suministro', 'sst', 'no_ot', 'distrito', 'estado_suministro', 'fecha_programada')
    list_filter = ('estado_suministro', 'distrito', 'fecha_programada')
    search_fields = ('suministro', 'no_ot', 'direccion', 'sst__sst')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Identificación', {
            'fields': ('sst', 'item', 'monto', 'no_ot', 'suministro', 'medidor', 'marca_medidor', 'fase', 'potencia')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'distrito', 'latitud', 'longitud')
        }),
        ('Programación', {
            'fields': ('fecha_primer_envio', 'fecha_programada', 'hora_inicio_programada', 'hora_fin_programada')
        }),
        ('Ejecución', {
            'fields': ('fecha_ejecucion', 'ejecutado_por')
        }),
        ('Contacto', {
            'fields': ('contacto', 'telefono')
        }),
        ('Estado y Observaciones', {
            'fields': ('estado_suministro', 'observacion_cliente', 'observacion_contratista','Observacion_LDS')
        }),
    )


class HistorialSueldoInline(admin.TabularInline):
    model = HistorialSueldo
    extra = 1
    fields = ('sueldo', 'fecha_inicio', 'motivo')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('numero_identificacion', 'nombre_completo', 'cargo', 'estado', 'fecha_ingreso')
    list_filter = ('estado', 'cargo', 'tipo_identificacion')
    search_fields = ('numero_identificacion', 'nombre', 'apellido_paterno', 'apellido_materno')
    inlines = [HistorialSueldoInline]
    
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"
    nombre_completo.short_description = 'Nombre Completo'


@admin.register(HistorialSueldo)
class HistorialSueldoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'sueldo', 'fecha_inicio', 'motivo')
    list_filter = ('fecha_inicio',)
    search_fields = ('empleado__nombre', 'empleado__apellido_paterno', 'motivo')


@admin.register(EmpleadoEpp)
class EmpleadoEppAdmin(admin.ModelAdmin):
    list_display = ('nombre_empleado', 'nombre_epp', 'cantidad', 'fecha')
    list_filter = ('fecha', 'nombre_epp')
    search_fields = ('nombre_empleado__nombre', 'nombre_empleado__apellido_paterno')


@admin.register(ProgramacionPersonalSST)
class ProgramacionPersonalSSTAdmin(admin.ModelAdmin):
    list_display = ('sst', 'nombre_empleado', 'nombre_actividad', 'fecha', 'hora_inicio', 'hora_fin', 'estado')
    list_filter = ('estado', 'fecha', 'nombre_actividad')
    search_fields = ('sst__sst', 'nombre_empleado__nombre', 'nombre_empleado__apellido_paterno')
    date_hierarchy = 'fecha'


@admin.register(SSTInsumo)
class SSTInsumoAdmin(admin.ModelAdmin):
    list_display = ('sst', 'nombre_insumo', 'cantidad', 'fecha')
    list_filter = ('fecha', 'nombre_insumo')
    search_fields = ('sst__sst', 'nombre_insumo__nombre_insumo')
    date_hierarchy = 'fecha'


@admin.register(ProgramacionTransporteSST)
class ProgramacionTransporteSSTAdmin(admin.ModelAdmin):
    list_display = ('sst', 'nombre_transporte', 'fecha', 'hora_inicio', 'hora_fin', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('sst__sst', 'nombre_transporte__nombre_transporte')
    date_hierarchy = 'fecha'
    
    
@admin.register(EstadoLiquidacion)
class EstadoLiquidacionAdmin(admin.ModelAdmin):
    list_display = ['estado', 'descripcion', 'color']
    search_fields = ['estado']    