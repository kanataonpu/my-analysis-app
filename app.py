import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 画面のタイトルと設定
st.set_page_config(
    page_title="完全版：自己分析＆年代別マネタイズ・キャリア設計診断",
    layout="wide"
)

st.title("🔮 完全版：自己分析＆年代別マネタイズ・キャリア設計診断")
st.write("生年月日・出生情報とこれまでの経歴エピソードから、あなたの本質・隠れた才能・年代ごとのライフフェーズ・現実的な収益化ロードマップを解き明かします。")

# サイドバー：APIキーの入力（Secrets未設定時のバックアップ用）
st.sidebar.header("設定")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Streamlit Secretsに設定していない場合、ここに入力してください。")

# Secretに設定されている場合は優先利用
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

# メインフォーム
with st.form("user_input_form"):
    st.subheader("1. 基本情報（星・数秘の解析用）")
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("生年月日", min_value=datetime(1950, 1, 1), max_value=datetime.today())
    with col2:
        birth_time = st.text_input("出生時刻（例: 14:30）※不明な場合は空白でOK", "")
    
    birth_place = st.text_input("出生地（例: 神奈川県座間市 / 東京都）", "")

    st.subheader("2. これまでの経歴と現状")
    career_history = st.text_area(
        "これまでの主な職歴・業務経験",
        placeholder="例: 事務職を10年経験後、現在はフルリモートで働きつつ、個人でカウンセリングや占い事業を開業中。",
        height=100
    )

    strengths_weaknesses = st.text_area(
        "自分自身で自覚している長所・短所",
        placeholder="長所: 人の気持ちを察するのが早い、世界観を作るのが好き\n短所: 妥協できない、集団生活で疲れやすい",
        height=100
    )

    episodes = st.text_area(
        "印象に残っているエピソード（成功体験・ワクワクしたこと・辛かった克服体験など）",
        placeholder="例: 35歳頃に意識の大きな覚醒があり、社会人としての降伏から『個人の力で立ち上がり独立・将来は法人化したい』というビジョンへ劇的にシフトした。",
        height=100
    )

    submit_button = st.form_submit_button("🔥 超詳細な分析レポートを生成する")

# 分析ボタンが押された時の処理
if submit_button:
    if not api_key:
        st.error("APIキーが設定されていません。サイドバーにAPIキーを入力するか、Streamlitのシークレットを設定してください。")
    elif not career_history or not strengths_weaknesses:
        st.warning("経歴や長所・短所などの必須項目を入力してください。")
    else:
        try:
            # APIキーを設定
            genai.configure(api_key=api_key)
            
            # 無料アカウントで確実に動作する gemini-1.5-flash に指定
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
あなたは西洋占星術・数秘術・キャリアコンサルティング・ビジネスプロデュースに精通した一流のスペシャリストです。
以下のユーザー情報に沿って、文字数を惜しまず、読み物として濃厚かつ超具体的な「完全版：自己分析＆年代別マネタイズ・キャリア設計シート」を作成してください。

---
【ユーザー情報】
■ 生年月日: {birth_date.strftime('%Y年%m月%d日')}
■ 出生時刻: {birth_time if birth_time else '不明'}
■ 出生地: {birth_place if birth_place else '未設定'}
■ 主な経歴:
{career_history}
■ 自覚している長所・短所:
{strengths_weaknesses}
■ 印象的なエピソード・転機:
{episodes}
---

【出力指示・構成ルール】
以下の全9章の構成に沿って、各章それぞれ具体例・根拠・ロジックを交えて詳細に執筆してください。文字数の縮小や省略は厳禁です。

# 🔮 完全版：自己分析＆年代別マネタイズ・キャリア設計シート

## 第1章：あなたの宿命と本質（星と数秘の解読）
- 生年月日・出生情報から読み解く魂のテーマ・本質的な強み・克服すべき宿題
- 西洋占星術および数秘術的視点からのパーソナリティ分析

## 第2章：これまでの人生の伏線回収と「強みの言語化」
- これまでの経験やエピソードに隠された「本質的な強み」と「固有の価値」
- 弱みや辛かった出来事の「ポジティブな再定義（光の側面）」

## 第3章：魂が望む本当のキャリアビジョンと「使命」
- あなたが人生で本当に目指すべき「生き方」と「社会での立ち位置」
- 組織勤務・個人事業・法人化など、あなたに最適な働き方のスタイル

## 第4章：マネタイズ（収益化）ポイントと「あなた専用の商品・サービス設計」
- あなたの経験・得意・本質を組み合わせた「具体的なビジネスモデル」
- ターゲット層の設定、提供できる価値、推奨される具体的な商品・サービス例

## 第5章：年代別（30代・40代・50代・60代〜）ライフ＆キャリアロードマップ
- **30代**：土台作りと独立・シフトの具体的な戦略
- **40代**：事業の拡大・法人化・影響力の確立
- **50代**：仕組み化・自動化・後進の育成や次なる展開
- **60代以降**：生涯現役としてのライフワークと社会的集大成

## 第6章：現在直面している課題と「突破するための具体的アクションプラン」
- 現状のモヤモヤや障壁に対する具体的なクリア方法
- 今すぐ（1〜3ヶ月以内）に取り組むべき優先タスクTOP3

## 第7章：あなたの運命を切り拓く「人間関係・パートナーシップ」の活かし方
- あなたを高めてくれる相性の良い人物タイプや環境
- ビジネスや人生における信頼関係・チーム作りの注意点

## 第8章：エネルギー・モチベーション管理とメンタルケア
- メンタルが落ちたときの回復法（スイッチの切り替え方）
- 持続可能なエネルギーを保つための日々の習慣

## 第9章：あなたへ贈る「人生の羅針盤となるメッセージ」
- 全体を通した愛と情熱のこもった総括メッセージ
"""

            with st.spinner("🔮 あなたの星と経歴を深く読み解き、超詳細な分析レポートを生成中...（1〜2分ほどかかります）"):
                response = model.generate_content(prompt)
                st.success("✨ 分析が完了しました！")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
