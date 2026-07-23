import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 画面のタイトルと設定
st.set_page_config(
    page_title="完全版：自己分析＆年代別マネタイズ・キャリア設計診断",
    layout="wide"
)

st.title("🔮 完全版：自己分析＆年代別マネタイズ・キャリア設計診断")
st.write("生年月日・出生情報とこれまでの経歴エピソードから、あなたの本質・隠れた才能・年代ごとのライフフェーズ・現実的な収益化ロードマップを紐解きます。")

# サイドバー：APIキーの入力（Secrets未設定時のバックアップ用）
st.sidebar.header("設定")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Streamlit Secretsに設定していない場合、ここに入力してください。")

# Secretsに設定されている場合は優先利用
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
        "自分で自覚している長所・短所",
        placeholder="長所: 人の気持ちを察するのが早い、世界観を作るのが好き\n短所: 妥協できない、集団生活で疲れやすい",
        height=100
    )
    
    episodes = st.text_area(
        "印象に残っているエピソード（成功体験・ワクワクしたこと・辛かった克服体験など）",
        placeholder="例: 35歳頃に意識の大きな覚醒があり、社会人としての枠組みから『個人の力で立ち上がり独立・将来は法人化したい』というビジョンへ劇的にシフトした。",
        height=100
    )

    submit_button = st.form_submit_button("🔥 超詳細な分析レポートを生成する")

# 分析ボタンが押された時の処理
if submit_button:
    if not api_key:
        st.error("APIキーが設定されていません。サイドバーにAPIキーを入力するか、StreamlitのSecretsを設定してください。")
    elif not career_history or not strengths_weaknesses:
        st.warning("経歴や長所・短所などの必須項目を入力してください。")
    else:
        try:
            genai.configure(api_key=api_key)
            # 最新・高速なモデルを設定
            # 修正後
model = genai.GenerativeModel("gemini-2.0-flash")

            prompt = f"""
あなたは西洋占星術・数秘術・キャリアコンサルティング・ビジネスプロデュースに精通した超一流のスペシャリストです。
以下のユーザー情報に基づき、文字数を惜しまず、読み物として重厚かつ超具体的な「完全版：自己分析＆年代別マネタイズ・キャリア設計シート」を作成してください。

---
【ユーザー情報】
■ 生年月日: {birth_date.strftime('%Y年%m月%d日')}
■ 出生時刻: {birth_time if birth_time else '不明'}
■ 出生地: {birth_place if birth_place else '未指定'}
■ 主な経歴:
{career_history}
■ 自覚している長所・短所:
{strengths_weaknesses}
■ 印象的なエピソード・転機:
{episodes}
---

【出力指示・構成ルール】
以下の全9章の構成に沿って、各章それぞれ具体例・根拠・ロジックを交えて詳細に執筆してください。文字数の削減や端折ることは厳禁です。

# 📖 完全版：自己分析＆年代別マネタイズ・キャリア設計シート

### 第1章：基本天体・数秘が明かす「あなたの本質と核（コア）」
- 太陽星座・月星座・数秘（ライフパス等）の解析から紐解くあなたの本性・心の満たされ方
- 本能的に得意なこと・最もパフォーマンスを発揮できる環境

### 第2章：人生の停滞を打ち破る「ブレイクスルーの鍵」（リリス＆ドラゴンヘッド）
- ドラゴンヘッド（今世開拓すべきテーマ）が示す飛躍のトリガー
- リリス（無意識の尖ったこだわり・圧倒的魅力）の解放とブランド化
- 自覚している短所の真実（実は隠れた才能が裏目に出ている可能性の読み解き）

### 第3章：天職と財のルート（MC・2室・8室・10室）
- MC（社会的到達点）が示すあなたが最終的に果たすべき役割
- 2室（自力で稼ぐ力）＆8室（他者・組織から受け取る財）から読み解くお金の循環システム
- 最も適した働き方の形態（個人事業・法人化・パートナーシップ等）

### 第4章：【特別解析】年齢域とサイクルで読み解く「人生の変遷と覚醒」
- **20代後半のフェーズ:** 社会人として基礎を固めていた時期のテーマ
- **30代前半のフェーズ:** 従来の働き方への違和感と次への準備期
- **35歳前後の「覚醒の真実」:** なぜこのタイミングで「個人事業・将来の法人化」へ意識が向かったのか？（年齢域・天体・数秘サイクルの切り替わりを解明）
- **30代後半（現在）のフェーズ:** 「会社員×開業」の二条のラインを走り、力を蓄える時期の課題と活用法
- **40代前半のフェーズ:** 事業の一本化・会社設立（法人化）に向けた飛躍と展開のテーマ
- **40代後半〜50代のフェーズ:** 事業拡大・継承・ライフワークの確立期

### 第5章：過去の経歴・エピソードの深層分析（リフレクション）
- 過去の成功体験・辛かった体験と星の素質との照合分析
- 経験から抽出される「あなただけの再現可能な強み」

### 第6章：強みを「商品・価値」に変えるマネタイズ戦略（将来の法人化を見据えて）
- 素質×経歴で作る「高単価・独自ポジション」のアイデア
- 収入を何倍にも跳ね上げるための具体的な商品化・サービス化の着眼点

### 第7章：転職・独立・法人化への年代別具体的ロードマップ
- **【ステップ1：今（30代後半）】** 安定を保ちつつ個人事業のファン・基盤を固める具体的行動
- **【ステップ2：切り替え期（40代手前〜前半）】** 一本化・法人化へ踏み切るための判断基準と星のタイミング
- **【ステップ3：拡大期】** 会社として組織化・展開していくステップ

### 第8章：あなたの弱みをカバーする「環境選び・パートナーシップ・組織作り」
- 選んではいけないストレスフルな環境の特徴
- 将来、会社を大きくしていく際に向いている右腕・協力者（パートナー）のタイプ

### 第9章：あなたへの総合メッセージ＆明日からの具体的アクション3選
- 全体を通したAIからの総括エールと、明日すぐできる行動3ステップ
"""

            with st.spinner("Geminiが星と経歴を高度分析し、超詳細レポートを生成中...（1〜2分ほどかかります）"):
                response = model.generate_content(prompt)
                st.success("分析が完了しました！")
                st.markdown("---")
                st.markdown(response.text)
                
                # ダウンロードボタン（テキストファイルとして保存）
                st.download_button(
                    label="📥 分析結果（レポート）をダウンロード",
                    data=response.text,
                    file_name=f"self_analysis_report_{birth_date.strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
