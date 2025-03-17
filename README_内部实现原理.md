# Guía Técnica: Funcionamiento Interno de la Herramienta de Reemplazo de Texto en Esperanto

## Índice
1. [Arquitectura general](#arquitectura-general)
2. [Componentes principales](#componentes-principales)
3. [Flujos de trabajo y procesos](#flujos-de-trabajo-y-procesos)
4. [Análisis detallado: main.py](#análisis-detallado-mainpy)
5. [Análisis detallado: Página para generar archivos JSON](#análisis-detallado-página-para-generar-archivos-json)
6. [Análisis detallado: esp_text_replacement_module.py](#análisis-detallado-esp_text_replacement_modulepy)
7. [Análisis detallado: esp_replacement_json_make_module.py](#análisis-detallado-esp_replacement_json_make_modulepy)
8. [Estructuras de datos clave](#estructuras-de-datos-clave)
9. [Procesamiento en paralelo](#procesamiento-en-paralelo)
10. [Optimizaciones implementadas](#optimizaciones-implementadas)

## Arquitectura general

Esta aplicación está construida con Streamlit, un framework para crear aplicaciones web de ciencia de datos y análisis en Python. La arquitectura sigue un patrón modular con una clara separación de responsabilidades:

```
├── main.py                                    # Aplicación principal
├── pages/
│   └── Página para generar archivos JSON...py # Página secundaria
├── esp_text_replacement_module.py             # Módulo de utilidades para reemplazo de texto
├── esp_replacement_json_make_module.py        # Módulo para generar archivos JSON
└── Appの运行に使用する各类文件/                 # Directorio de archivos de recursos
    ├── 占位符(placeholders)*.txt               # Archivos de placeholders
    ├── *.json                                 # Archivos JSON predeterminados
    └── *.csv                                  # Archivos CSV con mapeos esperanto-español/kanji
```

La aplicación está diseñada con dos interfaces principales y dos módulos de soporte:

1. **Interfaz principal** (`main.py`): Proporciona funcionalidades para reemplazar texto en esperanto.
2. **Interfaz secundaria** (`Página para generar...`): Permite generar archivos JSON personalizados.
3. **Módulo de reemplazo** (`esp_text_replacement_module.py`): Contiene las funciones core para reemplazo de texto.
4. **Módulo de generación** (`esp_replacement_json_make_module.py`): Contiene funciones para crear archivos JSON.

## Componentes principales

### 1. Aplicación principal (main.py)

Este componente es el punto de entrada de la aplicación y maneja:

- Carga y gestión de archivos JSON con reglas de reemplazo
- Configuración de parámetros de procesamiento (formatos, opciones de procesamiento en paralelo)
- Procesamiento del texto en esperanto aplicando las reglas de reemplazo
- Visualización de resultados y opciones de descarga

### 2. Generador de archivos JSON (Página para generar...)

Esta página secundaria permite:

- Cargar archivos CSV con pares de palabras esperanto-traducción
- Configurar reglas de descomposición de palabras en esperanto
- Generar un archivo JSON combinado con tres tipos de listas de reemplazo
- Optimizar el proceso mediante procesamiento en paralelo

### 3. Módulo de reemplazo de texto (esp_text_replacement_module.py)

Este módulo contiene funciones especializadas para:

- Conversión entre diferentes formatos de caracteres esperanto (ĉ, cx, c^)
- Procesamiento de marcadores especiales (%, @) para control del reemplazo
- Implementación de reemplazo seguro mediante sistema de placeholders
- Funciones para procesamiento en paralelo de textos extensos

### 4. Módulo de generación de JSON (esp_replacement_json_make_module.py)

Este módulo proporciona funciones para:

- Manipulación de caracteres esperanto y gestión de formatos
- Medición del ancho de texto para ajustar visualización
- Construcción y optimización de estructuras de datos para reglas de reemplazo
- Formateo HTML y generación de anotaciones Ruby

## Flujos de trabajo y procesos

### Flujo principal: Reemplazo de texto en esperanto

1. **Carga de reglas de reemplazo**:
   - Carga del archivo JSON con tres listas principales: global, local y de raíces de 2 caracteres
   - Carga de placeholders para gestión segura de reemplazos

2. **Entrada de texto**:
   - El usuario proporciona texto en esperanto (manual o por archivo)
   - Se preprocesan los caracteres especiales del esperanto

3. **Procesamiento del texto**:
   - Se identifican secciones marcadas con % (no reemplazar) y @ (reemplazo local)
   - Se aplican reemplazos según prioridades predefinidas
   - Se aplica formato al resultado según la configuración seleccionada

4. **Visualización y descarga**:
   - Se muestra el resultado en formato HTML o texto plano
   - Se ofrece la opción de descargar el resultado

### Flujo secundario: Generación de JSON personalizado

1. **Carga de datos fuente**:
   - Carga de CSV con mapeos de raíces esperanto a traducciones/kanji
   - Carga de JSON con reglas de descomposición de palabras

2. **Procesamiento de raíces y reglas**:
   - Generación de diccionarios temporales con raíces esperanto
   - Aplicación de reglas para las diferentes formas gramaticales (verbos, adjetivos, etc.)
   - Construcción de listas de reemplazo con prioridades adecuadas

3. **Creación del JSON final**:
   - Combinación de tres listas principales en un único archivo JSON
   - Exportación del archivo para su uso en la aplicación principal

## Análisis detallado: main.py

La aplicación principal está estructurada en varias secciones clave:

### Importaciones y configuración

El archivo comienza importando las bibliotecas necesarias y configurando el entorno:

```python
import streamlit as st
import re
import io
import json
import pandas as pd
from typing import List, Dict, Tuple, Optional
import streamlit.components.v1 as components
import multiprocessing
```

Se establece el método de inicio para multiprocessing en 'spawn' para evitar errores:

```python
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass
```

Luego, importa funciones específicas del módulo de reemplazo de texto:

```python
from esp_text_replacement_module import (
    x_to_circumflex,
    x_to_hat,
    hat_to_circumflex,
    # ...otras funciones
)
```

### Función para cargar archivos JSON

La función `load_replacements_lists` utiliza el decorador `@st.cache_data` para optimizar el rendimiento mediante caché:

```python
@st.cache_data
def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
    """
    Carga un archivo JSON y devuelve tres listas como una tupla:
    1) replacements_final_list
    2) replacements_list_for_localized_string
    3) replacements_list_for_2char
    """
    # ...código de carga
```

Esta función es crucial porque el archivo JSON puede ser grande (hasta 50MB) y la caché mejora significativamente el rendimiento.

### Interfaz de usuario

La aplicación configura la interfaz con Streamlit:

```python
st.set_page_config(page_title="Herramienta de reemplazo de caracteres (kanji) en texto en esperanto", layout="wide")
st.title("Reemplazo de texto en esperanto por kanjis y/o anotaciones en HTML (versión ampliada)")
```

Luego proporciona opciones para cargar el archivo JSON:

```python
json_options = ["デフォルトを使用する", "アップロードする"]
selected_option = st.radio(
    "¿Cómo manejar el archivo JSON? (lectura del archivo JSON de reemplazo)",
    json_options,
    format_func=lambda x: "Usar valor predeterminado" if x == "デフォルトを使用する" else "Subir archivo"
)
```

Observe el uso inteligente de `format_func` para mostrar etiquetas en español mientras mantiene valores internos en japonés para mantener compatibilidad con otras versiones.

### Carga de listas de reemplazo

Dependiendo de la selección del usuario, la aplicación carga las listas desde un archivo predeterminado o uno subido por el usuario:

```python
if selected_option == "デフォルトを使用する":
    default_json_path = "./Appの运行に使用する各类文件/最终的な替换用リスト(列表)(合并3个JSON文件).json"
    # ... carga el archivo predeterminado
else:
    # ... carga el archivo subido por el usuario
```

### Procesamiento del texto

El núcleo del procesamiento se encuentra dentro del formulario:

```python
with st.form(key='profile_form'):
    # ... configuración de entrada de texto y opciones

    if submit_btn:
        # Guarda el texto en la sesión para persistencia
        st.session_state["text0_value"] = text0

        # Elige entre procesamiento paralelo o secuencial
        if use_parallel:
            processed_text = parallel_process(
                text=text0,
                num_processes=num_processes,
                # ... otros parámetros
            )
        else:
            processed_text = orchestrate_comprehensive_esperanto_text_replacement(
                text=text0,
                # ... otros parámetros
            )

        # Procesa los caracteres especiales según la configuración
        if letter_type == '上付き文字':
            processed_text = replace_esperanto_chars(processed_text, x_to_circumflex)
            processed_text = replace_esperanto_chars(processed_text, hat_to_circumflex)
        elif letter_type == '^形式':
            # ...
```

Finalmente, aplica encabezados y pies de página HTML si es necesario:

```python
processed_text = apply_ruby_html_header_and_footer(processed_text, format_type)
```

### Visualización de resultados

Para mostrar los resultados, la aplicación maneja textos grandes dividiéndolos para vista previa:

```python
if processed_text:
    MAX_PREVIEW_LINES = 250
    lines = processed_text.splitlines()
    if len(lines) > MAX_PREVIEW_LINES:
        # ... lógica para mostrar vista previa limitada
```

Y muestra pestañas diferentes según el formato seleccionado:

```python
if "HTML" in format_type:
    tab1, tab2 = st.tabs(["Vista previa en HTML", "Resultado (código HTML)"])
    with tab1:
        components.html(preview_text, height=500, scrolling=True)
    with tab2:
        st.text_area("Código HTML generado:", preview_text, height=300)
else:
    # ... manejo para formatos no HTML
```

## Análisis detallado: Página para generar archivos JSON

Esta página secundaria es responsable de generar archivos JSON personalizados con reglas de reemplazo.

### Estructura general

La página está organizada en varias secciones principales:

1. **Importaciones y configuración**: Similar a la aplicación principal, importa bibliotecas y funciones necesarias.
2. **Definición de variables globales**: Incluye sufijos verbales, listas AN/ON, y roots de 2 caracteres.
3. **Interfaz de usuario**: Configuración para cargar archivos CSV y JSON.
4. **Procesamiento de datos**: Genera las listas de reemplazo cuando se activa el botón.

### Funcionamiento interno

El proceso de generación de JSON es complejo e incluye estos pasos clave:

1. **Carga de raíces esperanto**: Carga unas 11,137 raíces esperanto para construir el diccionario base.

2. **Aplicación de mapeos CSV**: Utiliza el CSV para aplicar traducciones a las raíces esperanto:

```python
for *, (E*root, hanzi_or_meaning) in CSV_data_imported.iterrows():
    if pd.notna(E_root) and pd.notna(hanzi_or_meaning) \
       and '#' not in E_root and (E_root != '') and (hanzi_or_meaning != ''):
        temporary_replacements_dict[E_root] = [
            output_format(E_root, hanzi_or_meaning, format_type, char_widths_dict),
            len(E_root)
        ]
```

3. **Creación de lista de reemplazos temporales**: Convierte el diccionario en una lista ordenada por longitud de palabra:

```python
temporary_replacements_list_1 = []
for old, new in temporary_replacements_dict.items():
    temporary_replacements_list_1.append((old, new[0], new[1]))
temporary_replacements_list_2 = sorted(temporary_replacements_list_1, key=lambda x: x[2], reverse=True)
```

4. **Construcción de diccionario pre-reemplazo**: Genera un diccionario con todas las formas gramaticales:

```python
if use_parallel:
    pre_replacements_dict_1 = parallel_build_pre_replacements_dict(
        E_stem_with_Part_Of_Speech_list,
        temporary_replacements_list_final,
        num_processes
    )
else:
    # ... construcción secuencial
```

5. **Ajuste de prioridades**: Realiza múltiples ajustes para manejar casos especiales como terminaciones verbales, sufijos "an", "on", etc.

6. **Aplicación de reglas personalizadas**: Aplica reglas de descomposición definidas por el usuario:

```python
for i in custom_stemming_setting_list:
    if len(i)==3:
        try:
            esperanto_Word_before_replacement = i[0].replace('/', '')
            # ... aplicación de reglas
```

7. **Creación de las tres listas finales**:
   - `replacements_final_list`: Para reemplazo global
   - `replacements_list_for_2char`: Para raíces de 2 caracteres
   - `replacements_list_for_localized_string`: Para reemplazo local

8. **Combinación y exportación**: Combina las tres listas en un único JSON:

```python
combined_data = {}
combined_data["全域替换用のリスト(列表)型配列(replacements_final_list)"] = replacements_final_list
combined_data["二文字词根替换用のリスト(列表)型配列(replacements_list_for_2char)"] = replacements_list_for_2char
combined_data["局部文字替换用のリスト(列表)型配列(replacements_list_for_localized_string)"] = replacements_list_for_localized_string
```

## Análisis detallado: esp_text_replacement_module.py

Este módulo es crucial para las operaciones de reemplazo de texto. Contiene varias funciones importantes:

### Diccionarios de conversión de caracteres

El módulo define diccionarios para convertir entre diferentes notaciones de caracteres especiales del esperanto:

```python
x_to_circumflex = {
    'cx': 'ĉ', 'gx': 'ĝ', 'hx': 'ĥ', 'jx': 'ĵ', 'sx': 'ŝ', 'ux': 'ŭ',
    'Cx': 'Ĉ', 'Gx': 'Ĝ', 'Hx': 'Ĥ', 'Jx': 'Ĵ', 'Sx': 'Ŝ', 'Ux': 'Ŭ'
}
# ... otros diccionarios similares
```

### Funciones de conversión

Proporciona funciones para aplicar estas conversiones:

```python
def replace_esperanto_chars(text, char_dict: Dict[str, str]) -> str:
    # Reemplaza caracteres según el diccionario proporcionado
    for original_char, converted_char in char_dict.items():
        text = text.replace(original_char, converted_char)
    return text

def convert_to_circumflex(text: str) -> str:
    """
    Convierte texto a formato de acento circunflejo (ĉ, ĝ, etc.)
    """
    text = replace_esperanto_chars(text, hat_to_circumflex)
    text = replace_esperanto_chars(text, x_to_circumflex)
    return text
```

### Sistema de reemplazo seguro con placeholders

Una de las funciones más importantes es `safe_replace`, que implementa un sistema de reemplazo en dos etapas para evitar conflictos:

```python
def safe_replace(text: str, replacements: List[Tuple[str, str, str]]) -> str:
    """
    Recibe una lista de tuplas (old, new, placeholder) y
    realiza reemplazos text: old → placeholder → new.
    """
    valid_replacements = {}
    # Primero old→placeholder
    for old, new, placeholder in replacements:
        if old in text:
            text = text.replace(old, placeholder)
            valid_replacements[placeholder] = new
    # Luego placeholder→new
    for placeholder, new in valid_replacements.items():
        text = text.replace(placeholder, new)
    return text
```

Este enfoque evita problemas como que un reemplazo afecte a otro o que se procesen partes ya reemplazadas.

### Procesamiento de marcadores especiales

El módulo proporciona funciones para procesar texto con marcadores especiales (% y @):

```python
PERCENT_PATTERN = re.compile(r'%(.{1,50}?)%')
def find_percent_enclosed_strings_for_skipping_replacement(text: str) -> List[str]:
    """Extrae todos los fragmentos de la forma '%foo%'. Limitado a 50 caracteres."""
    # ... implementación
```

### Función principal de reemplazo

La función principal `orchestrate_comprehensive_esperanto_text_replacement` coordina todo el proceso:

```python
def orchestrate_comprehensive_esperanto_text_replacement(
    text,
    placeholders_for_skipping_replacements: List[str],
    replacements_list_for_localized_string: List[Tuple[str, str, str]],
    placeholders_for_localized_replacement: List[str],
    replacements_final_list: List[Tuple[str, str, str]],
    replacements_list_for_2char: List[Tuple[str, str, str]],
    format_type: str
) -> str:
    """
    Función principal que aplica múltiples reglas de reemplazo a texto en esperanto.
    """
    # 1, 2) Normalización de espacios + conversión a formato circunflejo
    text = unify_halfwidth_spaces(text)
    text = convert_to_circumflex(text)

    # 3) Reemplazo temporal de partes %...%
    # ... código para manejar secciones a mantener intactas

    # 4) Reemplazo de secciones @...@
    # ... código para reemplazo localizado

    # 5) Reemplazo global
    # ... código para reemplazo principal

    # 6) Reemplazo de raíces de 2 caracteres (2 pasadas)
    # ... código para procesar raíces cortas

    # 7) Restauración de placeholders a strings finales
    # ... código para restaurar todo en orden correcto

    # 8) Formato HTML si es necesario
    if "HTML" in format_type:
        # ... código para formateo HTML

    return text
```

### Procesamiento en paralelo

Para textos grandes, el módulo ofrece funciones de procesamiento en paralelo:

```python
def parallel_process(
    text: str,
    num_processes: int,
    # ... otros parámetros
) -> str:
    """
    Divide el texto en líneas y procesa en paralelo usando multiprocessing.
    """
    # ... implementación
```

## Análisis detallado: esp_replacement_json_make_module.py

Este módulo se especializa en la creación de archivos JSON de reemplazo y contiene varias funciones clave:

### Funciones de conversión de caracteres

Similar al módulo de reemplazo, define diccionarios y funciones para convertir caracteres esperanto:

```python
def replace_esperanto_chars(text, char_dict: Dict[str, str]) -> str:
    # ... similar al otro módulo
```

### Medición de ancho de texto

Proporciona funciones para medir el ancho de texto en píxeles, crucial para el formato Ruby:

```python
def measure_text_width_Arial16(text, char_widths_dict: Dict[str, int]) -> int:
    """
    Calcula el ancho total de un texto usando un diccionario de anchos de caracteres
    """
    total_width = 0
    for ch in text:
        char_width = char_widths_dict.get(ch, 8)
        total_width += char_width
    return total_width
```

### Formateo de salida

La función `output_format` es esencial para generar diferentes formatos de salida:

```python
def output_format(main_text, ruby_content, format_type, char_widths_dict):
    """
    Formatea texto esperanto (main_text) y su traducción (ruby_content)
    según el formato especificado
    """
    if format_type == 'HTML格式_Ruby文字_大小调整':
        # Calcula la proporción de anchos
        width_ruby = measure_text_width_Arial16(ruby_content, char_widths_dict)
        width_main = measure_text_width_Arial16(main_text, char_widths_dict)
        ratio_1 = width_ruby / width_main

        # Ajusta el tamaño de ruby según la proporción
        if ratio_1 > 6:
            return f'<ruby>{main_text}<rt class="XXXS_S">{insert_br_at_third_width(ruby_content, char_widths_dict)}</rt></ruby>'
        # ... más condiciones para diferentes tamaños

    elif format_type == 'HTML格式_Ruby文字_大小调整_汉字替换':
        # Similar pero invirtiendo main_text y ruby_content
        # ...

    elif format_type == 'HTML格式':
        return f'<ruby>{main_text}<rt>{ruby_content}</rt></ruby>'

    # ... otros formatos
```

### Optimización de las etiquetas Ruby

El módulo incluye funciones para optimizar y corregir el formato Ruby HTML:

```python
def capitalize_ruby_and_rt(text: str) -> str:
    """
    Capitaliza tanto el texto padre como el ruby dentro de etiquetas <ruby>
    """
    # ... implementación con regex
```

```python
def remove_redundant_ruby_if_identical(text: str) -> str:
    """
    Elimina etiquetas ruby cuando el texto padre y el ruby son idénticos
    """
    # ... implementación
```

### Construcción de diccionario en paralelo

Para mejorar el rendimiento durante la generación de JSON, ofrece funciones de procesamiento en paralelo:

```python
def parallel_build_pre_replacements_dict(
    E_stem_with_Part_Of_Speech_list: List[List[str]],
    replacements: List[Tuple[str, str, str]],
    num_processes: int = 4
) -> Dict[str, List[str]]:
    """
    Divide los datos en chunks y construye diccionarios en paralelo
    """
    # ... implementación
```

## Estructuras de datos clave

### 1. Listas de reemplazo

La aplicación utiliza tres listas principales de reemplazo:

1. **replacements_final_list**: Para reemplazo global de palabras
   - Formato: `[(original, reemplazo, placeholder), ...]`
   - Ordenada por longitud de palabra (más largas primero)

2. **replacements_list_for_2char**: Para raíces de 2 caracteres
   - Formato: `[(original, reemplazo, placeholder), ...]`
   - Contiene prefijos, sufijos y palabras independientes

3. **replacements_list_for_localized_string**: Para reemplazo dentro de marcadores @
   - Formato: `[(original, reemplazo, placeholder), ...]`
   - Aplicada solo a texto dentro de marcadores @...@

### 2. Tuplas de formato

En estas listas, cada ítem es una tupla con tres elementos:
- `original`: La palabra esperanto original
- `reemplazo`: El texto de reemplazo formateado (HTML, paréntesis, etc.)
- `placeholder`: Un texto único usado temporalmente durante el proceso de reemplazo

### 3. Diccionarios de mapeo

Durante el procesamiento, se utilizan varios diccionarios:

1. **temporary_replacements_dict**: Mapeo inicial de raíces esperanto a traducciones
   - Clave: raíz esperanto
   - Valor: `[texto_reemplazo, longitud]`

2. **pre_replacements_dict_1**: Contiene todas las formas gramaticales
   - Clave: palabra esperanto
   - Valor: `[texto_reemplazo, info_gramatical]`

3. **pre_replacements_dict_3**: Diccionario con prioridades
   - Clave: palabra esperanto
   - Valor: `[texto_reemplazo, prioridad]`

### 4. Listas de placeholders

Se utilizan varios conjuntos de placeholders:
- **placeholders_for_skipping_replacements**: Para texto entre %...%
- **placeholders_for_localized_replacement**: Para texto entre @...@
- **imported_placeholders_for_global_replacement**: Para reemplazos globales
- **imported_placeholders_for_2char_replacement**: Para raíces de 2 caracteres

## Procesamiento en paralelo

La aplicación implementa procesamiento en paralelo en dos lugares clave:

### 1. Procesamiento de texto en la aplicación principal

```python
def parallel_process(text, num_processes, ...):
    # Divide el texto en líneas
    lines = re.findall(r'.*?\n|.+$', text)
    # Calcula cuántas líneas por proceso
    lines_per_process = max(num_lines // num_processes, 1)
    # Asigna rangos
    ranges = [(i * lines_per_process, (i + 1) * lines_per_process) for i in range(num_processes)]
    # Ajusta el último rango
    ranges[-1] = (ranges[-1][0], num_lines)

    # Procesa en paralelo
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(
            process_segment,
            [
                (lines[start:end], ...) for (start, end) in ranges
            ]
        )
    return ''.join(results)
```

### 2. Generación de diccionario en la página secundaria

```python
def parallel_build_pre_replacements_dict(...):
    # ... divide los datos en chunks
    with multiprocessing.Pool(num_processes) as pool:
        partial_dicts = pool.starmap(
            process_chunk_for_pre_replacements,
            [(chunk, replacements) for chunk in chunks]
        )

    # Combina los resultados
    merged_dict = {}
    for partial_d in partial_dicts:
        # ... código para combinar diccionarios
    return merged_dict
```

## Optimizaciones implementadas

### 1. Caché de datos con Streamlit

El uso de `@st.cache_data` optimiza la carga de archivos JSON grandes:

```python
@st.cache_data
def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
    # ... evita recargar el mismo archivo
```

### 2. Sistema de reemplazo en dos etapas

El enfoque de `old → placeholder → new` evita conflictos durante los reemplazos:

```python
# Primero old→placeholder
for old, new, placeholder in replacements:
    text = text.replace(old, placeholder)
    valid_replacements[placeholder] = new

# Luego placeholder→new
for placeholder, new in valid_replacements.items():
    text = text.replace(placeholder, new)
```

### 3. Orden de reemplazo por longitud

Los reemplazos se ordenan por longitud (más largos primero) para evitar sustituciones parciales:

```python
temporary_replacements_list_2 = sorted(temporary_replacements_list_1, key=lambda x: x[2], reverse=True)
```

### 4. Priorización de formas gramaticales

El sistema asigna diferentes prioridades a formas gramaticales:

```python
# Por ejemplo, para verbos:
if "动词" in j[1]:
    for k1,k2 in verb_suffix_2l_2.items():
        pre_replacements_dict_3[i+k1]=[j[0]+k2,j[2]+len(k1)*10000-3000]
```

### 5. Tratamiento especial para raíces de 2 caracteres

Las raíces cortas requieren manejo especial para evitar conflictos, por lo que se procesan en pasadas separadas:

```python
# Primera pasada
for old, new, placeholder in replacements_list_for_2char:
    if old in text:
        text = text.replace(old, placeholder)
        valid_replacements_for_2char_roots[placeholder] = new

# Segunda pasada
for old, new, placeholder in replacements_list_for_2char:
    if old in text:
        place_holder_second = "!" + placeholder + "!"
        text = text.replace(old, place_holder_second)
        valid_replacements_for_2char_roots_2[place_holder_second] = new
```

### 6. Ajuste automático de tamaño para anotaciones Ruby

El sistema mide el ancho relativo del texto y las anotaciones para ajustar automáticamente el tamaño:

```python
width_ruby = measure_text_width_Arial16(ruby_content, char_widths_dict)
width_main = measure_text_width_Arial16(main_text, char_widths_dict)
ratio_1 = width_ruby / width_main

if ratio_1 > 6:
    # Texto ruby muy largo en comparación con el texto principal
    return f'<ruby>{main_text}<rt class="XXXS_S">{insert_br_at_third_width(ruby_content, char_widths_dict)}</rt></ruby>'
```

### 7. Vista previa limitada para textos grandes

Para mantener el rendimiento con textos extensos, se limita la vista previa:

```python
if len(lines) > MAX_PREVIEW_LINES:
    first_part = lines[:247]
    last_part = lines[-3:]
    preview_text = "\n".join(first_part) + "\n...\n" + "\n".join(last_part)
```

Este análisis detallado muestra la sofisticada arquitectura y las técnicas de programación implementadas en esta aplicación Streamlit para procesamiento de texto en esperanto.
