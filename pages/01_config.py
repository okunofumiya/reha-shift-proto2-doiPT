import streamlit as st
import json
import os

# --- ページ設定 ---
st.set_page_config(
    page_title="病院・ルールの設定",
    layout="wide"
)

st.title("病院・ルールの設定 ⚙️")

# ---【改善点①】config.jsonを読み込む ---
config_path = 'config.json'
# デフォルト値を設定
default_config = {
    "role_rules": {"sunday_off": []},
    "holiday_rules": {
        "saturday_is_special": False,
        "national_holiday_is_special": True
    }
}
# ファイルが存在すれば読み込み、なければデフォルト値を使う
if os.path.exists(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            current_config = json.load(f)
    except json.JSONDecodeError:
        st.error("config.jsonファイルが破損しているため、デフォルト設定で表示しました。")
        current_config = default_config
else:
    st.info("config.json が見つかりません。新規作成のためのデフォルト設定で表示します。")
    current_config = default_config

# --- 設定項目 ---
st.header("1. 役割（ロール）に関する設定")
st.write("職員一覧CSVに追加した「役割」列の名称を基準に、特別なルールを設定します。")

# ---【改善点②】読み込んだ値でUIの初期値を設定 ---
# カンマ区切りの文字列に変換
sunday_off_roles_str = ", ".join(current_config.get("role_rules", {}).get("sunday_off", []))

role_sunday_off = st.text_input(
    "日曜日に必ず休みになる役割名を入力してください",
    value=sunday_off_roles_str, # valueに設定
    placeholder="例: 外来PT, 地域包括専従"
)
st.caption("複数の役割がある場合は、カンマ（,）で区切って入力してください。")

st.markdown("---")

st.header("2. 休日に関する設定")
st.write("シフト作成時に、日曜日以外に特別扱いする曜日や祝日を設定します。")

# ---【改善点③】読み込んだ値でUIの初期値を設定 ---
saturday_setting = current_config.get("holiday_rules", {}).get("saturday_is_special", False)
holiday_setting = current_config.get("holiday_rules", {}).get("national_holiday_is_special", True)

is_saturday_special = st.toggle("土曜日を特別休として扱う", value=saturday_setting)
st.caption("ONにすると、土曜日も日曜日と同じような休日設定の対象になります。")

is_holiday_special = st.toggle("日本の祝日を特別休として扱う", value=holiday_setting)
st.caption("ONにすると、祝日も日曜日と同じような休日設定の常になります。")

st.markdown("---")

# --- 設定内容の出力 ---
st.header("3. 設定内容の保存")
st.write("以下の内容をコピーし、GitHub上の `config.json` ファイルに貼り付けて保存してください。")

# UIの現在の状態から設定を辞書形式でまとめる
new_config_data = {
    "role_rules": {
        # 入力が空の場合のエラーを避ける
        "sunday_off": [role.strip() for role in role_sunday_off.split(',') if role.strip()]
    },
    "holiday_rules": {
        "saturday_is_special": is_saturday_special,
        "national_holiday_is_special": is_holiday_special
    }
}

# JSON形式のテキストに変換して表示
config_json_text = json.dumps(new_config_data, indent=2, ensure_ascii=False)
st.code(config_json_text, language="json")

st.warning("設定を変更した後は、必ず `config.json` を更新してください。")