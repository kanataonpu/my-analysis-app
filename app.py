import datetime
import google.generativeai as genai
import streamlit as st
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# ==========================================
# 1. 日本全国の都道府県庁所在地および主要都市の緯度経度データ
# ==========================================
CITY_COORDS = {
    # 北海道・東北
    '北海道': ('43.0642', '141.3469'),
    '札幌': ('43.0642', '141.3469'),
    '青森': ('40.8244', '140.7400'),
    '岩手': ('39.7036', '141.1527'),
    '盛岡': ('39.7036', '141.1527'),
    '宮城': ('38.2688', '140.8721'),
    '仙台': ('38.2688', '140.8721'),
    '秋田': ('39.7186', '140.1024'),
    '山形': ('38.2404', '140.3636'),
    '福島': ('37.7500', '140.4678'),
    # 関東
    '茨城': ('36.3418', '140.4468'),
    '水戸': ('36.3418', '140.4468'),
    '栃木': ('36.5658', '139.8836'),
    '宇都宮': ('36.5658', '139.8836'),
    '群馬': ('36.3911', '139.0608'),
    '前橋': ('36.3911', '139.0608'),
    '埼玉': ('35.8569', '139.6489'),
    '千葉': ('35.6074', '140.1065'),
    '東京': ('35.6895', '139.6917'),
    '東京都': ('35.6895', '139.6917'),
    '神奈川': ('35.4478', '139.6425'),
    '横浜': ('35.4478', '139.6425'),
    # 甲信越・北陸
    '新潟': ('37.9022', '139.0236'),
    '富山': ('36.6953', '137.2113'),
    '石川': ('36.5944', '136.6256'),
    '金沢': ('36.5944', '136.6256'),
    '福井': ('36.0652', '136.2219'),
    '山梨': ('35.6642', '138.5684'),
    '甲府': ('35.6642', '138.5684'),
    '長野': ('36.6513', '138.1812'),
    # 東海
    '岐阜': ('35.3912', '136.7223'),
    '静岡': ('34.9769', '138.3831'),
    '愛知': ('35.1815', '136.9066'),
    '名古屋': ('35.1815', '136.9066'),
    '三重': ('34.7303', '136.5086'),
    '津': ('34.7303', '136.5086'),
    # 関西
    '滋賀': ('35.0045', '135.8686'),
    '大津': ('35.0045', '135.8686'),
    '京都': ('35.0116', '135.7681'),
    '大阪': ('34.6937', '135.5023'),
    '大阪府': ('34.6937', '135.5023'),
    '大阪市': ('34.6937', '135.5023'),
    '兵庫': ('34.6913', '135.1830'),
    '神戸': ('34.6913', '135.1830'),
    '奈良': ('34.6851', '135.8328'),
    '和歌山': ('34.2260', '135.1675'),
    # 中国
    '鳥取': ('35.5036', '134.2383'),
    '島根': ('35.4723', '133.0505'),
    '松江': ('35.4723', '133.0505'),
    '岡山': ('34.6617', '133.9350'),
    '広島': ('34.3965', '132.4596'),
    '山口': ('34.1861', '131.4705'),
    # 四国
    '徳島': ('34.0658', '134.5593'),
    '香川': ('34.3401', '134.0434'),
    '高松': ('34.3401', '134.0434'),
    '愛媛': ('33.8416', '132.7657'),
    '松山': ('33.8416', '132.7657'),
    '高知': ('33.5597', '133.5311'),
    # 九州・沖縄
    '福岡': ('33.5904', '130.4017'),
    '佐賀': ('33.2494', '130.2988'),
    '長崎': ('32.7448', '129.8737'),
    '熊本': ('32.7898', '130.7417'),
    '大分': ('33.2382', '131.6126'),
    '宮崎': ('31.9111', '131.4239'),
    '鹿児島': ('31.5602', '130.5581'),
    '沖縄': ('26.2124', '127.6809'),
    '那覇': ('26.2124', '127.6809'),
}


def get_coordinates(location_str):
  if not location_str:
    return ('35.6895', '139.6917')
  for city, coords in CITY_COORDS.items():
    if city in location_str:
      return coords
  return ('35.6895', '139.6917')


# ==========================================
# 2. 正確なホロスコープ計算処理（ハウス・感受点追加）
# ==========================================
def calculate_horoscope(birth_date, birth_time_str, birth_place):
  try:
    if not birth_time_str:
      time_obj = datetime.time(12, 0)
    else:
      time_obj = datetime.datetime.strptime(birth_time_str, '%H:%M').time()

    dt_local = datetime.datetime.combine(birth_date, time_obj)
    dt_utc = dt_local - datetime.timedelta(hours=9)

    date_str = dt_utc.strftime('%Y/%m/%d')
    time_str = dt_utc.strftime('%H:%M:%S')
    date_obj = Datetime(date_str, time_str, '+00:00')

    lat, lon = get_coordinates(birth_place)
    pos = GeoPos(lat, lon)

    chart = Chart(date_obj, pos, hsys=const.HOUSES_PLACIDUS)

    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)
    mercury = chart.getObject(const.MERCURY)
    venus = chart.getObject(const.VENUS)
    mars = chart.getObject(const.MARS)
    jupiter = chart.getObject(const.JUPITER)
    saturn = chart.getObject(const.SATURN)
    asc = chart.get(const.ASC)
    mc = chart.get(const.MC)
    nn = chart.getObject(const.NORTH_NODE)
    lilith = chart.getObject(const.LILITH)

    houses = {}
    for i in range(1, 13):
      h_obj = chart.getHouse(i)
      houses[f'{i}ハウス'] = f'{h_obj.sign} ({h_obj.lon:.2f}°)'

    return {
        '太陽': f'{sun.sign} ({sun.lon:.2f}°)',
        '月': f'{moon.sign} ({moon.lon:.2f}°)',
        '水星': f'{mercury.sign} ({mercury.lon:.2f}°)',
        '金星': f'{venus.sign} ({venus.lon:.2f}°)',
        '火星': f'{mars.sign} ({mars.lon:.2f}°)',
        '木星': f'{jupiter.sign} ({jupiter.lon:.2f}°)',
        '土星': f'{saturn.sign} ({saturn.lon:.2f}°)',
        'アセンダント(ASC)': f'{asc.sign} ({asc.lon:.2f}°)',
        'MC': f'{mc.sign} ({mc.lon:.2f}°)',
        'ドラゴンヘッド': f'{nn.sign} ({nn.lon:.2f}°)',
        'リリス': f'{lilith.sign} ({lilith.lon:.2f}°)',
        'ハウス情報': houses,
    }
  except Exception as e:
    return {'エラー': str(e)}


# ==========================================
# 3. 画面表示（Streamlit）
# ==========================================
st.set_page_config(
    page_title='【決定版】自己分析＆年代別マネタイズロードマップ', layout='wide'
)

st.title('🔮 【決定版】自己分析＆年代別マネタイズロードマップ')
st.write(
    '生年月日・出生情報とこれまでの経歴エピソードから、あなたの本質・変遷・年代別ライフフェーズ・現実的なロードマップを解き明かします。'
)

with st.sidebar:
  st.header('設定')
  api_key = st.text_input('Gemini APIキー', type='password')

with st.form('user_input_form'):
  st.subheader('1. 基本情報（星・数秘の用解析）')
  col1, col2 = st.columns(2)
  with col1:
    birth_date = st.date_input(
        '生年月日',
        min_value=datetime.date(1950, 1, 1),
        max_value=datetime.date(2025, 12, 31),
        value=datetime.date(1987, 9, 11),
    )
  with col2:
    birth_time_input = st.text_input(
        '出生時刻 (例: 11:43) ※不明な場合は空白でOK', value='11:43'
    )

  birth_place_input = st.text_input(
      '出生地 (例: 大阪府大阪市 / 神奈川県横浜市 / 東京都)',
      value='大阪府大阪市',
  )

  st.subheader('2. これまでの経歴と現状')
  career_history = st.text_area(
      'これまでの主な職歴・業務経験をご入力ください',
      placeholder=(
          '例：専門学校卒業後、一般事務5年、経理8年を経験。現在は在宅でバックオフィス業務を担当しつつ、個人でカウンセリング活動も行っています。'
      ),
      height=100,
  )
  strengths_weaknesses = st.text_area(
      'ご自身の長所・短所、大切にしたい価値観をご入力ください',
      placeholder=(
          '例：長所はスケジュール管理や細かい仕組み化が得意なこと。短所や不満に感じること：理不尽な対応をされるとモチベーションが下がります。'
      ),
      height=100,
  )
  episodes = st.text_area(
      '印象に残っているエピソードや、今後の目標・悩んでいることなどをご入力ください',
      placeholder=(
          '例：自分の本当にやりたいことで独立したい、または信頼できる仲間と仕事をして正当な対価を得られる環境を作りたいと考えている。'
      ),
      height=100,
  )

  submitted = st.form_submit_button('🔥 決定版ロードマップレポートを生成する')

if submitted:
  if not api_key:
    st.error('Gemini APIキーを入力してください。')
  else:
    genai.configure(api_key=api_key)

    with st.spinner(
        '正確な天体配置・ハウス・ドラゴンヘッド・リリスを計算し、レポートを生成中...'
    ):
      astro_data = calculate_horoscope(
          birth_date, birth_time_input, birth_place_input
      )

      houses_str = (
          '\n'.join(
              [
                  f'・{k}: {v}'
                  for k, v in astro_data.get('ハウス情報', {}).items()
              ]
          )
          if isinstance(astro_data.get('ハウス情報'), dict)
          else ''
      )

      prompt = f"""
あなたはプロの西洋占星術師およびキャリアカウンセラーです。
以下の「事前にプログラムで正確に計算されたホロスコープデータ（天体、ハウス、ドラゴンヘッド、リリス）」および「相談者の入力データ」を厳密に使用し、推測による変更を一切加えずに、圧倒的に深くボリュームのある自己分析・キャリア設計レポートを作成してください。

【厳格な指示】
・以下の計算結果データに記載されたサイン（星座）や度数をそのまま解釈に使用し、独自に計算し直したり変更したりすることは絶対に禁止します。

【正確な計算結果データ】
・太陽: {astro_data.get('太陽')}
・月: {astro_data.get('月')}
・水星: {astro_data.get('水星')}
・金星: {astro_data.get('金星')}
・火星: {astro_data.get('火星')}
・木星: {astro_data.get('木星')}
・土星: {astro_data.get('土星')}
・アセンダント(ASC): {astro_data.get('アセンダント(ASC)')}
・MC: {astro_data.get('MC')}
・ドラゴンヘッド: {astro_data.get('ドラゴンヘッド')}
・リリス: {astro_data.get('リリス')}

【ハウスカスプ配置】
{houses_str}

【相談者の入力データ】
・生年月日: {birth_date}
・出生時刻: {birth_time_input}
・出生地: {birth_place_input}
・職歴: {career_history}
・長所・短所: {strengths_weaknesses}
・エピソード: {episodes}

上記データに基づき、以下の【決定版】の9章構成に従って、徹底的に深掘りした分析レポートを出力してください。

第1章：基本天体・数秘が明かす「あなたの本質と核（コア）」
第2章：人生の停滞を打ち破る「ブレイクスルーの鍵」（リリス＆ドラゴンヘッド）
第3章：天職と財のルート（MC・2室・8室・10室）
第4章：【特別解析】年齢域とサイクルで読み解く「人生の変遷と覚醒」
- 20代後半のフェーズ：社会人として基礎を固め、模索していた時期の星のテーマ
- 30代前半のフェーズ：従来の働き方に対する違和感や、次への土台作りの時期
- 35歳前後の「覚醒の真実」：なぜこのタイミングで意識が「個人事業・将来の法人化」へ向かったのか？（天体・サイクルの切り替わりを解明）
- 30代後半（現在）のフェーズ：「正社員×開業」の二条のラインを走り、力を蓄える時期の課題と活用法
- 40代前半のフェーズ：事業の一本化・会社設立（法人化）に向けた飛躍と展開のテーマ
- 40代後半〜50代のフェーズ：拡大・継承・ライフワークの確立期
第5章：過去の経歴・エピソードの深層分析（リフレクション）
第6章：強みを「商品・価値」に変えるマネタイズ戦略（会社設立を見据えて）
第7章：転職・独立・法人化への年代別具体的ロードマップ
- 【ステップ1：今（30代後半）】正社員の安定を活かしながら、個人の事業基盤とファンを強固にする方法
- 【ステップ2：切り替え期（40代手前〜前半）】一本化・法人化へ踏み切るための判断基準と星のタイミング
第8章：あなたの弱みをカバーする「環境選び・パートナーシップ・組織作り」
- 将来、会社にしていく際に向いている右腕・協力者のタイプ
第9章：あなたへの総合メッセージ＆明日からのアクション3選
"""

      try:
        model = genai.GenerativeModel('gemini-3.6-flash')
        response = model.generate_content(prompt)

        st.success('分析が完了しました！')
        st.markdown(response.text)

      except Exception as e:
        st.error(f'エラーが発生しました: {str(e)}')
