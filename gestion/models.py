from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal


placa_peruana_validator = RegexValidator(
    regex=r'^[A-Z]{3}-\d{3}$|^[A-Z]{2}-\d{4}$|^[A-Z]\d{2}-\d{3}$',
    message='Formato de placa inválido. Use formatos: ABC-123, AB-1234, o A12-345'
)


class Insumos(models.Model):
    nombre_insumo = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Insumo")
    unidad_medida = models.CharField(max_length=50, verbose_name="Unidad de Medida")
    precio = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Precio Unitario")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        ordering = ['nombre_insumo']
        
    def __str__(self):
        return f"{self.nombre_insumo} ({self.unidad_medida})"


class UnidadTransporte(models.Model):
    nombre_transporte = models.CharField(max_length=100, verbose_name="Nombre del Transporte")
    placa = models.CharField(max_length=20, unique=True, validators=[placa_peruana_validator], verbose_name="Placa")
    costo_por_hora = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Costo por Hora")
    tipo_vehiculo = models.CharField(
        max_length=50,
        choices=[
            ('CAMIONETA', 'Camioneta'),
            ('CAMION', 'Camión'),
            ('MINIVAN', 'Minivan'),
            ('GRUA', 'Grúa'),
            ('AUTO', 'Automóvil'),
        ],
        default='CAMION',
        verbose_name="Tipo de Vehículo"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Unidad de Transporte"
        verbose_name_plural = "Unidades de Transporte"
        ordering = ['tipo_vehiculo', 'nombre_transporte']
        
    def __str__(self):
        return f"{self.nombre_transporte} - {self.placa}"


class CargoEmpleado(models.Model):
    nombre_cargo = models.CharField(max_length=100, unique=True, verbose_name="Cargo")
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Cargo")
    
    class Meta:
        verbose_name = "Cargo de Empleado"
        verbose_name_plural = "Cargos de Empleados"
        ordering = ['nombre_cargo']
        
    def __str__(self):
        return self.nombre_cargo


class Actividad(models.Model):
    nombre_actividad = models.CharField(max_length=100, unique=True, verbose_name="Actividad")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
   
    
    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ['nombre_actividad']
        
    def __str__(self):
        return self.nombre_actividad


class Distrito(models.Model):
    nombre_distrito = models.CharField(max_length=100, unique=True, verbose_name="Distrito")
    
    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['nombre_distrito']
        
    def __str__(self):
        return self.nombre_distrito


class TipoIdentificacion(models.Model):
    nombre_tipo = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Identificación")
    
    class Meta:
        verbose_name = "Tipo de Identificación"
        verbose_name_plural = "Tipos de Identificación"
        ordering = ['nombre_tipo']
        
    def __str__(self):
        return self.nombre_tipo


class Epp(models.Model):
    nombre_epp = models.CharField(max_length=100, unique=True, verbose_name="Nombre del EPP")
    costo = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Costo")
    unidad_medida = models.CharField(max_length=50, verbose_name="Unidad de Medida")
    
    
    class Meta:
        verbose_name = "EPP"
        verbose_name_plural = "EPPs"
        ordering = ['nombre_epp']
        
    def __str__(self):
        return self.nombre_epp


class EstadoSST(models.Model):
    estado = models.CharField(max_length=50, unique=True, verbose_name="Estado")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    color = models.CharField(max_length=7, default='#007bff', verbose_name="Color", help_text="Color en formato hexadecimal (#FFFFFF)")
    
    class Meta:
        verbose_name = "Estado SST"
        verbose_name_plural = "Estados SST"
        ordering = ['estado']
        
    def __str__(self):
        return self.estado


class EstadoSuministro(models.Model):
    estado_suministro = models.CharField(max_length=50, unique=True, verbose_name="Estado")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    color = models.CharField(max_length=7, default='#007bff', verbose_name="Color", help_text="Color en formato hexadecimal (#FFFFFF)")
    
    class Meta:
        verbose_name = "Estado Suministro"
        verbose_name_plural = "Estados Suministro"
        ordering = ['estado_suministro']
        
    def __str__(self):
        return self.estado_suministro


class SST(models.Model):
    sst = models.CharField(max_length=7, unique=True, db_index=True, verbose_name="Código SST")
    direccion = models.TextField(verbose_name="Dirección")
    distrito = models.ForeignKey('Distrito', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Distrito")
    estado_sst = models.ForeignKey('EstadoSST', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Estado")
    
    
    #monto_proyectado = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], 
     #                                      null=True, blank=True, verbose_name="Monto Proyectado")
    
    monto_proyectado = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name="Monto Proyectado",
        help_text="Suma automática de todos los suministros"
    )
    
    #monto_real = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Monto Real")
    
    monto_real = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Monto Real")
    inicio_real = models.DateField(null=True, blank=True, verbose_name="Inicio Real")
    fin_real = models.DateField(null=True, blank=True, verbose_name="Fin Real")
    fecha_entrega_reporte_electrico_liquidacion = models.DateField(null=True, blank=True, verbose_name="Entrega Reporte Eléctrico Liquidación")
    fecha_entrega_reporte_civil_liquidacion = models.DateField(null=True, blank=True, verbose_name="Entrega Reporte Civil Liquidación")
    fecha_entrega_reporte_a_area_de_liquidacion = models.DateField(null=True, blank=True, verbose_name="Entrega Reporte a Área de Liquidación")
    fecha_liquidacion_sistema = models.DateField(null=True, blank=True, verbose_name="Liquidación Sistema")
    observacion = models.TextField(blank=True, verbose_name="Observaciones")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")
    
    class Meta:
        verbose_name = "SST"
        verbose_name_plural = "SSTs"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.sst} - {self.estado_sst.estado if self.estado_sst else 'Sin estado'}"
    
    def calcular_costo_ejecucion(self):
        """
        Calcula el costo real sumando Personal (sueldo histórico), 
        Insumos y Transporte.
        """
        from datetime import datetime, timedelta
        
        total_personal = Decimal('0.00')
        total_insumos = Decimal('0.00')
        total_transporte = Decimal('0.00')

        # 1. Calcular Personal basado en sueldo en la fecha de la actividad
        programaciones = self.programaciones_personal.all()
        for prog in programaciones:
            # Buscamos el sueldo que tenía el empleado en la fecha de la programación
            sueldo_historico = HistorialSueldo.objects.filter(
                empleado=prog.nombre_empleado,
                fecha_inicio__lte=prog.fecha
            ).first()
            
            if sueldo_historico:
                # Calculamos horas trabajadas
                fecha_hora_inicio = datetime.combine(prog.fecha, prog.hora_inicio)
                fecha_hora_fin = datetime.combine(prog.fecha, prog.hora_fin)
                diferencia = fecha_hora_fin - fecha_hora_inicio
                horas = Decimal(str(diferencia.total_seconds() / 3600))
                
                # Sueldo mensual / 30 días / 8 horas = costo por hora
                costo_hora = sueldo_historico.sueldo / Decimal('240')
                total_personal += (costo_hora * horas)

        # 2. Calcular Insumos
        for sst_insumo in self.sst_insumos.all():
            total_insumos += (sst_insumo.nombre_insumo.precio * sst_insumo.cantidad)

        # 3. Calcular Transporte
        for prog_t in self.programaciones_transporte.all():
            fecha_hora_inicio = datetime.combine(prog_t.fecha, prog_t.hora_inicio)
            fecha_hora_fin = datetime.combine(prog_t.fecha, prog_t.hora_fin)
            diferencia = fecha_hora_fin - fecha_hora_inicio
            horas_t = Decimal(str(diferencia.total_seconds() / 3600))
            total_transporte += (prog_t.nombre_transporte.costo_por_hora * horas_t)

        self.monto_real = total_personal + total_insumos + total_transporte
        self.save()
        return self.monto_real
    
    def actualizar_monto_total(self):
        """
        Actualiza el monto_proyectado de la SST sumando todos los montos de sus suministros
        """
        from django.db.models import Sum
        
        # Sumar montos de todos los suministros (originales + adicionales)
        resultado = self.suministros.aggregate(
            total=Sum('monto', default=Decimal('0.00'))
        )
        
        nuevo_total = resultado['total']
        
        # Solo actualizar si hay cambio
        if self.monto_proyectado != nuevo_total:
            self.monto_proyectado = nuevo_total
            self.save(update_fields=['monto_proyectado'])
            print(f"DEBUG: SST {self.sst} monto actualizado a {nuevo_total}")
        
        return nuevo_total
    
    @property
    def monto_total_formateado(self):
        """Devuelve el monto formateado para mostrar"""
        return f"S/ {self.monto_proyectado:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    
    
    @property
    def monto_total_suministros(self):
        """Calcula el monto total de todos los suministros de esta SST"""
        total = self.suministros.aggregate(
            total=models.Sum('monto', default=Decimal('0.00'))
        )['total']
        return total if total else Decimal('0.00')        

    # ... tus campos existentes ...
    def actualizar_estado_segun_suministros(self):
        """
        Actualiza el estado de la SST según los estados de sus suministros
        (tanto originales como adicionales)
        """
        suministros = self.suministros.all()  # Incluye originales y adicionales
        
        if not suministros.exists():
            return  # No hay suministros, no cambiar estado
        
        # Obtener o crear estados
        estado_ejecutado, _ = EstadoSST.objects.get_or_create(
            estado='EJECUTADO',
            defaults={'descripcion': 'Trabajo completado', 'color': '#10B981'}
        )
        estado_admisible, _ = EstadoSST.objects.get_or_create(
            estado='ADMISIBLE',
            defaults={'descripcion': 'Asignado y listo', 'color': '#3B82F6'}
        )
        estado_en_ejecucion, _ = EstadoSST.objects.get_or_create(
            estado='EN EJECUCIÓN',
            defaults={'descripcion': 'Trabajo en progreso', 'color': '#F59E0B'}
        )
        
        # Contar estados de suministros (todos los tipos)
        estados_suministros = suministros.values_list('estado_suministro__estado_suministro', flat=True)
        estados_upper = [e.upper() if e else '' for e in estados_suministros]
        
        total = suministros.count()
        ejecutados_o_devueltos = sum(1 for e in estados_upper if e in ['EJECUTADO', 'DEVUELTO'])
        asignados = sum(1 for e in estados_upper if e == 'ASIGNADO')
        
        # Lógica de actualización
        if ejecutados_o_devueltos == total:
            # Todos (originales + adicionales) están ejecutados o devueltos
            self.estado_sst = estado_ejecutado
        elif asignados == total:
            # Todos están asignados
            self.estado_sst = estado_admisible
        elif ejecutados_o_devueltos > 0:
            # Al menos uno ejecutado o devuelto (pero no todos)
            self.estado_sst = estado_en_ejecucion
        
        self.save()   


class Suministro(models.Model):
    sst = models.ForeignKey(
        SST,
        on_delete=models.PROTECT,
        related_name="suministros",
        verbose_name="SST"
    )

    tipo_suministro = models.CharField(
        max_length=20,
        choices=[
            ('ORIGINAL', 'Original'),
            ('ADICIONAL', 'Adicional'),
        ],
        default='ORIGINAL',
        verbose_name="Tipo de Suministro"
    )
    
    # Identificación
    item = models.PositiveIntegerField()
    no_ot = models.CharField(max_length=20, verbose_name="N° OT")
    suministro = models.CharField(max_length=20, db_index=True, verbose_name="Suministro")
    
    # ✅ Campo monto único y correcto
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        verbose_name="Monto (S/)",
        help_text="Monto en soles del suministro"
    )
    
    medidor = models.CharField(max_length=20, blank=True, null=True)
    marca_medidor = models.CharField(max_length=20, blank=True, null=True)
    fase = models.CharField(max_length=10, blank=True, null=True)
    potencia = models.CharField(max_length=20, blank=True, null=True)
    
    # Ubicación
    direccion = models.TextField()
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Distrito")
    latitud = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    # Programación
    fecha_primer_envio = models.DateField(null=True, blank=True)
    fecha_programada = models.DateField(null=True, blank=True)
    hora_inicio_programada = models.TimeField(blank=True, null=True)
    hora_fin_programada = models.TimeField(blank=True, null=True)

    # Ejecución
    fecha_ejecucion = models.DateField(null=True, blank=True)
    ejecutado_por = models.CharField(max_length=100, blank=True, null=True)

    # Contacto
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    # Estado y observaciones
    estado_suministro = models.ForeignKey('EstadoSuministro', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Estado Suministro")
    observacion_cliente = models.TextField(blank=True, null=True)
    observacion_contratista = models.TextField(blank=True, null=True)
    Observacion_LDS=models.TextField(blank=True, null=True)
    

    # Campos específicos para suministros adicionales
    motivo_adicional = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Motivo del suministro adicional",
        help_text="¿Por qué se agregó este suministro adicional?"
    )
    solicitado_por = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Solicitado por"
    )
    fecha_identificacion = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Fecha de identificación"
    )

    created_at = models.DateTimeField(auto_now_add=True)  # SOLO UNA VEZ

    class Meta:
        verbose_name = "Suministro"
        verbose_name_plural = "Suministros"
        ordering = ["tipo_suministro", "item"]
        unique_together = ("sst", "suministro")  # SOLO UNA VEZ

    def __str__(self):
        tipo = "ADIC" if self.tipo_suministro == 'ADICIONAL' else ""
        return f"SST {self.sst.sst} - SUM {self.suministro} {tipo}"

    def save(self, *args, **kwargs):
        # Si es adicional y no tiene fecha_identificacion, usar fecha actual
        if self.tipo_suministro == 'ADICIONAL' and not self.fecha_identificacion:
            self.fecha_identificacion = timezone.now().date()
        
        # Generar un item automático si es adicional y no tiene item
        if self.tipo_suministro == 'ADICIONAL' and not self.item:
            # Buscar el último item de esta SST
            ultimo_suministro = Suministro.objects.filter(
                sst=self.sst
            ).order_by('-item').first()
            
            if ultimo_suministro:
                self.item = ultimo_suministro.item + 1
            else:
                self.item = 1
        
        # ✅ Calcular monto automáticamente si es 0.00
        if not self.monto or self.monto == Decimal('0.00'):
            self.monto = self.calcular_monto_automatico()
        
        # Guardar el suministro primero
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # ✅ ACTUALIZAR MONTO DE LA SST (una sola vez)
        self.sst.actualizar_monto_total()
        
        # ✅ Actualizar estado de la SST (una sola vez)
        self.sst.actualizar_estado_segun_suministros()
        
    def delete(self, *args, **kwargs):
        """Sobrescribir delete para actualizar monto de la SST al eliminar"""
        sst = self.sst
        
        # Eliminar el suministro
        super().delete(*args, **kwargs)
        
        # ✅ ACTUALIZAR MONTO DE LA SST
        sst.actualizar_monto_total()
        
        # ✅ Actualizar estado de la SST
        sst.actualizar_estado_segun_suministros()

    def calcular_monto_automatico(self):
        """
        Calcula el monto automáticamente si no está definido
        """
        if self.tipo_suministro == 'ORIGINAL':
            base = Decimal('0.00')
        else:
            base = Decimal('00.00')
        
        # Ajuste por potencia si existe
        if self.potencia:
            try:
                import re
                numeros = re.findall(r'\d+\.?\d*', str(self.potencia))
                if numeros:
                    potencia_num = Decimal(numeros[0])
                    if potencia_num > Decimal('5.0'):
                        base *= Decimal('1.2')
            except:
                pass
        
        return base.quantize(Decimal('0.01'))
        
    
class Empleado(models.Model):
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.PROTECT, verbose_name="Tipo de Identificación")
    numero_identificacion = models.CharField(max_length=20, unique=True, db_index=True, verbose_name="Número de Identificación")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Email")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    cargo = models.ForeignKey(CargoEmpleado, on_delete=models.PROTECT, verbose_name="Cargo")
    estado = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVO', 'Activo'),
            ('INACTIVO', 'Inactivo'),
        ], 
        default='ACTIVO',
        verbose_name="Estado"
    )
    fecha_ingreso = models.DateField(null=True, blank=True, verbose_name="Fecha de Ingreso")
    fecha_cese = models.DateField(null=True, blank=True, verbose_name="Fecha de Cese")
    
    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']
        
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    @property
    def sueldo_actual(self):
        """Devuelve el sueldo vigente a la fecha de hoy"""
        sueldo_reg = self.historial_sueldos.filter(fecha_inicio__lte=timezone.now().date()).first()
        return sueldo_reg.sueldo if sueldo_reg else Decimal('0.00')


class HistorialSueldo(models.Model):
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE, related_name='historial_sueldos')
    sueldo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    fecha_inicio = models.DateField(verbose_name="Vigente desde")
    motivo = models.CharField(max_length=255, blank=True, null=True, help_text="Ej: Aumento anual, ascenso, etc.")

    class Meta:
        verbose_name = "Historial de Sueldo"
        verbose_name_plural = "Historial de Sueldos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.empleado} - {self.sueldo} desde {self.fecha_inicio}"


class EmpleadoEpp(models.Model):
    nombre_empleado = models.ForeignKey('Empleado', on_delete=models.PROTECT, related_name='epps_asignados')
    nombre_epp = models.ForeignKey(Epp, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    fecha = models.DateField(verbose_name="Fecha de Asignación")
    observacion = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = "Empleado EPP"
        verbose_name_plural = "Empleado EPPs"
        ordering = ['-fecha']
        
    def __str__(self):
        return f"{self.nombre_empleado} - {self.nombre_epp.nombre_epp}"


class ProgramacionPersonalSST(models.Model):
    sst = models.ForeignKey(SST, on_delete=models.PROTECT, related_name='programaciones_personal')
    nombre_empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    nombre_actividad = models.ForeignKey(Actividad, on_delete=models.PROTECT)
    fecha = models.DateField(verbose_name="Fecha")
    hora_inicio = models.TimeField(verbose_name="Hora Inicio")
    hora_fin = models.TimeField(verbose_name="Hora Fin")
    observacion = models.TextField(blank=True, verbose_name="Observaciones")
    estado = models.CharField(
        max_length=20,
        choices=[
            ('PROGRAMADO', 'Programado'),
            ('EN_EJECUCION', 'En Ejecución'),           
            ('EJECUTADO', 'Ejecutado'),
            ('PARALIZADO', 'Paralizado'),
            ('PENDIENTE', 'Pendiente'),
        ],
        default='PROGRAMADO',
        verbose_name="Estado"
    )
    
    class Meta:
        verbose_name = "Programación Personal SST"
        verbose_name_plural = "Programaciones Personal SST"
        unique_together = ['nombre_empleado', 'fecha', 'hora_inicio']
        ordering = ['-fecha', 'hora_inicio']
        
    def __str__(self):
        return f"{self.sst.sst} - {self.nombre_empleado} - {self.nombre_actividad.nombre_actividad}"


class SSTInsumo(models.Model):
    sst = models.ForeignKey(SST, on_delete=models.PROTECT, related_name='sst_insumos')
    nombre_insumo = models.ForeignKey(Insumos, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    fecha = models.DateField(verbose_name="Fecha de Uso")
    observacion = models.TextField(blank=True, verbose_name="Observaciones")
    
    
    class Meta:
        verbose_name = "SST Insumo"
        verbose_name_plural = "SST Insumos"
        unique_together = ['sst', 'nombre_insumo', 'fecha']
        ordering = ['-fecha']
        
    def __str__(self):
        return f"{self.sst.sst} - {self.nombre_insumo.nombre_insumo}"


class ProgramacionTransporteSST(models.Model):
    sst = models.ForeignKey(SST, on_delete=models.PROTECT, related_name='programaciones_transporte')
    nombre_transporte = models.ForeignKey(UnidadTransporte, on_delete=models.PROTECT)
    fecha = models.DateField(verbose_name="Fecha")
    hora_inicio = models.TimeField(verbose_name="Hora Inicio")
    hora_fin = models.TimeField(verbose_name="Hora Fin")
    observacion = models.TextField(blank=True, verbose_name="Observaciones")
    estado = models.CharField(
        max_length=20,
        choices=[
            ('PROGRAMADO', 'Programado'),
            ('EN_EJECUCION', 'En Ejecución'),
            ('TERMINADO', 'Terminado'),
            ('CANCELADO', 'Cancelado'),
        ],
        default='PROGRAMADO',
        verbose_name="Estado"
    )
    
    class Meta:
        verbose_name = "Programación Transporte SST"
        verbose_name_plural = "Programaciones Transporte SST"
        unique_together = ['nombre_transporte', 'fecha', 'hora_inicio']
        ordering = ['-fecha', 'hora_inicio']
        
    def __str__(self):
        return f"{self.sst.sst} - {self.nombre_transporte.nombre_transporte} - {self.fecha}"