from nicegui import ui
import pandas as pd
import numpy as np

df = pd.read_csv('清理后的数据.csv', encoding='utf-8-sig')

# 全局样式
ui.add_head_html('''
<style>
    body { background-color: #F8F9FA; font-family: 'Microsoft YaHei', sans-serif; }
    .card { background: white; border-radius: 12px; padding: 24px; 
            margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .metric-value { font-size: 36px; font-weight: bold; }
</style>
''')

# 侧边栏导航
with ui.left_drawer(value=True).style('background-color: #2C3E50; color: white;'):
    ui.label('📊 导航').style('font-size: 20px; font-weight: bold; margin-bottom: 20px;')
    selected = ui.radio(
        ['研究概览', '描述性统计', '动机结构', '语言迁移', '质性发现'],
        value='研究概览'
    ).style('color: white;')

# 主内容区
content = ui.column().classes('w-full p-8')

def render_page():
    content.clear()
    with content:
        if selected.value == '研究概览':
            with ui.card().classes('card w-full'):
                ui.label('英语专业学生德语二外学习动机研究').style('font-size: 28px; font-weight: bold; color: #2C3E50;')
                ui.label('基于L2MSS理论框架的混合方法研究').style('color: #7F8C8D; margin-bottom: 20px;')

            with ui.card().classes('card w-full'):
                ui.label('📋 基本信息').style('font-size: 20px; font-weight: bold;')
                ui.table(
                    columns=[{'name': 'key', 'label': '项目', 'field': 'key'},
                             {'name': 'value', 'label': '内容', 'field': 'value'}],
                    rows=[
                        {'key': '研究对象', 'value': '安徽大学外语学院英语专业大三学生'},
                        {'key': '有效样本', 'value': f'{len(df)} 人'},
                        {'key': '理论框架', 'value': 'Dörnyei 二语动机自我系统（L2MSS）'},
                        {'key': '调查时间', 'value': '第二学期初'},
                    ]
                ).classes('w-full')

            with ui.card().classes('card w-full'):
                ui.label('❓ 研究问题').style('font-size: 20px; font-weight: bold;')
                ui.label('1. 德语学习动机的结构特征是什么？')
                ui.label('2. 语言迁移感知如何影响德语学习动机？')
                ui.label('3. 第二学期初的动机结构有何特征？')

        elif selected.value == '描述性统计':
            with ui.card().classes('card w-full'):
                ui.label('📈 描述性统计').style('font-size: 28px; font-weight: bold;')
                desc_vars = ['理想德语自我','德语学习体验','语言迁移感知','学习投入总分']
                desc = df[desc_vars].describe().round(2)
                ui.table(
                    columns=[{'name': 'index', 'label': '统计量', 'field': 'index'}] +
                            [{'name': v, 'label': v, 'field': v} for v in desc_vars],
                    rows=desc.reset_index().to_dict('records')
                ).classes('w-full')

            with ui.card().classes('card w-full'):
                ui.label('动机维度均值对比').style('font-size: 20px; font-weight: bold;')
                means = {
                    '理想德语自我': df['理想德语自我'].mean(),
                    '德语学习体验': df['德语学习体验'].mean(),
                    '语言迁移感知': df['语言迁移感知'].mean(),
                    '学习投入': df['学习投入总分'].mean(),
                }
                ui.echart({
                    'xAxis': {'type': 'category', 'data': list(means.keys())},
                    'yAxis': {'type': 'value', 'max': 6},
                    'series': [{'type': 'bar', 'data': [round(v, 2) for v in means.values()],
                                'itemStyle': {'color': '#4C72B0'}}],
                    'tooltip': {'trigger': 'axis'},
                }).style('height: 400px; width: 100%;')

        elif selected.value == '动机结构':
            with ui.card().classes('card w-full'):
                ui.label('🔍 动机结构分析').style('font-size: 28px; font-weight: bold;')
                with ui.row().classes('w-full justify-around'):
                    for label, value, color in [
                        ('理想德语自我', df['理想德语自我'].mean(), '#4C72B0'),
                        ('德语学习体验', df['德语学习体验'].mean(), '#55A868'),
                        ('语言迁移感知', df['语言迁移感知'].mean(), '#C44E52'),
                    ]:
                        with ui.column().classes('text-center'):
                            ui.label(label).style('font-size: 16px;')
                            ui.label(f'{value:.2f}').style(f'font-size: 36px; font-weight: bold; color: {color};')

            with ui.card().classes('card w-full'):
                ui.label('选择德语的原因分布').style('font-size: 20px; font-weight: bold;')
                reason_cols = ['选德原因_迁移优势','选德原因_文化兴趣','选德原因_考研',
                               '选德原因_家人建议','选德原因_被调剂','选德原因_老师口碑',
                               '选德原因_同学','选德原因_留学']
                reason_labels = ['迁移优势','文化兴趣','考研','家人建议','被调剂','老师口碑','同学','留学']
                counts = df[reason_cols].sum().values.tolist()
                ui.echart({
                    'yAxis': {'type': 'category', 'data': reason_labels[::-1]},
                    'xAxis': {'type': 'value'},
                    'series': [{'type': 'bar', 'data': counts[::-1],
                                'itemStyle': {'color': '#4C72B0'}}],
                    'tooltip': {'trigger': 'axis'},
                }).style('height: 400px; width: 100%;')

        elif selected.value == '语言迁移':
            with ui.card().classes('card w-full'):
                ui.label('🔗 语言迁移分析').style('font-size: 28px; font-weight: bold;')
                desc_vars = ['理想德语自我','德语学习体验','语言迁移感知','学习投入总分']
                corr = df[desc_vars].corr().round(3)
                # 热力图数据
                heatmap_data = []
                for i, v1 in enumerate(desc_vars):
                    for j, v2 in enumerate(desc_vars):
                        heatmap_data.append([j, i, float(corr.iloc[i, j])])
                ui.echart({
                    'xAxis': {'type': 'category', 'data': desc_vars},
                    'yAxis': {'type': 'category', 'data': desc_vars},
                    'visualMap': {'min': -1, 'max': 1, 'calculable': True,
                                  'inRange': {'color': ['#C44E52', '#FFFFFF', '#4C72B0']}},
                    'series': [{'type': 'heatmap', 'data': heatmap_data,
                                'label': {'show': True}}],
                }).style('height: 500px; width: 100%;')

            with ui.card().classes('card w-full'):
                ui.label('📝 学术解读').style('font-size: 20px; font-weight: bold;')
                ui.label('• 如果迁移感知与理想德语自我显著正相关，说明英语基础增强了学生成为"德语使用者"的愿望。')
                ui.label('• 如果迁移感知与学习投入显著正相关，说明英语基础也促进了实际学习行为。')
                ui.label('• 可与此前研究对照：钟振华（2017）发现英语补偿、元认知、情感、社交策略与德语策略中度相关。')

        elif selected.value == '质性发现':
            with ui.card().classes('card w-full'):
                ui.label('💬 质性发现').style('font-size: 28px; font-weight: bold;')
                ui.label('开放题1：如果重新选择，你还会选择德语吗？').style('font-weight: bold; margin-top: 20px;')
                for _, row in df.iterrows():
                    if pd.notna(row.get('开放题1')):
                        with ui.row():
                            ui.label(f"{row['ID']}：").style('font-weight: bold;')
                            ui.label(row['开放题1'])

                ui.label('开放题2：对德语教学的建议').style('font-weight: bold; margin-top: 20px;')
                for _, row in df.iterrows():
                    if pd.notna(row.get('开放题2')):
                        with ui.row():
                            ui.label(f"{row['ID']}：").style('font-weight: bold;')
                            ui.label(row['开放题2'])

selected.on_value_change(lambda: render_page())
render_page()

ui.run(title='德语二外学习动机研究', port=8080, reload=False)