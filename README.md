# Conciliación Bancaria Automatizada

Este proyecto proporciona una herramienta para automatizar el proceso de conciliación bancaria, comparando movimientos entre el extracto bancario y el mayor contable.

## Descripción

La herramienta permite:
- Comparar movimientos bancarios con registros contables
- Identificar coincidencias con tolerancia en montos y fechas
- Marcar partidas conciliadas
- Generar referencias cruzadas
- Producir reportes de conciliación

## Estructura de Archivos Requerida

### Extracto Bancario (Excel)
```
Columnas requeridas:
- Fecha (formato: dd/mm/yyyy)
- Descripción
- Descripcion_adicional
- Crédito
- Débito
- Saldo
```

### Mayor Contable (Excel)
```
Columnas requeridas:
- Número Asiento
- Descripción
- Fecha (formato: dd/mm/yyyy)
- Debe
- Haber
```

## Requisitos Previos

```bash
Python 3.7 o superior
pip (gestor de paquetes de Python)
```

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/LionelChoque/Conciliacion-excel.git
cd Conciliacion-excel
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
```

3. Activar el entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```
## Instalar empaquetador

```bash
pip install build wheel
```

## Empaquetar

Construir el paquete con:

```bash
python -m build
```

## Instalación


```bash
pip install dist/conciliacion_bancaria-0.1.0-py3-none-any.whl
```

## Uso

1. Ejecutar el script:
```bash
conciliacion
```

2. Seguir las instrucciones en pantalla:
   - Seleccionar archivo de extracto bancario
   - Seleccionar archivo de mayor contable

3. El programa generará:
   - Archivo de extracto conciliado (_conciliado.xlsx)
   - Archivo de mayor conciliado (_conciliado.xlsx)
   - Reporte de conciliación en consola



## Configuración

Los parámetros de tolerancia se pueden ajustar en el código:
- `tolerancia_monto = 1.0` (diferencia máxima en pesos)
- `dias_tolerancia = 5` (diferencia máxima en días)

## Estructura del Proyecto

```
conciliacion-bancaria/
│
├── conciliacion.py       # Script principal
├── requirements.txt      # Dependencias
├── setup.py             # Configuración de empaquetado
├── README.md            # Este archivo
└── tests/               # Pruebas unitarias
```

## Dependencias

```
pandas
numpy
openpyxl
```

## Contribuir

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request


## Notas Adicionales

- Los archivos Excel deben estar cerrados antes de ejecutar el programa
- Se recomienda hacer backup de los archivos originales
- Los resultados se guardan en archivos nuevos con sufijo "_conciliado"
