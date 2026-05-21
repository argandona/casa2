// SUMINISTROS_URLS se pasa como global desde el template:
// { buscarSst, agregarAdicional, descargarExcel, descargarModulo }

// ── Vista tabla / tarjetas ──────────────────────────────
document.getElementById('btnTableView').addEventListener('click', function() {
    document.getElementById('tableView').classList.remove('hidden');
    document.getElementById('cardView').classList.add('hidden');
    this.classList.add('bg-blue-600', 'text-white');
    this.classList.remove('bg-gray-200', 'text-gray-700');
    document.getElementById('btnCardView').classList.remove('bg-blue-600', 'text-white');
    document.getElementById('btnCardView').classList.add('bg-gray-200', 'text-gray-700');
});

document.getElementById('btnCardView').addEventListener('click', function() {
    document.getElementById('tableView').classList.add('hidden');
    document.getElementById('cardView').classList.remove('hidden');
    this.classList.add('bg-blue-600', 'text-white');
    this.classList.remove('bg-gray-200', 'text-gray-700');
    document.getElementById('btnTableView').classList.remove('bg-blue-600', 'text-white');
    document.getElementById('btnTableView').classList.add('bg-gray-200', 'text-gray-700');
});

function checkScreenSize() {
    if (window.innerWidth < 768) {
        document.getElementById('tableView').classList.add('hidden');
        document.getElementById('cardView').classList.remove('hidden');
        document.getElementById('btnTableView').classList.remove('bg-blue-600', 'text-white');
        document.getElementById('btnTableView').classList.add('bg-gray-200', 'text-gray-700');
        document.getElementById('btnCardView').classList.add('bg-blue-600', 'text-white');
        document.getElementById('btnCardView').classList.remove('bg-gray-200', 'text-gray-700');
    } else {
        document.getElementById('tableView').classList.remove('hidden');
        document.getElementById('cardView').classList.add('hidden');
        document.getElementById('btnTableView').classList.add('bg-blue-600', 'text-white');
        document.getElementById('btnTableView').classList.remove('bg-gray-200', 'text-gray-700');
        document.getElementById('btnCardView').classList.remove('bg-blue-600', 'text-white');
        document.getElementById('btnCardView').classList.add('bg-gray-200', 'text-gray-700');
    }
}

window.addEventListener('load', checkScreenSize);
window.addEventListener('resize', checkScreenSize);

// ── Modal editar ────────────────────────────────────────
function abrirModalEditar(suministroId, sst, suministro, estadoId, fechaEjecucion, ejecutadoPor, observacion, monto) {
    document.getElementById('edit_suministro_id').value = suministroId;
    document.getElementById('edit_sst').value = sst;
    document.getElementById('edit_suministro').value = suministro;
    document.getElementById('edit_estado').value = estadoId;
    document.getElementById('edit_fecha_ejecucion').value = fechaEjecucion || '';
    document.getElementById('edit_ejecutado_por').value = ejecutadoPor || '';
    document.getElementById('edit_observacion').value = observacion || '';

    const montoInput = document.getElementById('edit_monto');
    montoInput.value = (monto ? parseFloat(monto) : 0).toFixed(2);

    document.getElementById('editModal').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('editModal').classList.add('hidden');
}

function verDetalle(suministroId) {
    document.getElementById('detailContent').innerHTML = `
        <div class="space-y-3">
            <div class="flex">
                <span class="w-32 font-medium text-gray-600">Cargando detalles...</span>
            </div>
        </div>
    `;
    document.getElementById('detailModal').classList.remove('hidden');
}

function cerrarDetailModal() {
    document.getElementById('detailModal').classList.add('hidden');
}

document.getElementById('editModal').addEventListener('click', function(e) {
    if (e.target === this) cerrarModal();
});

document.getElementById('detailModal').addEventListener('click', function(e) {
    if (e.target === this) cerrarDetailModal();
});

document.getElementById('editForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const suministroId = document.getElementById('edit_suministro_id').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const data = {
        estado_suministro: document.getElementById('edit_estado').value,
        fecha_ejecucion:   document.getElementById('edit_fecha_ejecucion').value,
        ejecutado_por:     document.getElementById('edit_ejecutado_por').value,
        observacion_contratista: document.getElementById('edit_observacion').value,
        monto: document.getElementById('edit_monto').value
    };

    if (data.monto) {
        const montoNum = parseFloat(data.monto);
        if (isNaN(montoNum) || montoNum < 0) {
            alert('El monto debe ser un número válido mayor o igual a 0');
            return;
        }
    }

    try {
        const actualizarUrl = SUMINISTROS_URLS.actualizarTpl.replace('/0/', `/${suministroId}/`);
        const response = await fetch(actualizarUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            alert('Suministro actualizado correctamente');
            location.reload();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        alert('Error al actualizar: ' + error);
    }
});

// ── Modal agregar adicional ─────────────────────────────
function abrirModalAgregarAdicional() {
    document.getElementById('addForm').reset();
    document.getElementById('sstInfo').classList.add('hidden');
    document.getElementById('add_suministro').placeholder = 'Ej: 001-AD001';
    document.getElementById('sugerenciaTexto').textContent = '';
    document.getElementById('addModal').classList.remove('hidden');
}

function cerrarAddModal() {
    document.getElementById('addModal').classList.add('hidden');
}

document.getElementById('addModal').addEventListener('click', function(e) {
    if (e.target === this) cerrarAddModal();
});

document.getElementById('addForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    if (!document.getElementById('add_sst').value) {
        alert('Por favor, seleccione una SST');
        return;
    }
    if (!document.getElementById('add_suministro').value.trim()) {
        alert('Por favor, ingrese el número de suministro');
        return;
    }
    if (!document.getElementById('add_estado_suministro').value) {
        alert('Por favor, seleccione un estado');
        return;
    }
    if (!document.getElementById('add_motivo_adicional').value.trim()) {
        alert('Por favor, ingrese el motivo del suministro adicional');
        return;
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const data = {
        sst_id:            document.getElementById('add_sst_id').value,
        suministro:        document.getElementById('add_suministro').value.trim(),
        estado_suministro: document.getElementById('add_estado_suministro').value,
        motivo_adicional:  document.getElementById('add_motivo_adicional').value.trim(),
        fecha_ejecucion:   document.getElementById('add_fecha_ejecucion').value,
        ejecutado_por:     document.getElementById('add_ejecutado_por').value.trim(),
        contacto:          document.getElementById('add_contacto').value.trim(),
        telefono:          document.getElementById('add_telefono').value.trim(),
        observacion_contratista: document.getElementById('add_observacion_contratista').value.trim(),
        monto: document.getElementById('add_monto').value || '0.00'
    };

    try {
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<svg class="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>Guardando...';
        submitBtn.disabled = true;

        const response = await fetch(SUMINISTROS_URLS.agregarAdicional, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            cerrarAddModal();
            setTimeout(() => location.reload(), 1000);
        } else {
            alert('Error: ' + result.message);
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        alert('Error al conectar con el servidor: ' + error);
        const submitBtn = e.target.querySelector('button[type="submit"]');
        submitBtn.innerHTML = 'Guardar Suministro';
        submitBtn.disabled = false;
    }
});

// ── Eliminar suministro ─────────────────────────────────
async function eliminarSuministro(suministroId, nombreSuministro) {
    const confirmar = confirm(
        `¿Estás seguro de eliminar el suministro "${nombreSuministro}"?\n\n` +
        `Esta acción NO se puede deshacer.\n\n` +
        `El estado de la SST se actualizará automáticamente.`
    );

    if (!confirmar) return;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const eliminarUrl = SUMINISTROS_URLS.eliminarTpl.replace('/0/', `/${suministroId}/`);
        const response = await fetch(eliminarUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken }
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);
            location.reload();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        alert('Error al eliminar: ' + error);
    }
}

// ── Autocompletado SST ──────────────────────────────────
document.getElementById('add_sst').addEventListener('input', async function() {
    const query = this.value.trim();
    const resultsDiv = document.getElementById('sstResults');

    if (query.length < 2) {
        resultsDiv.classList.add('hidden');
        document.getElementById('add_sst_id').value = '';
        document.getElementById('sstInfo').classList.add('hidden');
        return;
    }

    try {
        const response = await fetch(`${SUMINISTROS_URLS.buscarSst}?q=${encodeURIComponent(query)}`);
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            resultsDiv.innerHTML = result.data.map(sst => `
                <div class="sst-result-item px-4 py-3 hover:bg-gray-100 cursor-pointer border-b border-gray-100 last:border-b-0"
                     data-id="${sst.id}"
                     data-sst="${sst.sst}"
                     data-direccion="${sst.direccion}"
                     data-distrito="${sst.distrito}"
                     data-estado="${sst.estado}"
                     data-total-suministros="${sst.total_suministros}">
                    <div class="font-medium text-gray-800">${sst.sst}</div>
                    <div class="text-sm text-gray-600 truncate">${sst.direccion}</div>
                    <div class="flex justify-between text-xs text-gray-500 mt-1">
                        <span>${sst.distrito}</span>
                        <span>Suministros: ${sst.total_suministros}</span>
                    </div>
                </div>
            `).join('');
            resultsDiv.classList.remove('hidden');

            document.querySelectorAll('.sst-result-item').forEach(item => {
                item.addEventListener('click', function() {
                    const sstId          = this.dataset.id;
                    const sstCode        = this.dataset.sst;
                    const direccion      = this.dataset.direccion;
                    const distrito       = this.dataset.distrito;
                    const estado         = this.dataset.estado;
                    const totalSuministros = this.dataset.totalSuministros;

                    document.getElementById('add_sst').value    = sstCode;
                    document.getElementById('add_sst_id').value = sstId;
                    resultsDiv.classList.add('hidden');

                    const sstInfoDiv = document.getElementById('sstInfo');
                    sstInfoDiv.innerHTML = `
                        <div class="grid grid-cols-2 gap-2 text-sm">
                            <div>
                                <span class="font-medium text-gray-600">Dirección:</span>
                                <span class="text-gray-800 ml-2 block truncate" title="${direccion}">${direccion.substring(0, 50)}${direccion.length > 50 ? '...' : ''}</span>
                            </div>
                            <div>
                                <span class="font-medium text-gray-600">Distrito:</span>
                                <span class="text-gray-800 ml-2">${distrito}</span>
                            </div>
                            <div>
                                <span class="font-medium text-gray-600">Estado:</span>
                                <span class="text-gray-800 ml-2">${estado}</span>
                            </div>
                            <div>
                                <span class="font-medium text-gray-600">Total suministros:</span>
                                <span class="text-gray-800 ml-2">${totalSuministros}</span>
                            </div>
                        </div>
                    `;
                    sstInfoDiv.classList.remove('hidden');

                    const adicionalesCount = parseInt(totalSuministros.split('/')[1] || 0);
                    const sugerencia = `${sstCode}-AD${(adicionalesCount + 1).toString().padStart(3, '0')}`;
                    document.getElementById('add_suministro').value = sugerencia;
                    document.getElementById('sugerenciaTexto').textContent =
                        `Sugerencia automática (${adicionalesCount} adicionales existentes)`;
                });
            });
        } else {
            resultsDiv.innerHTML = '<div class="px-4 py-3 text-gray-500">No se encontraron SST</div>';
            resultsDiv.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error en autocompletado:', error);
    }
});

document.addEventListener('click', function(e) {
    if (!e.target.closest('.relative')) {
        document.getElementById('sstResults').classList.add('hidden');
    }
});

// ── Descargar Excel ─────────────────────────────────────
function descargarExcel() {
    const sst        = document.querySelector('input[name="sst"]')?.value || '';
    const distrito   = document.querySelector('select[name="distrito"]')?.value || '';
    const estado     = document.querySelector('select[name="estado"]')?.value || '';
    const search     = document.querySelector('input[name="search"]')?.value || '';
    const obs_lds    = document.querySelector('input[name="obs_lds"]')?.value || '';
    const fecha_desde = document.querySelector('input[name="fecha_desde"]')?.value || '';
    const fecha_hasta = document.querySelector('input[name="fecha_hasta"]')?.value || '';

    const params = [];
    if (sst)        params.push(`sst=${encodeURIComponent(sst)}`);
    if (distrito)   params.push(`distrito=${encodeURIComponent(distrito)}`);
    if (estado)     params.push(`estado=${encodeURIComponent(estado)}`);
    if (search)     params.push(`search=${encodeURIComponent(search)}`);
    if (obs_lds)    params.push(`obs_lds=${encodeURIComponent(obs_lds)}`);
    if (fecha_desde) params.push(`fecha_desde=${encodeURIComponent(fecha_desde)}`);
    if (fecha_hasta) params.push(`fecha_hasta=${encodeURIComponent(fecha_hasta)}`);

    const url = SUMINISTROS_URLS.descargarExcel + '?' + params.join('&');

    const link = document.createElement('a');
    link.href = url;
    link.download = `suministros_${new Date().toISOString().split('T')[0]}.xlsx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    alert('Descargando Excel...');
}

function descargarExcelModulo() {
    const sst      = document.querySelector('input[name="sst"]')?.value || '';
    const distrito = document.querySelector('select[name="distrito"]')?.value || '';
    const estado   = document.querySelector('select[name="estado"]')?.value || '';
    const search   = document.querySelector('input[name="search"]')?.value || '';

    const params = [];
    if (sst)      params.push(`sst=${encodeURIComponent(sst)}`);
    if (distrito) params.push(`distrito=${encodeURIComponent(distrito)}`);
    if (estado)   params.push(`estado=${encodeURIComponent(estado)}`);
    if (search)   params.push(`search=${encodeURIComponent(search)}`);

    const url = SUMINISTROS_URLS.descargarModulo + '?' + params.join('&');

    const link = document.createElement('a');
    link.href = url;
    link.download = `modulo_${new Date().toISOString().split('T')[0]}.xlsx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
