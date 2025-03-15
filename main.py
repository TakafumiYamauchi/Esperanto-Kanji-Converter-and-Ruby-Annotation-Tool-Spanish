##  main.py(1つ目)
# main.py (メインの Streamlit アプリ/機能拡充版202502)

import streamlit as st
import re
import io
import json
import pandas as pd  # 必要なら使う
from typing import List, Dict, Tuple, Optional
import streamlit.components.v1 as components
import multiprocessing

#=================================================================
# Streamlit で multiprocessing を使う際、PicklingError 回避のため
# 明示的に 'spawn' モードを設定する必要がある。
#=================================================================
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass  # すでに start method が設定済みの場合はここで無視する

#=================================================================
# エスペラント文の(漢字)置換・ルビ振りなどを行う独自モジュールから
# 関数をインポートする。
# esp_text_replacement_module.py内に定義されているツールをまとめて呼び出す
#=================================================================
from esp_text_replacement_module import (
    x_to_circumflex,
    x_to_hat,
    hat_to_circumflex,
    circumflex_to_hat,
    replace_esperanto_chars,
    import_placeholders,
    orchestrate_comprehensive_esperanto_text_replacement,
    parallel_process,
    apply_ruby_html_header_and_footer
)

#=================================================================
# Streamlit の @st.cache_data デコレータを使い、読み込み結果をキャッシュして
# JSONファイルのロード高速化を図る。大きなJSON(50MB程度)を都度読むと遅いので、
# ここで呼び出す関数をキャッシュする作り。
#=================================================================
@st.cache_data
def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
    """
    JSONファイルをロードし、以下の3つのリストをタプルとして返す:
    1) replacements_final_list
    2) replacements_list_for_localized_string
    3) replacements_list_for_2char
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    replacements_final_list = data.get(
        "全域替换用のリスト(列表)型配列(replacements_final_list)", []
    )
    replacements_list_for_localized_string = data.get(
        "局部文字替换用のリスト(列表)型配列(replacements_list_for_localized_string)", []
    )
    replacements_list_for_2char = data.get(
        "二文字词根替换用のリスト(列表)型配列(replacements_list_for_2char)", []
    )
    return (
        replacements_final_list,
        replacements_list_for_localized_string,
        replacements_list_for_2char,
    )

#=================================================================
# Streamlit ページの見た目設定
# page_title: ブラウザタブに表示されるタイトル
# layout="wide" で横幅を広く使えるUIにする
#=================================================================
st.set_page_config(page_title="Herramienta de reemplazo de caracteres (kanji) en texto en esperanto", layout="wide")

# タイトル部分（GUI表示部分のみスペイン語に）
st.title("Reemplazo de texto en esperanto por kanjis y/o anotaciones en HTML (versión ampliada)")
st.write("---")

#=================================================================
# 1) JSONファイル (置換ルール) をロード
#   (デフォルトを使うか、ユーザーがアップロードするかの選択)
#=================================================================

# ラジオボタンに format_func をつけるため、まず選択肢のリストを定義
json_options = ["デフォルトを使用する", "アップロードする"]

selected_option = st.radio(
    "¿Cómo manejar el archivo JSON? (lectura del archivo JSON de reemplazo)",
    json_options,
    format_func=lambda x: "Usar valor predeterminado" if x == "デフォルトを使用する" else "Subir archivo"
)

# Streamlit の折りたたみ (expander) でサンプルJSONのダウンロードを案内
with st.expander("Descargar archivo JSON de ejemplo (para reemplazo)"):
    # サンプルファイルのパス
    json_file_path = './Appの运行に使用する各类文件/最终的な替换用リスト(列表)(合并3个JSON文件).json'
    # JSONファイルを読み込んでダウンロードボタンを生成
    with open(json_file_path, "rb") as file_json:
        btn_json = st.download_button(
            label="Descargar el archivo JSON de ejemplo",
            data=file_json,
            file_name="archivo_de_reemplazo_ejemplo.json",
            mime="application/json"
        )

#=================================================================
# 置換ルールとして使うリスト3種を初期化しておく。
# (JSONファイル読み込み後に代入される)
#=================================================================
replacements_final_list: List[Tuple[str, str, str]] = []
replacements_list_for_localized_string: List[Tuple[str, str, str]] = []
replacements_list_for_2char: List[Tuple[str, str, str]] = []

# JSONファイルの読み込み方を分岐
if selected_option == "デフォルトを使用する":
    default_json_path = "./Appの运行に使用する各类文件/最终的な替换用リスト(列表)(合并3个JSON文件).json"
    try:
        # デフォルトJSONをロード
        (replacements_final_list,
         replacements_list_for_localized_string,
         replacements_list_for_2char) = load_replacements_lists(default_json_path)
        st.success("Se ha cargado correctamente el JSON predeterminado.")
    except Exception as e:
        st.error(f"No se pudo cargar el JSON predeterminado: {e}")
        st.stop()
else:
    # ユーザーがファイルアップロードする場合
    uploaded_file = st.file_uploader("Subir archivo JSON (en formato combinado con 3 listas).json", type="json")
    if uploaded_file is not None:
        try:
            combined_data = json.load(uploaded_file)
            replacements_final_list = combined_data.get(
                "全域替换用のリスト(列表)型配列(replacements_final_list)", [])
            replacements_list_for_localized_string = combined_data.get(
                "局部文字替换用のリスト(列表)型配列(replacements_list_for_localized_string)", [])
            replacements_list_for_2char = combined_data.get(
                "二文字词根替换用のリスト(列表)型配列(replacements_list_for_2char)", [])
            st.success("El archivo JSON se ha subido y cargado exitosamente.")
        except Exception as e:
            st.error(f"No se pudo leer el archivo JSON subido: {e}")
            st.stop()
    else:
        st.warning("No se ha subido ningún archivo JSON. Se detiene el proceso.")
        st.stop()

#=================================================================
# 2) placeholders (占位符) の読み込み
#    %...% や @...@ で囲った文字列を守るために使用する文字列群を読み込む
#=================================================================
placeholders_for_skipping_replacements: List[str] = import_placeholders(
    './Appの运行に使用する各类文件/占位符(placeholders)_%1854%-%4934%_文字列替换skip用.txt'
)
placeholders_for_localized_replacement: List[str] = import_placeholders(
    './Appの运行に使用する各类文件/占位符(placeholders)_@5134@-@9728@_局部文字列替换结果捕捉用.txt'
)

st.write("---")

#=================================================================
# 設定パラメータ (UI) - 高度な設定
# 並列処理 (multiprocessing) を利用できるかどうかのスイッチと、
# 同時プロセス数の選択
#=================================================================
st.header("Configuración avanzada (procesamiento en paralelo)")
with st.expander("Abrir configuración de procesamiento en paralelo"):
    st.write("""
    Aquí puede definir el número de procesos en paralelo a utilizar 
    durante el reemplazo de caracteres (kanji).
    """)
    use_parallel = st.checkbox("Usar procesamiento en paralelo", value=False)
    num_processes = st.number_input("Número de procesos simultáneos", min_value=2, max_value=4, value=4, step=1)

st.write("---")

#=================================================================
# 例: 出力形式の選択
# (HTMLルビ形式・括弧形式・文字列のみ など)
#=================================================================

# 以下の辞書は内部ロジックで利用しているため、キーを変更すると壊れる可能性が高い。
# -> そこで「format_func」でユーザーが見る名称だけをスペイン語にしている。
options = {
    'HTML格式_Ruby文字_大小调整': 'HTML格式_Ruby文字_大小调整',
    'HTML格式_Ruby文字_大小调整_汉字替换': 'HTML格式_Ruby文字_大小调整_汉字替换',
    'HTML格式': 'HTML格式',
    'HTML格式_汉字替换': 'HTML格式_汉字替换',
    '括弧(号)格式': '括弧(号)格式',
    '括弧(号)格式_汉字替换': '括弧(号)格式_汉字替换',
    '替换后文字列のみ(仅)保留(简单替换)': '替换后文字列のみ(仅)保留(简单替换)'
}

# ユーザーに見せるスペイン語ラベルを別途マッピング
options_spanish_labels = {
    'HTML格式_Ruby文字_大小调整': "Formato HTML con anotaciones (ruby) y ajuste de tamaño",
    'HTML格式_Ruby文字_大小调整_汉字替换': "Formato HTML con anotaciones (ruby), ajuste de tamaño y reemplazo de kanji",
    'HTML格式': "Formato HTML",
    'HTML格式_汉字替换': "Formato HTML con reemplazo de kanji",
    '括弧(号)格式': "Formato con paréntesis",
    '括弧(号)格式_汉字替换': "Formato con paréntesis y reemplazo de kanji",
    '替换后文字列のみ(仅)保留(简单替换)': "Sólo texto reemplazado (reemplazo simple)"
}

display_options = list(options.keys())

selected_display = st.selectbox(
    "Seleccione el formato de salida (use el mismo que el definido en el archivo JSON de reemplazo):",
    display_options,
    format_func=lambda key: options_spanish_labels[key]
)

format_type = options[selected_display]


# フォーム外で、変数 processed_text を初期化しておく
processed_text = ""

#=================================================================
# 4) 入力テキストのソースを選択 (手動入力 or ファイルアップロード)
#=================================================================

# ラジオボタンの選択肢（同様に format_func で表示文字を変える）
source_options = ["手動入力", "ファイルアップロード"]
st.subheader("Fuente del texto de entrada")
source_option = st.radio(
    "¿Cómo desea obtener el texto de entrada?",
    source_options,
    format_func=lambda x: "Entrada manual" if x == "手動入力" else "Subir archivo"
)

uploaded_text = ""

# ファイルアップロードが選択された場合
if source_option == "ファイルアップロード":
    text_file = st.file_uploader("Subir un archivo de texto (codificación UTF-8)", type=["txt", "csv", "md"])
    if text_file is not None:
        uploaded_text = text_file.read().decode("utf-8", errors="replace")
        st.info("El archivo de texto se ha cargado correctamente.")
    else:
        st.warning("No se ha subido ningún archivo de texto. Cambie a entrada manual o cargue un archivo.")

#=================================================================
# フォーム: 実行ボタン(送信/キャンセル)を配置
#  - テキストエリアにエスペラント文を入力してもらう
#=================================================================
with st.form(key='profile_form'):

    # アップロードテキストがあればそれを初期値にする。
    if uploaded_text:
        initial_text = uploaded_text
    else:
        # セッションステートから 'text0_value' を取得し、それがなければ空文字
        initial_text = st.session_state.get("text0_value", "")

    # メインのテキストエリア（ラベルをスペイン語に）
    text0 = st.text_area(
        "Por favor ingrese aquí el texto en esperanto",
        height=150,
        value=initial_text
    )

    # %...% と @...@ の使い方を説明した短文を出力 (ユーザー向け説明をスペイン語に)
    st.markdown("""Al encerrar una parte de texto con el signo **%** (por ej.: `%<texto de hasta 50 caracteres>%`),
    esa parte **no será reemplazada** y se mantendrá tal cual en el resultado final.""")

    st.markdown("""Asimismo, al encerrar una parte de texto con el signo **@** (por ej.: `@<texto de hasta 18 caracteres>@`),
    esa parte se reemplazará de forma **local** (limitada) dentro de ese fragmento.""")

    # 出力文字形式の選択 (エスペラント特有文字の表記形式)
    letter_type = st.radio(
        'Forma de mostrar los caracteres especiales de esperanto en el resultado',
        ('上付き文字', 'x 形式', '^形式'),
        format_func=lambda x: (
            "Signo de acento sobre la letra (ĉ → c + ˆ)" if x == "上付き文字"
            else ("Formato con x (ĉ → cx)" if x == "x 形式" else "Formato con ^ (ĉ → c^)")
        )
    )

    # 送信ボタンとキャンセルボタンを並べる
    submit_btn = st.form_submit_button('Enviar')
    cancel_btn = st.form_submit_button("Cancelar")

    # キャンセルが押された時の処理
    if cancel_btn:
        st.warning("Se canceló la operación.")
        st.stop()  # ここで処理中断

    # 送信ボタンが押されたら
    if submit_btn:
        # 入力テキストをセッションステートに保存しておく
        st.session_state["text0_value"] = text0

        #=================================================================
        # ここから実際にテキストを置換して処理 (並列 or 単一プロセス)
        #=================================================================
        if use_parallel:
            processed_text = parallel_process(
                text=text0,
                num_processes=num_processes,
                placeholders_for_skipping_replacements=placeholders_for_skipping_replacements,
                replacements_list_for_localized_string=replacements_list_for_localized_string,
                placeholders_for_localized_replacement=placeholders_for_localized_replacement,
                replacements_final_list=replacements_final_list,
                replacements_list_for_2char=replacements_list_for_2char,
                format_type=format_type
            )
        else:
            processed_text = orchestrate_comprehensive_esperanto_text_replacement(
                text=text0,
                placeholders_for_skipping_replacements=placeholders_for_skipping_replacements,
                replacements_list_for_localized_string=replacements_list_for_localized_string,
                placeholders_for_localized_replacement=placeholders_for_localized_replacement,
                replacements_final_list=replacements_final_list,
                replacements_list_for_2char=replacements_list_for_2char,
                format_type=format_type
            )

        #=================================================================
        # letter_typeの指定に応じて、最終的なエスペラント文字の表記を変換する
        #  - 上付き文字 (ĉ → c + ˆ)
        #  - x 形式 (ĉ → cx)
        #  - ^ 形式 (ĉ → c^)
        #=================================================================
        if letter_type == '上付き文字':
            processed_text = replace_esperanto_chars(processed_text, x_to_circumflex)
            processed_text = replace_esperanto_chars(processed_text, hat_to_circumflex)
        elif letter_type == '^形式':
            processed_text = replace_esperanto_chars(processed_text, x_to_hat)
            processed_text = replace_esperanto_chars(processed_text, circumflex_to_hat)

        # HTML形式の場合、ヘッダーとフッターをつける (ルビ表示対応など)
        processed_text = apply_ruby_html_header_and_footer(processed_text, format_type)

#=================================================================
# =========================================
# フォーム外の処理: 結果表示・ダウンロード
# =========================================
#=================================================================
if processed_text:
    # -- ここから追加: 巨大テキスト対策ロジック（行数ベースで一部省略表示）
    MAX_PREVIEW_LINES = 250  # 250行まで表示
    lines = processed_text.splitlines()  # 改行区切りでリスト化

    if len(lines) > MAX_PREVIEW_LINES:
        # 先頭247行 + "..." + 末尾3行のプレビュー
        first_part = lines[:247]
        last_part = lines[-3:]
        preview_text = "\n".join(first_part) + "\n...\n" + "\n".join(last_part)
        st.warning(
            f"El texto es muy extenso (total de líneas: {len(lines)}). "
            "Se muestra una vista previa limitada (primeras 247 líneas y últimas 3 líneas)."
        )
    else:
        preview_text = processed_text

    #=================================================================
    # 置換結果の表示。HTML形式の場合はプレビュータブとソースコードタブに分けて表示
    #=================================================================
    if "HTML" in format_type:
        tab1, tab2 = st.tabs(["Vista previa en HTML", "Resultado (código HTML)"])
        with tab1:
            components.html(preview_text, height=500, scrolling=True)
        with tab2:
            st.text_area("Código HTML generado:", preview_text, height=300)
    else:
        # HTML以外 (括弧形式 など) の場合はテキストタブに表示
        tab3_list = st.tabs(["Texto resultante"])
        with tab3_list[0]:
            st.text_area("Resultado:", preview_text, height=300)

    # ダウンロードボタン
    download_data = processed_text.encode('utf-8')
    st.download_button(
        label="Descargar resultado",
        data=download_data,
        file_name="resultado_reemplazo.html",
        mime="text/html"
    )

st.write("---")
st.title("Ligilo-oj(URL-oj)")
st.markdown("""
#### Ligilo-oj de la aplikaĵo en aliaj lingvaj versioj (Esperanto, English, 日本語, 中文, 한국어, Русский, español, italiano, français, Deutsch, العربية, हिन्दी, polski, Tiếng Việt, Bahasa Indonesia; entute 14 lingvoj) ⇓  
              
Esperanta versio    
https://esperanto-kanji-converter-and-ruby-annotation-tool-esperanto.streamlit.app/  
English version  
https://esperanto-kanji-converter-and-ruby-annotation-tool-english.streamlit.app/  
日本語版    
https://esperanto-kanji-converter-and-ruby-annotation-tool.streamlit.app/  
中文版  
https://esperanto-hanzi-converter-and-ruby-annotation-tool-chinese-dgw.streamlit.app/  
한국어 버전  
https://esperanto-kanji-converter-and-ruby-annotation-tool-korean-yrrx.streamlit.app/    
Русская версия  
https://esperanto-kanji-converter-and-ruby-annotation-tool-russian.streamlit.app/  
**Versión en español**  
https://esperanto-kanji-converter-and-ruby-annotation-tool-spanish.streamlit.app/  
Versione italiana  
https://esperanto-kanji-converter-and-ruby-annotation-tool-italian.streamlit.app/  
Version française  
https://esperanto-kanji-converter-and-ruby-annotation-tool-french.streamlit.app/  
Deutsche Version  
https://esperanto-kanji-converter-and-ruby-annotation-tool-german.streamlit.app/  
إصدار عربي  
https://esperanto-kanji-converter-and-ruby-annotation-tool-arabic.streamlit.app/  
हिन्दी संस्करण  
https://esperanto-kanji-converter-and-ruby-annotation-tool-hindi.streamlit.app/  
Polska wersja  
https://esperanto-kanji-converter-and-ruby-annotation-tool-polish.streamlit.app/  
Phiên bản tiếng Việt  
https://esperanto-kanji-converter-and-ruby-annotation-tool-vietnamese.streamlit.app/  
Versi Bahasa Indonesia  
https://esperanto-kanji-converter-and-ruby-annotation-tool-indonesian.streamlit.app/  

#### Uzadaj instrukcioj de la aplikaĵo (README.md en la GitHub-deponejo) ⇓    
  
Esperanta versio  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Esperanto  
English version  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-English  
日本語版    
https://github.com/Takatakatake/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-  
中文版  
https://github.com/Takatakatake/Esperanto-Hanzi-Converter-and-Ruby-Annotation-Tool-Chinese  
한국어 버전  
https://github.com/Takatakatake/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Korean  
Русская версия    
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Russian  
**Versión en español**  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Spanish  
Versione italiana  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Italian  
Version française  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-French  
Deutsche Version  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-German  
إصدار عربي  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Arabic  
हिन्दी संस्करण  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Hindi  
Polska wersja  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Polish  
Phiên bản tiếng Việt  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Vietnamese  
Versi Bahasa Indonesia  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Indonesian  
""")