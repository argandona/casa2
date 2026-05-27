from datetime import date, datetime

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Actividad, SST, Suministro
from .serializers import (
    ActividadSerializer,
    SSTSerializer,
    SuministroSerializer,
    SuministroUpdateSerializer,
)


class SuministroListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SuministroSerializer

    def get_queryset(self):
        qs = Suministro.objects.select_related(
            'sst', 'estado_suministro', 'actividad', 'distrito'
        )
        sst = self.request.query_params.get('sst')
        estado = self.request.query_params.get('estado')
        fecha = self.request.query_params.get('fecha_programada')
        if sst:
            qs = qs.filter(sst__sst=sst)
        if estado:
            qs = qs.filter(estado_suministro__estado_suministro__iexact=estado)
        if fecha:
            qs = qs.filter(fecha_programada=fecha)
        return qs


class SuministroDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Suministro.objects.select_related(
        'sst', 'estado_suministro', 'actividad', 'distrito'
    )

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return SuministroUpdateSerializer
        return SuministroSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ProgramacionView(generics.ListAPIView):
    """Suministros del día. Acepta ?fecha=YYYY-MM-DD, por defecto hoy."""
    permission_classes = [IsAuthenticated]
    serializer_class = SuministroSerializer

    def get_queryset(self):
        fecha_str = self.request.query_params.get('fecha')
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else date.today()
        except ValueError:
            fecha = date.today()
        return Suministro.objects.filter(fecha_programada=fecha).select_related(
            'sst', 'estado_suministro', 'actividad', 'distrito'
        )


class SSTListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SSTSerializer
    queryset = SST.objects.select_related('distrito', 'estado_sst')


class SSTDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SSTSerializer
    queryset = SST.objects.select_related('distrito', 'estado_sst')


class ActividadListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActividadSerializer
    queryset = Actividad.objects.all()
