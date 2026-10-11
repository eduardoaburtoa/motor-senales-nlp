"""Controles didácticos: no emiten órdenes ni pronostican rendimientos."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Supuestos:
    comision_compra: float = .01
    comision_venta: float = .01
    persistencia: float = .35
    margen_seguridad: float = 0.0
    max_rotaciones_anuales: int = 2

def evaluar_cambio(posicion_mxn, diferencial_historico, perfil_compatible,
                   liquidez_compatible, rotaciones_anuales=0,
                   fee_adicional_no_incluido=0.0, supuestos=Supuestos()):
    """Tasas decimales; horizonte comparable de un año. Supuestos, no tarifas BBVA.

    Los gastos del fondo NO se restan otra vez si los rendimientos ya son netos.
    `fee_adicional_no_incluido` solo aplica a gastos que no estén en el retorno.
    Se usa aproximación conservadora de ambas comisiones sobre el mismo nominal.
    Un resultado favorable es para revisión humana, nunca autorización de venta.
    """
    vals=[posicion_mxn,diferencial_historico,fee_adicional_no_incluido]
    import math
    if not all(math.isfinite(float(v)) for v in vals) or posicion_mxn<=0:
        raise ValueError('Valores finitos y posición positiva requeridos')
    if fee_adicional_no_incluido < 0 or not 0 <= supuestos.persistencia <= 1:
        raise ValueError('Revisar fee y persistencia')
    costo=supuestos.comision_compra+supuestos.comision_venta+fee_adicional_no_incluido
    diferencial_escenario=diferencial_historico*supuestos.persistencia
    neto=diferencial_escenario-costo
    motivos=[]
    if not perfil_compatible:motivos.append('perfil no compatible')
    if not liquidez_compatible:motivos.append('liquidez no compatible')
    if rotaciones_anuales>=supuestos.max_rotaciones_anuales:motivos.append('límite anual')
    if neto<=supuestos.margen_seguridad:motivos.append('no supera costo y margen')
    return dict(estado='BLOQUEADO' if motivos else 'REQUIERE_REVISION_HUMANA',
                motivos=motivos,costo_supuesto_mxn=posicion_mxn*costo,
                beneficio_neto_escenario_mxn=posicion_mxn*neto,
                beneficio_neto_escenario_pct=100*neto,
                orden_autorizada=False)
