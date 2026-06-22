from rest_framework import serializers
from .models import Suministro, SST, Actividad, EstadoSuministro, Distrito


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'nombre_actividad']


class EstadoSuministroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoSuministro
        fields = ['id', 'estado_suministro', 'color']


class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        fields = ['id', 'nombre_distrito']


class SuministroSerializer(serializers.ModelSerializer):
    estado_suministro = EstadoSuministroSerializer(read_only=True)
    actividad = ActividadSerializer(read_only=True)
    distrito = DistritoSerializer(read_only=True)
    sst_codigo = serializers.CharField(source='sst.sst', read_only=True)

    class Meta:
        model = Suministro
        fields = [
            'id', 'sst_codigo', 'suministro', 'no_ot', 'tipo_suministro',
            'medidor', 'fase', 'potencia', 'direccion', 'distrito',
            'fecha_programada', 'hora_inicio_programada', 'hora_fin_programada',
            'fecha_ejecucion', 'ejecutado_por',
            'estado_suministro', 'actividad', 'monto',
            'observacion_contratista',
        ]


class SuministroUpdateSerializer(serializers.ModelSerializer):
    # Acepta el estado por su nombre (ej. "EJECUTADO"/"DEVUELTO") en vez del id.
    estado_suministro = serializers.SlugRelatedField(
        slug_field='estado_suministro',
        queryset=EstadoSuministro.objects.all(),
        required=False,
    )

    class Meta:
        model = Suministro
        fields = [
            'estado_suministro', 'fecha_programada',
            'fecha_ejecucion', 'ejecutado_por',
            'observacion_contratista', 'monto',
        ]


class SSTSerializer(serializers.ModelSerializer):
    distrito = DistritoSerializer(read_only=True)
    estado_sst = serializers.StringRelatedField()

    class Meta:
        model = SST
        fields = [
            'id', 'sst', 'direccion', 'distrito', 'estado_sst',
            'monto_proyectado', 'monto_real',
        ]
