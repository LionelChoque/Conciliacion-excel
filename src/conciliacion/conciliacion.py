import pandas as pd
import numpy as np
from tkinter import filedialog, Tk
import datetime

def seleccionar_archivo(mensaje):
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal
    archivo = filedialog.askopenfilename(title=mensaje,
                                       filetypes=[("Excel files", "*.xlsx *.xls")])
    return archivo

def leer_archivos():
    # Seleccionar archivos
    print("Seleccione el archivo de extracto bancario...")
    archivo_extracto = seleccionar_archivo("Seleccione el extracto bancario")
    print("Seleccione el archivo de mayor...")
    archivo_mayor = seleccionar_archivo("Seleccione el mayor")

    # Leer archivos
    try:
        extracto = pd.read_excel(archivo_extracto)
        mayor = pd.read_excel(archivo_mayor)
        return extracto, mayor, archivo_extracto, archivo_mayor
    except Exception as e:
        print(f"Error al leer archivos: {e}")
        return None, None, None, None

def preparar_datos(extracto, mayor):
    # Agregar columnas necesarias
    extracto['Estado'] = 'Pendiente'
    extracto['Referencia_Mayor'] = ''
    extracto['Monto'] = extracto['Crédito'].fillna(0) - extracto['Débito'].fillna(0)
    
    mayor['Estado'] = 'Pendiente'
    mayor['Referencia_Extracto'] = ''
    mayor['Monto'] = mayor['Debe'].fillna(0) - mayor['Haber'].fillna(0)
    
    return extracto, mayor

def son_montos_similares(monto1, monto2, tolerancia=1.0):
    return abs(abs(monto1) - abs(monto2)) <= tolerancia

def son_fechas_cercanas(fecha1, fecha2, dias_tolerancia=5):
    try:
        if isinstance(fecha1, str):
            fecha1 = datetime.datetime.strptime(fecha1, '%d/%m/%Y')
        if isinstance(fecha2, str):
            fecha2 = datetime.datetime.strptime(fecha2, '%d/%m/%Y')
        
        diferencia = abs((fecha1 - fecha2).days)
        return diferencia <= dias_tolerancia
    except:
        return False

def conciliar_movimientos(extracto, mayor):
    for idx_ext, mov_extracto in extracto.iterrows():
        monto_extracto = mov_extracto['Monto']
        fecha_extracto = mov_extracto['Fecha']
        
        for idx_may, mov_mayor in mayor.iterrows():
            if mov_mayor['Estado'] == 'Conciliado':
                continue
                
            monto_mayor = mov_mayor['Monto']
            fecha_mayor = mov_mayor['Fecha']
            
            if son_montos_similares(monto_extracto, monto_mayor) and \
               son_fechas_cercanas(fecha_extracto, fecha_mayor):
                
                # Marcar como conciliados
                extracto.at[idx_ext, 'Estado'] = 'Conciliado'
                extracto.at[idx_ext, 'Referencia_Mayor'] = f"Asiento {mov_mayor['Número Asiento']}"
                
                mayor.at[idx_may, 'Estado'] = 'Conciliado'
                mayor.at[idx_may, 'Referencia_Extracto'] = f"Fila {idx_ext + 2}"  # +2 por el encabezado y base 0
                break
    
    return extracto, mayor

def guardar_resultados(extracto, mayor, archivo_extracto, archivo_mayor):
    # Crear nombres para los nuevos archivos
    archivo_extracto_nuevo = archivo_extracto.replace('.xlsx', '_conciliado.xlsx')
    archivo_mayor_nuevo = archivo_mayor.replace('.xlsx', '_conciliado.xlsx')
    
    # Guardar archivos
    try:
        extracto.to_excel(archivo_extracto_nuevo, index=False)
        mayor.to_excel(archivo_mayor_nuevo, index=False)
        print(f"Archivos guardados como:\n{archivo_extracto_nuevo}\n{archivo_mayor_nuevo}")
    except Exception as e:
        print(f"Error al guardar archivos: {e}")

def generar_reporte(extracto, mayor):
    total_movimientos_extracto = len(extracto)
    total_movimientos_mayor = len(mayor)
    
    conciliados_extracto = len(extracto[extracto['Estado'] == 'Conciliado'])
    conciliados_mayor = len(mayor[mayor['Estado'] == 'Conciliado'])
    
    print("\nReporte de Conciliación:")
    print(f"Total movimientos en extracto: {total_movimientos_extracto}")
    print(f"Movimientos conciliados en extracto: {conciliados_extracto}")
    print(f"Movimientos pendientes en extracto: {total_movimientos_extracto - conciliados_extracto}")
    print(f"\nTotal movimientos en mayor: {total_movimientos_mayor}")
    print(f"Movimientos conciliados en mayor: {conciliados_mayor}")
    print(f"Movimientos pendientes en mayor: {total_movimientos_mayor - conciliados_mayor}")

def main():
    try:
        # Leer archivos
        extracto, mayor, archivo_extracto, archivo_mayor = leer_archivos()
        if extracto is None or mayor is None:
            return 1
        
        # Preparar datos
        extracto, mayor = preparar_datos(extracto, mayor)
        
        # Realizar conciliación
        extracto, mayor = conciliar_movimientos(extracto, mayor)
        
        # Guardar resultados
        guardar_resultados(extracto, mayor, archivo_extracto, archivo_mayor)
        
        # Generar reporte
        generar_reporte(extracto, mayor)
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

def run_cli():
    """Función de entrada para la línea de comandos"""
    import sys
    sys.exit(main())

if __name__ == "__main__":
    run_cli()