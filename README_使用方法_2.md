# Manual de Usuario: Herramienta de Reemplazo de Caracteres (Kanji) en Texto en Esperanto

## Índice
- [Manual de Usuario: Herramienta de Reemplazo de Caracteres (Kanji) en Texto en Esperanto](#manual-de-usuario-herramienta-de-reemplazo-de-caracteres-kanji-en-texto-en-esperanto)
  - [Índice](#índice)
  - [Introducción](#introducción)
  - [Instalación y acceso](#instalación-y-acceso)
  - [Página principal - Reemplazo de texto](#página-principal---reemplazo-de-texto)
    - [Configuración del archivo JSON](#configuración-del-archivo-json)
    - [Configuración avanzada](#configuración-avanzada)
    - [Selección del formato de salida](#selección-del-formato-de-salida)
    - [Entrada de texto](#entrada-de-texto)
    - [Procesamiento del texto](#procesamiento-del-texto)
    - [Visualización y descarga de resultados](#visualización-y-descarga-de-resultados)
  - [Página de generación de archivos JSON](#página-de-generación-de-archivos-json)
    - [Preparación del archivo CSV](#preparación-del-archivo-csv)
    - [Configuración de archivos JSON complementarios](#configuración-de-archivos-json-complementarios)
    - [Creación del archivo JSON final](#creación-del-archivo-json-final)
  - [Características especiales](#características-especiales)
    - [Marcadores de preservación con %...%](#marcadores-de-preservación-con-)
    - [Marcadores de reemplazo local con @...@](#marcadores-de-reemplazo-local-con-)
    - [Formatos de caracteres esperanto](#formatos-de-caracteres-esperanto)
  - [Ejemplos de uso](#ejemplos-de-uso)
    - [Ejemplo 1: Reemplazo simple de texto en esperanto](#ejemplo-1-reemplazo-simple-de-texto-en-esperanto)
    - [Ejemplo 2: Usando marcadores especiales](#ejemplo-2-usando-marcadores-especiales)
    - [Ejemplo 3: Creación de un archivo JSON personalizado](#ejemplo-3-creación-de-un-archivo-json-personalizado)
  - [Solución de problemas comunes](#solución-de-problemas-comunes)
    - [No se ve ningún cambio en el texto procesado](#no-se-ve-ningún-cambio-en-el-texto-procesado)
    - [El archivo JSON no se carga correctamente](#el-archivo-json-no-se-carga-correctamente)
    - [El procesamiento es demasiado lento](#el-procesamiento-es-demasiado-lento)
    - [Las anotaciones no se muestran correctamente](#las-anotaciones-no-se-muestran-correctamente)
  - [Versiones en otros idiomas](#versiones-en-otros-idiomas)

## Introducción

Esta aplicación es una herramienta especializada para convertir texto en esperanto, sustituyendo palabras o raíces con caracteres kanji, anotaciones ruby HTML u otros formatos de texto. Permite visualizar textos en esperanto con anotaciones que facilitan su comprensión para hablantes de español u otros idiomas. 

La herramienta ofrece varias opciones de formato de salida, incluyendo:
- Formato HTML con anotaciones ruby (pequeño texto explicativo sobre los caracteres)
- Formato con paréntesis (mostrando las traducciones entre paréntesis)
- Reemplazo simple de texto

## Instalación y acceso

No es necesario instalar la aplicación localmente, ya que está alojada en Streamlit Cloud. Para acceder a ella:

1. Abra su navegador web y visite la URL:
   ```
   https://esperanto-kanji-converter-and-ruby-annotation-tool-spanish.streamlit.app/
   ```

2. La aplicación se cargará directamente en su navegador y estará lista para usar.

3. Para acceder a la página de generación de archivos JSON, utilice el menú desplegable en la esquina superior izquierda de la aplicación.

## Página principal - Reemplazo de texto

La página principal permite convertir texto en esperanto utilizando archivos JSON con reglas de reemplazo predefinidas.

### Configuración del archivo JSON

El primer paso es seleccionar el archivo JSON que contiene las reglas de reemplazo:

1. Seleccione una de las opciones:
   - **Usar valor predeterminado**: Utiliza el archivo JSON incorporado en la aplicación.
   - **Subir archivo**: Permite cargar su propio archivo JSON personalizado.

2. Si selecciona "Subir archivo", utilice el botón para seleccionar su archivo JSON.

3. Para obtener un archivo JSON de ejemplo, puede expandir la sección "Descargar archivo JSON de ejemplo" y hacer clic en el botón correspondiente.

### Configuración avanzada

La aplicación ofrece opciones de procesamiento en paralelo para archivos de texto grandes:

1. Expanda la sección "Abrir configuración de procesamiento en paralelo".

2. Active la casilla "Usar procesamiento en paralelo" si desea acelerar el procesamiento de textos extensos.

3. Ajuste el "Número de procesos simultáneos" según la capacidad de su dispositivo (valores típicos: 2-4).

### Selección del formato de salida

Seleccione el formato de salida deseado del menú desplegable:

- **Formato HTML con anotaciones (ruby) y ajuste de tamaño**: Muestra el texto original con anotaciones pequeñas encima y ajusta automáticamente el tamaño.
- **Formato HTML con anotaciones (ruby), ajuste de tamaño y reemplazo de kanji**: Similar al anterior, pero intercambia la posición del texto original y las anotaciones.
- **Formato HTML**: Formato HTML básico con anotaciones.
- **Formato HTML con reemplazo de kanji**: Formato HTML donde el texto original se reemplaza con kanji.
- **Formato con paréntesis**: Muestra las anotaciones entre paréntesis.
- **Formato con paréntesis y reemplazo de kanji**: Similar al anterior, pero intercambiando la posición.
- **Sólo texto reemplazado**: Realiza un reemplazo simple mostrando sólo el texto traducido.

### Entrada de texto

Existen dos formas de proporcionar el texto en esperanto:

1. **Entrada manual**: Escriba o pegue directamente el texto en el área de texto.
2. **Subir archivo**: Cargue un archivo de texto (UTF-8) con el contenido en esperanto.

Importante: Si elige subir un archivo, primero seleccione "Subir archivo" en el selector de fuente de texto y luego use el botón para cargar su archivo.

### Procesamiento del texto

Una vez configuradas las opciones y proporcionado el texto:

1. Seleccione la forma de mostrar los caracteres especiales del esperanto en el resultado:
   - **Signo de acento sobre la letra** (ĉ → c + ˆ)
   - **Formato con x** (ĉ → cx)
   - **Formato con ^** (ĉ → c^)

2. Haga clic en el botón "Enviar" para procesar el texto.

3. Si desea cancelar la operación, puede hacer clic en "Cancelar".

### Visualización y descarga de resultados

Después de procesar el texto, los resultados se mostrarán en la pantalla:

1. Para formatos HTML, se mostrarán dos pestañas:
   - **Vista previa en HTML**: Muestra el resultado renderizado.
   - **Resultado (código HTML)**: Muestra el código HTML generado.

2. Para otros formatos, se mostrará una pestaña con el texto resultante.

3. Para guardar el resultado, haga clic en el botón "Descargar resultado".

## Página de generación de archivos JSON

Esta página permite crear sus propios archivos JSON de reglas de reemplazo personalizadas para usar en la página principal.

### Preparación del archivo CSV

El primer paso es preparar el archivo CSV con las correspondencias entre raíces en esperanto y sus traducciones:

1. Seleccione una opción:
   - **Subir un archivo CSV**: Cargue su propio archivo CSV personalizado.
   - **Usar archivo por defecto**: Utilice el archivo CSV incorporado en la aplicación.

2. Si selecciona "Subir un archivo CSV", utilice el botón para cargar su archivo.

3. Puede descargar ejemplos de archivos CSV desde la sección expandible "Lista de archivos de ejemplo".

Formato del CSV:
- Primera columna: Raíces en esperanto
- Segunda columna: Traducciones al español o caracteres kanji

### Configuración de archivos JSON complementarios

A continuación, configure los archivos JSON que definen las reglas de descomposición y reemplazo:

1. Para el archivo JSON de descomposición de raíces:
   - Seleccione "Subir un archivo JSON" o "Usar archivo por defecto".
   - Si sube un archivo, asegúrese de que tenga el formato correcto.

2. Para el archivo JSON de texto de sustitución:
   - Seleccione "Subir un archivo JSON" o "Usar archivo por defecto".
   - Normalmente, el archivo por defecto es suficiente.

3. Puede descargar ejemplos de estos archivos JSON desde la sección de archivos de ejemplo.

### Creación del archivo JSON final

Una vez configurados los archivos de entrada:

1. Configure las opciones de procesamiento en paralelo si lo desea.

2. Haga clic en el botón "Crear archivo JSON para la sustitución".

3. Espere a que se complete el procesamiento (puede tardar varios minutos para archivos grandes).

4. Una vez completado, haga clic en "Descargar la lista final de sustitución" para guardar el archivo JSON generado.

5. Este archivo JSON descargado puede utilizarse en la página principal para realizar reemplazos personalizados.

## Características especiales

### Marcadores de preservación con %...%

Si desea preservar ciertas partes del texto sin que sean reemplazadas:

1. Encierre la parte del texto que desea preservar entre signos de porcentaje: `%texto a preservar%`

2. Esta parte del texto se mantendrá exactamente igual en el resultado final, sin ser procesada por las reglas de reemplazo.

3. Útil para nombres propios, términos técnicos o cualquier texto que desee mantener inalterado.

4. Limitación: El texto entre los signos % no debe exceder los 50 caracteres.

### Marcadores de reemplazo local con @...@

Si desea aplicar reglas de reemplazo específicas solo a ciertas partes del texto:

1. Encierre la parte del texto que desea reemplazar localmente entre signos de arroba: `@texto para reemplazo local@`

2. Solo esta parte específica será procesada con las reglas de reemplazo.

3. Útil cuando desea controlar exactamente qué partes del texto se reemplazan.

4. Limitación: El texto entre los signos @ no debe exceder los 18 caracteres.

### Formatos de caracteres esperanto

El esperanto utiliza caracteres especiales (ĉ, ĝ, ĥ, ĵ, ŝ, ŭ) que pueden representarse de diferentes maneras:

1. **Signo de acento sobre la letra**: Los caracteres aparecen con sus acentos: ĉ, ĝ, ĥ, etc.

2. **Formato con x**: Los caracteres se representan añadiendo una x: cx, gx, hx, etc.

3. **Formato con ^**: Los caracteres se representan añadiendo un circunflejo: c^, g^, h^, etc.

La aplicación puede manejar cualquiera de estos formatos en el texto de entrada y convertirlos al formato seleccionado en la salida.

## Ejemplos de uso

### Ejemplo 1: Reemplazo simple de texto en esperanto

1. En la página principal, seleccione "Usar valor predeterminado" para el archivo JSON.
2. Seleccione "Formato HTML con anotaciones (ruby) y ajuste de tamaño" como formato de salida.
3. En la sección de entrada de texto, escriba o pegue el siguiente texto en esperanto:
   ```
   La suno brilas en la ĉielo. Ĝi estas varma hodiaŭ.
   ```
4. Seleccione "Signo de acento sobre la letra" como formato de caracteres.
5. Haga clic en "Enviar".
6. Observe el resultado con anotaciones ruby sobre las palabras en esperanto.

### Ejemplo 2: Usando marcadores especiales

1. Configure la aplicación como en el ejemplo anterior.
2. En la sección de entrada de texto, escriba:
   ```
   Mi loĝas en %Madrid%. La tempo estas @bela@ hodiaŭ.
   ```
3. Haga clic en "Enviar".
4. Observe cómo "Madrid" permanece sin cambios y "bela" recibe un tratamiento especial de reemplazo.

### Ejemplo 3: Creación de un archivo JSON personalizado

1. Prepare un archivo CSV con sus propias correspondencias de raíces en esperanto y traducciones.
2. En la página de generación de archivos JSON, cargue su archivo CSV.
3. Use los archivos JSON por defecto para las reglas de descomposición y reemplazo.
4. Haga clic en "Crear archivo JSON para la sustitución".
5. Descargue el archivo JSON generado.
6. Regrese a la página principal y use este archivo JSON personalizado seleccionando "Subir archivo".

## Solución de problemas comunes

### No se ve ningún cambio en el texto procesado

- Verifique que el archivo JSON de reemplazo contenga correspondencias para las palabras en su texto.
- Asegúrese de que está utilizando el formato de salida correcto.
- Compruebe que no hay errores en la carga de archivos (mensajes en rojo).

### El archivo JSON no se carga correctamente

- Asegúrese de que el archivo JSON tiene el formato correcto.
- Verifique que el archivo no excede el tamaño máximo permitido.
- Intente usar el archivo JSON por defecto para comparar.

### El procesamiento es demasiado lento

- Active el procesamiento en paralelo en la configuración avanzada.
- Aumente el número de procesos simultáneos (si su dispositivo lo permite).
- Para textos muy grandes, considere dividirlos en partes más pequeñas.

### Las anotaciones no se muestran correctamente

- Asegúrese de usar un navegador moderno que soporte HTML5.
- Verifique que el formato de salida seleccionado es el adecuado para sus necesidades.
- Descargue el resultado y ábralo en otro navegador o editor HTML.

## Versiones en otros idiomas

Esta aplicación está disponible en varios idiomas. Puede acceder a estas versiones a través de los enlaces disponibles al final de la página principal:

- Esperanto: `https://esperanto-kanji-converter-and-ruby-annotation-tool-esperanto.streamlit.app/`
- English: `https://esperanto-kanji-converter-and-ruby-annotation-tool-english.streamlit.app/`
- 日本語: `https://esperanto-kanji-converter-and-ruby-annotation-tool.streamlit.app/`
- 中文: `https://esperanto-hanzi-converter-and-ruby-annotation-tool-chinese-dgw.streamlit.app/`
- 한국어: `https://esperanto-kanji-converter-and-ruby-annotation-tool-korean-yrrx.streamlit.app/`
- Русский: `https://esperanto-kanji-converter-and-ruby-annotation-tool-russian.streamlit.app/`
- Español: `https://esperanto-kanji-converter-and-ruby-annotation-tool-spanish.streamlit.app/`
- Italiano: `https://esperanto-kanji-converter-and-ruby-annotation-tool-italian.streamlit.app/`
- Français: `https://esperanto-kanji-converter-and-ruby-annotation-tool-french.streamlit.app/`
- Deutsch: `https://esperanto-kanji-converter-and-ruby-annotation-tool-german.streamlit.app/`
- العربية: `https://esperanto-kanji-converter-and-ruby-annotation-tool-arabic.streamlit.app/`
- हिन्दी: `https://esperanto-kanji-converter-and-ruby-annotation-tool-hindi.streamlit.app/`
- Polski: `https://esperanto-kanji-converter-and-ruby-annotation-tool-polish.streamlit.app/`
- Tiếng Việt: `https://esperanto-kanji-converter-and-ruby-annotation-tool-vietnamese.streamlit.app/`
- Bahasa Indonesia: `https://esperanto-kanji-converter-and-ruby-annotation-tool-indonesian.streamlit.app/`

También puede encontrar documentación adicional y código fuente en los repositorios de GitHub listados al final de la página principal.