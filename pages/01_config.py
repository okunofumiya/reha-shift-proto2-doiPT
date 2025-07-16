import streamlit as st
import json

# --- ページ設定 ---
st.set_page_config(
    page_title="病院・ルールの設定",
    layout="wide"
)

st.title("病院・ルールの設定 ⚙️")
st.info("ここで設定した内容は、メインのシフト作成プログラムに反映されます。")
st.markdown("---")

# --- 設定項目 ---
st.header("1. 役割（ロール）に関する設定")
st.write("職員一覧CSVに追加した「役割」列の名称を基準に、特別なルールを設定します。")

role_sunday_off = st.text_input(
    "日曜日に必ず休みになる役割名を入力してください",
    placeholder="例: 外来PT, 地域包括専従"
)
st.caption("複数の役割がある場合は、カンマ（,）で区切って入力してください。")

st.markdown("---")

st.header("2. 休日に関する設定")
st.write("シフト作成時に、日曜日以外に特別扱いする曜日や祝日を設定します。")

is_saturday_special = st.toggle("土曜日を特別休として扱う", value=False)
st.caption("ONにすると、土曜日も日曜日と同じような休日設定の対象になります。")

is_holiday_special = st.toggle("日本の祝日を特別休として扱う", value=True)
st.caption("ONにすると、祝日も日曜日と同じような休日設定の対象になります。")

st.markdown("---")

# --- 設定内容の出力 ---
st.header("3. 設定内容の保存")
st.write("以下の内容をコピーし、GitHub上の `config.json` ファイルに貼り付けて保存してください。")

# 設定を辞書形式でまとめる
config_data = {
    "role_rules": {
        "sunday_off": [role.strip() for role in role_sunday_off.split(',')]
    },
    "holiday_rules": {
        "saturday_is_special": is_saturday_special,
        "national_holiday_is_special": is_holiday_special
    }
}

# JSON形式のテキストに変換して表示
config_json_text = json.dumps(config_data, indent=2, ensure_ascii=False)
st.code(config_json_text, language="json")

st.warning("設定を変更した後は、必ず `config.json` を更新してください。")