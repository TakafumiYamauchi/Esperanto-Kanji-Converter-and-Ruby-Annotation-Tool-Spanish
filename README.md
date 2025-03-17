# Manual de Usuario: Herramienta de Reemplazo de Caracteres en Texto Esperanto

## Índice
1. [Introducción](#introducción)
2. [Funcionalidades principales](#funcionalidades-principales)
3. [Página principal: Reemplazo de texto](#página-principal-reemplazo-de-texto)
   - [Carga del archivo JSON](#carga-del-archivo-json)
   - [Configuración avanzada](#configuración-avanzada)
   - [Selección del formato de salida](#selección-del-formato-de-salida)
   - [Entrada de texto](#entrada-de-texto)
   - [Visualización y descarga de resultados](#visualización-y-descarga-de-resultados)
4. [Marcadores especiales en el texto](#marcadores-especiales-en-el-texto)
5. [Página secundaria: Generación de archivos JSON](#página-secundaria-generación-de-archivos-json)
   - [Preparación del archivo CSV](#preparación-del-archivo-csv)
   - [Preparación de los archivos JSON](#preparación-de-los-archivos-json)
   - [Creación del archivo JSON combinado](#creación-del-archivo-json-combinado)
6. [Ejemplos prácticos](#ejemplos-prácticos)
7. [Solución de problemas comunes](#solución-de-problemas-comunes)
8. [Enlaces a otras versiones](#enlaces-a-otras-versiones)

## Introducción

Esta aplicación es una herramienta especializada para el procesamiento de textos en esperanto que permite sustituir palabras o raíces del esperanto por caracteres kanji o traducciones en español, añadiendo opcionalmente anotaciones que facilitan la comprensión del texto original. La herramienta ofrece múltiples formatos de visualización y opciones de personalización avanzadas.

La aplicación consta de dos partes principales:
- **Página principal**: donde se realiza el reemplazo de texto en esperanto
- **Página secundaria**: para generar archivos JSON personalizados con reglas de sustitución

Esta herramienta resulta especialmente útil para:
- Estudiantes que aprenden esperanto y desean visualizar traducciones
- Profesores que crean materiales didácticos con anotaciones
- Investigadores que trabajan con textos en esperanto y necesitan referencias
- Cualquier persona interesada en la visualización alternativa de textos en esperanto

## Funcionalidades principales

- Reemplazo de texto en esperanto por caracteres kanji o traducciones en español
- Múltiples formatos de visualización (HTML con anotaciones Ruby, formato con paréntesis, etc.)
- Personalización del tamaño y apariencia de las anotaciones
- Marcado de secciones específicas del texto para excluirlas del reemplazo o aplicar reglas especiales
- Procesamiento en paralelo para textos extensos
- Creación de archivos de reglas de sustitución personalizados

## Página principal: Reemplazo de texto

La página principal es donde se realiza el proceso de sustitución de texto en esperanto. A continuación se detallan los pasos para utilizar correctamente esta funcionalidad.

### Carga del archivo JSON

El primer paso es seleccionar el archivo JSON que contiene las reglas de sustitución:

1. En la sección superior, encontrará la opción "¿Cómo manejar el archivo JSON?" con dos alternativas:
   - **Usar valor predeterminado**: utiliza el archivo JSON incorporado en la aplicación
   - **Subir archivo**: permite cargar un archivo JSON personalizado

2. Si selecciona "Subir archivo", aparecerá un botón para seleccionar el archivo desde su dispositivo.

3. Para descargar un archivo JSON de ejemplo que puede modificar, haga clic en "Descargar archivo JSON de ejemplo" dentro de la sección expandible correspondiente.

**Nota**: El archivo JSON debe contener tres listas específicas de reglas de sustitución. Si no está familiarizado con este formato, se recomienda utilizar la página secundaria para generar el archivo correctamente.

### Configuración avanzada

En la sección "Configuración avanzada" puede activar el procesamiento en paralelo para mejorar el rendimiento con textos extensos:

1. Haga clic en "Abrir configuración de procesamiento en paralelo" para expandir las opciones.
2. Marque la casilla "Usar procesamiento en paralelo" si desea activar esta función.
3. Ajuste el número de procesos simultáneos (de 2 a 4) según las capacidades de su sistema.

**Recomendación**: Active el procesamiento en paralelo solo cuando trabaje con textos muy extensos (más de 1000 palabras).

### Selección del formato de salida

La aplicación ofrece diversos formatos para presentar el texto procesado:

1. En el menú desplegable "Seleccione el formato de salida", elija una de estas opciones:
   - **Formato HTML con anotaciones (ruby) y ajuste de tamaño**: muestra el texto original con traducciones/kanji como anotaciones pequeñas encima, ajustando automáticamente el tamaño
   - **Formato HTML con anotaciones (ruby), ajuste de tamaño y reemplazo de kanji**: similar al anterior pero invirtiendo la posición (kanji como texto principal)
   - **Formato HTML**: formato HTML básico con anotaciones de tamaño fijo
   - **Formato HTML con reemplazo de kanji**: formato HTML con kanji como texto principal
   - **Formato con paréntesis**: muestra el texto original seguido de la traducción entre paréntesis
   - **Formato con paréntesis y reemplazo de kanji**: muestra la traducción seguida del texto original entre paréntesis
   - **Sólo texto reemplazado**: muestra únicamente las traducciones/kanji, sin el texto original

**Importante**: El formato seleccionado debe ser compatible con el archivo JSON de sustitución que esté utilizando.

### Entrada de texto

Puede ingresar el texto en esperanto de dos maneras:

1. En "Fuente del texto de entrada", seleccione:
   - **Entrada manual**: para escribir o pegar directamente el texto
   - **Subir archivo**: para cargar un archivo de texto (UTF-8)

2. Si elige "Subir archivo", haga clic en el botón correspondiente para seleccionar el archivo desde su dispositivo.

3. El texto aparecerá en el área de texto principal, donde podrá editarlo si es necesario.

4. En la parte inferior del formulario, seleccione cómo desea mostrar los caracteres especiales del esperanto en el resultado:
   - **Signo de acento sobre la letra** (ĉ → c + ˆ)
   - **Formato con x** (ĉ → cx)
   - **Formato con ^** (ĉ → c^)

5. Haga clic en "Enviar" para procesar el texto.

### Visualización y descarga de resultados

Una vez procesado el texto, se mostrará el resultado:

1. Si ha elegido un formato HTML, verá dos pestañas:
   - **Vista previa en HTML**: muestra el resultado visual con las anotaciones
   - **Resultado (código HTML)**: muestra el código HTML generado

2. Si ha elegido otro formato, verá una pestaña "Texto resultante" con el texto procesado.

3. Para guardar el resultado, haga clic en "Descargar resultado". Se descargará un archivo con el texto procesado.

**Nota**: Si el texto es muy extenso, la aplicación mostrará una vista previa limitada (primeras 247 líneas y últimas 3), pero el archivo descargado contendrá el texto completo.

## Marcadores especiales en el texto

La aplicación permite marcar partes específicas del texto para aplicar reglas especiales:

### Marcar texto para evitar sustitución

Si desea que ciertas partes del texto se mantengan sin cambios (no se sustituyan), puede encerrarlas entre signos **%**:

```
La vorto %superjaro% ne estos anstataŭigita.
```

En este ejemplo, la palabra "superjaro" permanecerá sin cambios en el resultado final, mientras que el resto del texto se procesará normalmente.

### Marcar texto para sustitución localizada

Si desea que ciertas partes del texto tengan un tratamiento especial (sustitución localizada), puede encerrarlas entre signos **@**:

```
Mi lernas @esperanto@ kaj mi ŝatas ĝin.
```

En este ejemplo, la palabra "esperanto" se sustituirá según reglas específicas para esa sección, que pueden ser diferentes de las reglas generales.

**Limitaciones**:
- El texto entre % puede tener hasta 50 caracteres
- El texto entre @ puede tener hasta 18 caracteres

## Página secundaria: Generación de archivos JSON

La página secundaria permite crear archivos JSON personalizados con reglas de sustitución. Estos archivos se pueden utilizar luego en la página principal.

### Preparación del archivo CSV

El primer paso es preparar o seleccionar un archivo CSV que contenga las correspondencias entre raíces en esperanto y sus traducciones:

1. En "Paso 1: Preparar el archivo CSV", seleccione:
   - **Subir un archivo CSV**: para cargar su propio archivo
   - **Usar archivo por defecto**: para utilizar el archivo incorporado en la aplicación

2. Si elige subir un archivo, debe tener el siguiente formato:
   - Primera columna: raíces en esperanto
   - Segunda columna: traducciones al español o caracteres kanji

3. Puede descargar varios archivos CSV de ejemplo desde la sección expandible "Lista de archivos de ejemplo".

### Preparación de los archivos JSON

A continuación, debe preparar o seleccionar archivos JSON que definan las reglas de descomposición y sustitución:

1. En "Paso 2: Preparar el/los archivo(s) JSON", hay dos secciones:
   - Archivo JSON que define la descomposición de raíces esperanto
   - Archivo JSON que define el texto de sustitución

2. Para cada sección, seleccione si desea subir un archivo personalizado o usar el archivo por defecto.

3. Puede descargar ejemplos de estos archivos desde la sección "Lista de archivos de ejemplo".

### Creación del archivo JSON combinado

Una vez preparados los archivos de entrada, puede generar el archivo JSON combinado:

1. En la sección "Configuración avanzada", puede activar el procesamiento en paralelo para acelerar la generación (recomendado para archivos grandes).

2. Haga clic en "Crear archivo JSON para la sustitución".

3. Espere mientras la aplicación procesa los datos. Este proceso puede tomar desde unos segundos hasta varios minutos, dependiendo del tamaño de los archivos.

4. Una vez completado, aparecerá un botón "Descargar la lista final de sustitución". Haga clic para guardar el archivo JSON generado.

5. Este archivo descargado podrá utilizarlo en la página principal, seleccionando la opción "Subir archivo" en la sección de carga del archivo JSON.

## Ejemplos prácticos

### Ejemplo 1: Texto simple con anotaciones

Para un texto sencillo como:
```
Mi lernas esperanton.
```

1. Seleccione "Usar valor predeterminado" para el archivo JSON
2. Elija "Formato HTML con anotaciones (ruby) y ajuste de tamaño"
3. Ingrese el texto en el área de texto
4. Haga clic en "Enviar"

El resultado mostrará el texto original con anotaciones encima de cada palabra, mostrando su traducción.

### Ejemplo 2: Texto con secciones excluidas

Para un texto donde quiera mantener algunas partes sin cambios:
```
Mi lernas %esperanton% kaj mi ŝatas ĝin.
```

Siguiendo los mismos pasos del ejemplo anterior, todas las palabras excepto "esperanton" serán procesadas.

### Ejemplo 3: Creación de un archivo JSON personalizado

Si desea crear reglas personalizadas para términos técnicos específicos:

1. Cree un archivo CSV con dos columnas: términos en esperanto y sus traducciones
2. En la página secundaria, seleccione "Subir un archivo CSV" y cargue su archivo
3. Use los archivos JSON por defecto para las reglas de descomposición
4. Haga clic en "Crear archivo JSON para la sustitución"
5. Descargue el archivo JSON generado
6. En la página principal, seleccione "Subir archivo" y cargue el archivo JSON que acaba de crear
7. Procese su texto como en los ejemplos anteriores

## Solución de problemas comunes

### El texto no se procesa correctamente

- Verifique que el formato de los caracteres especiales del esperanto sea consistente (ĉ, ĝ, ŝ, etc.)
- Asegúrese de que el archivo JSON contiene las reglas para las palabras que está utilizando
- Compruebe que no haya errores de sintaxis en los marcadores % o @

### La aplicación se vuelve lenta con textos extensos

- Active el procesamiento en paralelo en la configuración avanzada
- Considere dividir el texto en secciones más pequeñas
- Si sube archivos muy grandes, espere pacientemente a que se complete la carga

### Las anotaciones no se muestran correctamente

- Asegúrese de seleccionar el formato de salida adecuado para el tipo de archivo JSON que está utilizando
- Verifique que su navegador sea compatible con las anotaciones Ruby HTML
- Intente con otro formato de salida (por ejemplo, formato con paréntesis)

### Error al generar el archivo JSON

- Verifique que su archivo CSV tenga el formato correcto (dos columnas)
- Asegúrese de que los archivos JSON de reglas sean válidos
- Intente con los archivos por defecto para identificar si el problema está en sus archivos personalizados

## Enlaces a otras versiones

La aplicación está disponible en múltiples idiomas. Puede acceder a las diferentes versiones a través de los enlaces que encontrará en la parte inferior de la página principal.

Además, cada versión cuenta con un repositorio en GitHub donde puede encontrar documentación adicional y ejemplos de uso.

---

Este manual ha sido diseñado para ayudarle a utilizar eficazmente todas las funcionalidades de la Herramienta de Reemplazo de Caracteres en Texto Esperanto. Si encuentra dificultades adicionales o tiene sugerencias para mejorar la aplicación, no dude en consultar la documentación detallada en el repositorio de GitHub correspondiente a la versión en español.

¡Esperamos que esta herramienta sea de gran utilidad para su trabajo con textos en esperanto!
