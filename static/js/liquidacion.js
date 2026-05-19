// CSRF_TOKEN se pasa como global desde el template

const ORDEN_ESTADOS = {
    'Observado':        0,
    'En liquidacion':   1,
    'Enviado a TECSUR': 2,
    'Liquidado':        3,
    'Facturado':        4,
};

function getPrioridad(select) {
    const text = select.options[select.selectedIndex]?.text?.trim() || '';
    return ORDEN_ESTADOS[text] ?? 99;
}

function reordenarTabla() {
    const tbody = document.querySelector('#liq-table tbody');
    if (!tbody) return;

    const filas = Array.from(tbody.querySelectorAll('tr[data-sst]'));

    filas.sort((a, b) => {
        const selA = a.querySelector('.select-liquidacion');
        const selB = b.querySelector('.select-liquidacion');
        return getPrioridad(selA) - getPrioridad(selB);
    });

    filas.forEach((fila, i) => {
        fila.style.animationDelay = `${i * 30}ms`;
        fila.style.animation = 'none';
        void fila.offsetHeight;
        fila.style.animation = '';
        tbody.appendChild(fila);
    });
}

function showToast(msg, type = 'success') {
    const toast = document.getElementById('toast');
    const icon  = document.getElementById('toast-icon');
    const msgEl = document.getElementById('toast-msg');

    toast.className = `toast ${type}`;
    icon.className  = type === 'success'
        ? 'fas fa-check-circle'
        : 'fas fa-exclamation-circle';
    msgEl.textContent = msg;

    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2800);
}

function cambiarEstadoLiquidacion(select) {
    const sstId    = select.dataset.sstId;
    const estadoId = select.value;
    const ind      = document.getElementById(`ind-liq-${sstId}`);

    if (!estadoId) return;

    ind.className = 'saving-indicator show';
    ind.innerHTML = '<i class="fas fa-circle-notch fa-spin text-xs"></i><span>Guardando...</span>';

    fetch(`/liquidacion/${sstId}/cambiar-estado/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: `estado_liquidacion_id=${estadoId}`
    })
    .then(r => r.json())
    .then(data => {
        if (!data.success) throw new Error('Error');

        ind.className = 'saving-indicator show saved';
        ind.innerHTML = '<i class="fas fa-check text-xs"></i><span>Guardado</span>';
        showToast('Estado actualizado');

        setTimeout(() => reordenarTabla(), 300);
        setTimeout(() => ind.className = 'saving-indicator', 2000);
    })
    .catch(() => {
        ind.className = 'saving-indicator show error';
        ind.innerHTML = '<i class="fas fa-times text-xs"></i><span>Error al guardar</span>';
        showToast('Error al guardar el estado', 'error');
        setTimeout(() => ind.className = 'saving-indicator', 3000);
    });
}

const obsTimers = {};

function autoGuardarObservacion(textarea) {
    const sstId = textarea.dataset.sstId;
    const ind   = document.getElementById(`ind-obs-${sstId}`);

    ind.className = 'saving-indicator show';
    ind.innerHTML = '<i class="fas fa-circle-notch fa-spin text-xs"></i><span>Guardando...</span>';

    clearTimeout(obsTimers[sstId]);
    obsTimers[sstId] = setTimeout(() => {
        fetch(`/liquidacion/${sstId}/actualizar-observacion/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': CSRF_TOKEN,
            },
            body: `observacion=${encodeURIComponent(textarea.value)}`
        })
        .then(r => r.json())
        .then(data => {
            if (!data.success) throw new Error('Error');
            ind.className = 'saving-indicator show saved';
            ind.innerHTML = '<i class="fas fa-check text-xs"></i><span>Guardado</span>';
            showToast('Observación guardada');
            setTimeout(() => ind.className = 'saving-indicator', 2000);
        })
        .catch(() => {
            ind.className = 'saving-indicator show error';
            ind.innerHTML = '<i class="fas fa-times text-xs"></i><span>Error</span>';
            showToast('Error al guardar observación', 'error');
            setTimeout(() => ind.className = 'saving-indicator', 3000);
        });
    }, 900);
}

let filtroActivo = '';

function aplicarFiltros() {
    const q = document.getElementById('search-input').value.toLowerCase();

    document.querySelectorAll('#liq-table tbody tr[data-sst]').forEach(row => {
        const textoFila = row.textContent.toLowerCase();
        const coincideBusqueda = textoFila.includes(q);

        let coincideEstado = true;
        if (filtroActivo === '__sin_estado__') {
            const sel = row.querySelector('.select-liquidacion');
            coincideEstado = !sel || sel.value === '';
        } else if (filtroActivo !== '') {
            const sel = row.querySelector('.select-liquidacion');
            const textoSel = sel?.options[sel.selectedIndex]?.text?.trim() || '';
            coincideEstado = textoSel === filtroActivo;
        }

        row.style.display = (coincideBusqueda && coincideEstado) ? '' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    reordenarTabla();

    document.getElementById('search-input').addEventListener('input', aplicarFiltros);

    document.querySelectorAll('.filtro-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filtroActivo = this.dataset.estado;
            aplicarFiltros();
        });
    });
});
