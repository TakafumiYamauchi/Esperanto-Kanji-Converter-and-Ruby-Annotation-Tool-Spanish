# Guía Técnica: Estructura y Funcionamiento Interno de la Aplicación de Reemplazo de Texto en Esperanto

## Índice
1. [Arquitectura general de la aplicación](#1-arquitectura-general-de-la-aplicación)
2. [Módulos principales y sus funciones](#2-módulos-principales-y-sus-funciones)
3. [Flujo de datos y algoritmos clave](#3-flujo-de-datos-y-algoritmos-clave)
4. [Estructuras de datos fundamentales](#4-estructuras-de-datos-fundamentales)
5. [Optimización y procesamiento en paralelo](#5-optimización-y-procesamiento-en-paralelo)
6. [Técnicas de manipulación de texto](#6-técnicas-de-manipulación-de-texto)
7. [Generación de archivos JSON](#7-generación-de-archivos-json)
8. [Extensibilidad y personalización](#8-extensibilidad-y-personalización)

## 1. Arquitectura general de la aplicación

La aplicación se construye sobre el framework Streamlit y sigue una arquitectura modular con clara separación de responsabilidades. El sistema está compuesto por cuatro componentes principales:

### 1.1 Estructura de archivos y dependencias

```
├── main.py                                      # Aplicación principal Streamlit
├── pages/                                       # Carpeta de páginas adicionales de Streamlit
│   └── Página para generar archivos JSON...     # Página secundaria para generar JSONs
├── esp_text_replacement_module.py               # Módulo de funciones de reemplazo de texto
├── esp_replacement_json_make_module.py          # Módulo para generar archivos JSON
└── Appの运行に使用する各类文件/                  # Carpeta de recursos
    ├── 占位符(placeholders)_*.txt               # Archivos de placeholders
    ├── *.json                                   # Archivos JSON predeterminados
    └── *.csv                                    # Archivos CSV de correspondencias
```

### 1.2 Flujo de ejecución general

El flujo de la aplicación puede dividirse en dos rutas principales:

1. **Ruta de reemplazo de texto** (main.py):
   - Carga de archivo JSON con reglas de sustitución
   - Entrada de texto en esperanto (manual o por archivo)
   - Procesamiento del texto mediante algoritmos de reemplazo
   - Visualización y descarga del resultado

2. **Ruta de generación de JSON** (Página para generar archivos JSON...):
   - Carga de archivo CSV con correspondencias esperanto-traducción
   - Carga de archivos JSON con reglas de descomposición y sustitución
   - Procesamiento y generación de listas de reemplazo
   - Creación y descarga del archivo JSON combinado

### 1.3 Principios de diseño

La aplicación está diseñada siguiendo varios principios clave:

- **Modularidad**: Separación clara entre interfaz de usuario, lógica de procesamiento y utilidades
- **Reutilización**: Funciones compartidas entre diferentes partes de la aplicación
- **Escalabilidad**: Capacidad para procesar textos de diferentes tamaños, con optimización para textos grandes
- **Flexibilidad**: Múltiples formatos de salida y opciones de configuración
- **Robustez**: Manejo de errores y casos especiales

## 2. Módulos principales y sus funciones

### 2.1 main.py

El archivo principal que coordina toda la aplicación:

- **Configuración de la interfaz de usuario Streamlit**:
  - Definición de controles para carga de archivos, entrada de texto y opciones
  - Gestión de la sesión para mantener el estado de la aplicación
  - Visualización de resultados en diferentes formatos

- **Funciones clave**:
  - `load_replacements_lists`: Carga y procesa archivos JSON con listas de reemplazo
  - `orchestrate_comprehensive_esperanto_text_replacement`: Coordina el proceso completo de sustitución
  - `parallel_process`: Implementa procesamiento en paralelo para mejorar rendimiento

### 2.2 esp_text_replacement_module.py

Módulo especializado en operaciones de transformación de texto:

- **Diccionarios de conversión de caracteres esperanto**:
  - Mapeos entre diferentes representaciones (ĉ, cx, c^, etc.)

- **Funciones de manipulación de texto**:
  - `replace_esperanto_chars`: Reemplaza caracteres según un diccionario
  - `convert_to_circumflex`: Convierte formato x o ^ a formato con acento circunflejo
  - `unify_halfwidth_spaces`: Normaliza diferentes tipos de espacios

- **Funciones de procesamiento de marcadores especiales**:
  - `find_percent_enclosed_strings_for_skipping_replacement`: Encuentra texto entre % para excluirlo
  - `find_at_enclosed_strings_for_localized_replacement`: Encuentra texto entre @ para reemplazo local

- **Función crítica de reemplazo seguro**:
  - `safe_replace`: Implementa reemplazo en dos fases usando placeholders intermedios

### 2.3 esp_replacement_json_make_module.py

Módulo para la generación y manipulación de archivos JSON:

- **Funciones de medición de texto**:
  - `measure_text_width_Arial16`: Calcula el ancho en píxeles según una tabla de referencia
  - `insert_br_at_half_width`: Inserta saltos de línea en puntos específicos

- **Funciones de formato**:
  - `output_format`: Genera diferentes formatos de salida (HTML, paréntesis, etc.)
  - `capitalize_ruby_and_rt`: Maneja las mayúsculas en etiquetas Ruby

- **Funciones de procesamiento paralelo**:
  - `process_chunk_for_pre_replacements`: Procesa un segmento de datos
  - `parallel_build_pre_replacements_dict`: Coordina el procesamiento paralelo

### 2.4 Página para generar archivos JSON...

Implementa la interfaz de usuario y lógica para crear archivos JSON:

- **Interfaz de usuario para carga de archivos**:
  - Selección de archivos CSV y JSON
  - Opciones de configuración

- **Algoritmos de generación de JSON**:
  - Procesamiento de raíces de esperanto y sus traducciones
  - Manejo de casos especiales (sufijos, prefijos, etc.)
  - Generación de listas con prioridades de reemplazo

## 3. Flujo de datos y algoritmos clave

### 3.1 Proceso principal de reemplazo de texto

El flujo completo de datos para el reemplazo de texto es:

1. **Carga de datos**:
   - Archivo JSON con tres listas de reemplazo: global, localizado y para raíces de 2 caracteres
   - Archivos de placeholders para evitar conflictos en reemplazos

2. **Preprocesamiento del texto**:
   - Normalización de espacios
   - Conversión de caracteres esperanto a formato con acento circunflejo
   - Identificación de marcadores especiales (%, @)

3. **Proceso de reemplazo**:
   - Reemplazo de secciones con marcadores especiales por placeholders
   - Aplicación de reglas de reemplazo global
   - Reemplazo de raíces de 2 caracteres
   - Restauración de placeholders con el texto procesado

4. **Postprocesamiento**:
   - Conversión final de caracteres esperanto según preferencia del usuario
   - Aplicación de formato HTML si es necesario

### 3.2 Algoritmo de reemplazo seguro

Una de las técnicas más importantes es el reemplazo seguro mediante placeholders:

```
Función safe_replace(texto, lista_reemplazos):
    1. Para cada tripla (original, reemplazo, placeholder) en lista_reemplazos:
        a. Reemplazar todas las ocurrencias de "original" por "placeholder"
        b. Guardar la relación (placeholder → reemplazo)
    2. Para cada par (placeholder, reemplazo) guardado:
        a. Reemplazar todas las ocurrencias de "placeholder" por "reemplazo"
    3. Devolver el texto resultante
```

Este algoritmo es crucial porque evita conflictos cuando una palabra a reemplazar es parte de otra o cuando un reemplazo podría coincidir con otro texto original.

### 3.3 Procesamiento en paralelo

Para textos grandes, la aplicación implementa procesamiento en paralelo:

```
Función parallel_process(texto, num_procesos, ...):
    1. Dividir el texto en segmentos (líneas) 
    2. Agrupar las líneas en chunks según el número de procesos
    3. Crear un pool de procesos
    4. Asignar cada chunk a un proceso para ejecutar process_segment
    5. Recopilar resultados de todos los procesos
    6. Unir los resultados en un solo texto
    7. Devolver el texto procesado
```

## 4. Estructuras de datos fundamentales

### 4.1 Listas de reemplazo

El archivo JSON principal contiene tres listas clave:

1. **replacements_final_list**: Para reemplazo global de palabras
   - Estructura: `[(palabra_original, reemplazo, placeholder), ...]`
   - Ejemplo: `("amiko", "<ruby>amiko<rt>amigo</rt></ruby>", "$39475$")`

2. **replacements_list_for_localized_string**: Para reemplazo dentro de marcadores @
   - Misma estructura que replacements_final_list pero usando placeholders diferentes

3. **replacements_list_for_2char**: Para raíces de dos caracteres
   - Incluye prefijos, sufijos y palabras independientes
   - Estructura similar pero con marcado especial

### 4.2 Diccionarios de conversión de caracteres

```python
x_to_circumflex = {
    'cx': 'ĉ', 'gx': 'ĝ', 'hx': 'ĥ', 'jx': 'ĵ', 'sx': 'ŝ', 'ux': 'ŭ',
    'Cx': 'Ĉ', 'Gx': 'Ĝ', 'Hx': 'Ĥ', 'Jx': 'Ĵ', 'Sx': 'Ŝ', 'Ux': 'Ŭ'
}
# (Y otros diccionarios similares para diferentes conversiones)
```

### 4.3 Diccionario de anchos de caracteres

Utilizado para calcular el ancho visual de texto y ajustar el tamaño de las anotaciones Ruby:

```python
# Cargado desde Unicode_BMP全范围文字幅(宽)_Arial16.json
char_widths_dict = {
    'a': 12,  # Ancho en píxeles para Arial 16
    'b': 12,
    # ... miles de caracteres más
}
```

### 4.4 Estructuras especiales para la generación de JSON

- **pre_replacements_dict**: Diccionario intermedio para construir reglas de reemplazo
  - Clave: palabra original
  - Valor: [texto de reemplazo, información de parte del discurso, prioridad]

- **Listas para sufijos y prefijos especiales**:
  - `suffix_2char_roots`: Lista de sufijos de 2 caracteres (ad, ag, am, etc.)
  - `prefix_2char_roots`: Lista de prefijos de 2 caracteres (al, bo, ge, etc.)
  - `standalone_2char_roots`: Lista de palabras independientes de 2 caracteres

## 5. Optimización y procesamiento en paralelo

### 5.1 Técnicas de caché

La aplicación implementa varias técnicas para optimizar el rendimiento:

```python
@st.cache_data
def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
    # Función para cargar y cachear datos JSON
    # Evita recargar archivos grandes entre ejecuciones
```

### 5.2 Implementación del procesamiento en paralelo

El procesamiento en paralelo se implementa mediante el módulo `multiprocessing`:

```python
def parallel_process(text, num_processes, ...):
    # Divide el texto en segmentos
    lines = re.findall(r'.*?\n|.+$', text)
    # Calcula cuántas líneas procesar por proceso
    lines_per_process = max(num_lines // num_processes, 1)
    # Crea rangos para cada proceso
    ranges = [(i * lines_per_process, (i + 1) * lines_per_process) 
              for i in range(num_processes)]
    # Ajusta el último rango para incluir todas las líneas restantes
    ranges[-1] = (ranges[-1][0], num_lines)
    # Crea un pool de procesos y distribuye el trabajo
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(process_segment, [...])
    # Une los resultados
    return ''.join(results)
```

### 5.3 Configuración específica para Streamlit

```python
# Configuración especial para evitar problemas con multiprocessing en Streamlit
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass  # Ya configurado, ignorar
```

### 5.4 Optimizaciones para la generación de JSON

```python
def parallel_build_pre_replacements_dict(
    E_stem_with_Part_Of_Speech_list,
    replacements,
    num_processes=4
):
    # Divide la lista de raíces en chunks
    # Procesa cada chunk en paralelo
    # Combina los resultados
```

## 6. Técnicas de manipulación de texto

### 6.1 Expresiones regulares para patrones especiales

La aplicación utiliza expresiones regulares para identificar patrones específicos:

```python
# Patrón para encontrar texto entre % (hasta 50 caracteres)
PERCENT_PATTERN = re.compile(r'%(.{1,50}?)%')

# Patrón para encontrar texto entre @ (hasta 18 caracteres)
AT_PATTERN = re.compile(r'@(.{1,18}?)@')

# Patrón para identificar etiquetas Ruby con contenido idéntico
IDENTICAL_RUBY_PATTERN = re.compile(r'<ruby>([^<]+)<rt class="XXL_L">([^<]+)</rt></ruby>')
```

### 6.2 Manipulación de HTML y etiquetas Ruby

```python
def output_format(main_text, ruby_content, format_type, char_widths_dict):
    # Genera diferentes formatos según la opción seleccionada
    if format_type == 'HTML格式_Ruby文字_大小调整':
        # Calcula el ratio entre el ancho del texto ruby y el texto principal
        width_ruby = measure_text_width_Arial16(ruby_content, char_widths_dict)
        width_main = measure_text_width_Arial16(main_text, char_widths_dict)
        ratio = width_ruby / width_main
        
        # Ajusta el tamaño según el ratio
        if ratio > 6:
            return f'<ruby>{main_text}<rt class="XXXS_S">{insert_br_at_third_width(ruby_content, char_widths_dict)}</rt></ruby>'
        # ... más condiciones para otros ratios
```

### 6.3 Técnica de eliminación de Ruby redundante

```python
def remove_redundant_ruby_if_identical(text: str) -> str:
    """
    Elimina etiquetas ruby cuando el texto principal y la anotación son idénticos.
    <ruby>xxx<rt>xxx</rt></ruby> → xxx
    """
    def replacer(match: re.Match) -> str:
        group1 = match.group(1)  # Texto principal
        group2 = match.group(2)  # Anotación
        if group1 == group2:
            return group1
        else:
            return match.group(0)  # Mantener original si no son idénticos
            
    return IDENTICAL_RUBY_PATTERN.sub(replacer, text)
```

## 7. Generación de archivos JSON

### 7.1 Proceso de creación de JSON

El proceso para generar un archivo JSON combinado incluye:

1. **Carga y procesamiento del CSV**:
   - Leer correspondencias entre raíces esperanto y traducciones
   - Convertir a diccionario temporal

2. **Aplicación de reglas de prioridad**:
   - Asignar prioridades basadas en longitud de palabra
   - Ajustar para casos especiales (sufijos verbales, etc.)

3. **Expansión de raíces**:
   - Generar variantes con sufijos y prefijos comunes
   - Crear versiones en mayúscula y capitalizada

4. **Aplicación de reglas personalizadas**:
   - Procesar custom_stemming_setting_list para descomposición de raíces
   - Aplicar user_replacement_item_setting_list para sustituciones personalizadas

5. **Generación de las tres listas finales**:
   - Lista para reemplazo global
   - Lista para reemplazo localizado
   - Lista para raíces de 2 caracteres

### 7.2 Estructura de prioridades

Las prioridades de reemplazo se calculan principalmente así:

```python
# Fórmula básica para prioridad
prioridad = longitud_palabra * 10000

# Ajustes para casos especiales
if condicion_especial:
    prioridad += modificador  # Podría ser positivo o negativo
```

Este sistema asegura que:
- Palabras más largas se reemplacen antes que las cortas (evita conflictos)
- Casos especiales tengan la prioridad adecuada
- El orden de reemplazo sea predecible y consistente

### 7.3 Modificación de prioridades para casos especiales

```python
# Ejemplo para raíces verbales con terminaciones
for k1, k2 in verb_suffix_2l_2.items():
    if not i+k1 in pre_replacements_dict_2:
        pre_replacements_dict_3[i+k1] = [j[0]+k2, j[2]+len(k1)*10000-3000]
    # ...
```

Este código ajusta la prioridad para verbos con terminaciones específicas, dándoles una prioridad ligeramente menor que la que tendrían por su longitud total.

## 8. Extensibilidad y personalización

### 8.1 Adición de nuevos formatos de salida

Para agregar un nuevo formato de salida, se requiere:

1. Añadir la opción al diccionario `options` en main.py
2. Implementar el formato en la función `output_format` en esp_replacement_json_make_module.py
3. Manejar cualquier requisito específico en `apply_ruby_html_header_and_footer`

### 8.2 Personalización de reglas de reemplazo

Los usuarios pueden personalizar las reglas de reemplazo mediante:

1. **CSV personalizado**:
   - Crear un archivo CSV con raíces esperanto y traducciones
   - Cargar en la página de generación de JSON

2. **Reglas de descomposición personalizadas**:
   - Crear un JSON con reglas como `["am", "dflt", ["verbo_s1"]]`
   - La estructura indica:
     - "am": raíz de esperanto
     - "dflt": prioridad (o un valor numérico)
     - ["verbo_s1"]: instrucciones especiales (aquí, añadir terminaciones verbales)

3. **Sustituciones personalizadas**:
   - Crear un JSON con reglas como `["esper/ant", "60000", ["o"], "希望/者"]`
   - La estructura indica:
     - "esper/ant": raíz de esperanto dividida
     - "60000": prioridad
     - ["o"]: sufijos a añadir
     - "希望/者": textos de reemplazo para cada parte

### 8.3 Integración con otras herramientas

La aplicación está diseñada para facilitar la integración:

1. **Exportación de resultados**:
   - Los resultados se pueden descargar como HTML o texto
   - El formato HTML es compatible con navegadores estándar

2. **Importación de datos**:
   - Acepta archivos CSV estándar
   - Soporta múltiples formatos de caracteres esperanto

3. **Extensiones potenciales**:
   - El sistema de módulos facilita añadir nuevas funcionalidades
   - El código está estructurado para permitir la adición de nuevos algoritmos de procesamiento

---

Esta guía técnica proporciona una visión detallada del funcionamiento interno de la aplicación. Comprenderla permitirá no solo utilizar la herramienta de manera efectiva, sino también personalizarla y potencialmente extenderla para necesidades específicas.

En la siguiente parte, profundizaremos en ejemplos específicos de código, patrones de diseño utilizados y recomendaciones para modificar o ampliar la aplicación.