import warnings

warnings.filterwarnings('ignore')  # 屏蔽数学警告

from nicegui import ui
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 读取数据
df = pd.read_csv('清理后的数据.csv', encoding='utf-8-sig')

# 全局样式
ui.add_head_html('''
<style>
    body { background-color: #F8F9FA; font-family: 'Microsoft YaHei', sans-serif; }
    .card { background: white; border-radius: 12px; padding: 24px; 
            margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .metric-value { font-size: 36px; font-weight: bold; }
    .table-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #2C3E50; }
</style>
''')

# 侧边栏导航
with ui.left_drawer(value=True).style('background-color: #2C3E50; color: white;'):
    ui.label('📊 导航').style('font-size: 20px; font-weight: bold; margin-bottom: 20px;')
    selected = ui.radio(
        ['研究概览', '描述性统计', '动机结构', '语言迁移', '回归分析', '质性发现', '问卷原文'],
        value='研究概览'
    ).style('color: white;')

# 主内容区
content = ui.column().classes('w-full p-8')


def render_page():
    content.clear()
    with content:
        # ========== 页面1：研究概览 ==========
        if selected.value == '研究概览':
            with ui.card().classes('card w-full'):
                ui.label('英语专业学生德语二外学习动机研究').style(
                    'font-size: 28px; font-weight: bold; color: #2C3E50;')
                ui.label("📌 注：当前为7人小样本探索性回归（保留3个核心自变量），模型有效自由度增加，结果能更真实地反映变量间的预测关系。").style('font-size: 13px; color: #7F8C8D; margin-top: 10px; padding: 10px; border-radius: 5px;')

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

            # 新增：理论假设模型图
            with ui.card().classes('card w-full'):
                ui.label('📊 理论假设模型图（L2MSS框架）').style('font-size: 20px; font-weight: bold;')
                ui.label('图示为本研究的理论假设路径，未来可扩大样本量后使用结构方程模型（SEM）进行验证。').style(
                    'color: #7F8C8D; font-size: 14px; margin-bottom: 10px;')
                # 加载刚才生成的图片
                ui.image('sem_model.png').classes('w-full max-w-4xl mx-auto')

        # ========== 页面2：描述性统计 ==========
        elif selected.value == '描述性统计':
            desc_vars = ['理想德语自我', '德语学习体验', '语言迁移感知', '学习投入总分']

            with ui.card().classes('card w-full'):
                ui.label('【表1】描述性统计与信度分析（模仿论文 Table 1）').classes('table-title')

                def cronbach_alpha(df_items):
                    df_items = df_items.dropna()
                    k = df_items.shape[1]
                    if k < 2: return np.nan
                    var_items = df_items.var(axis=0, ddof=1)
                    var_total = df_items.sum(axis=1).var(ddof=1)
                    if var_total == 0: return np.nan
                    return (k / (k - 1)) * (1 - var_items.sum() / var_total)

                alpha_ideal = cronbach_alpha(df[['理想1', '理想2', '理想3', '理想4', '理想5']])
                alpha_exp = cronbach_alpha(df[['体验1', '体验2', '体验3', '体验4', '体验5']])
                alpha_trans = cronbach_alpha(df[['迁移1', '迁移2', '迁移3', '迁移4_正向']])
                alpha_invest = cronbach_alpha(df[['投入1', '投入2', '投入3', '投入4', '投入5', '投入6']])

                table1_data = []
                for var, name, alpha_val in zip(
                        desc_vars,
                        ['理想二语自我', '二语学习经历', '语言迁移感知', '预期学习努力程度'],
                        [alpha_ideal, alpha_exp, alpha_trans, alpha_invest]
                ):
                    table1_data.append({
                        '变量': name,
                        '均值 (M)': round(df[var].mean(), 2),
                        '标准差 (SD)': round(df[var].std(), 2),
                        'Cronbach α': round(alpha_val, 2) if not np.isnan(alpha_val) else '-'
                    })

                ui.table(
                    columns=[{'name': '变量', 'label': '变量', 'field': '变量', 'align': 'left'},
                             {'name': '均值 (M)', 'label': '均值 (M)', 'field': '均值 (M)'},
                             {'name': '标准差 (SD)', 'label': '标准差 (SD)', 'field': '标准差 (SD)'},
                             {'name': 'Cronbach α', 'label': 'Cronbach α', 'field': 'Cronbach α'}],
                    rows=table1_data
                ).classes('w-full')

            with ui.card().classes('card w-full'):
                ui.label('动机维度均值对比图').style('font-size: 20px; font-weight: bold;')
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

        # ========== 页面3：动机结构 ==========
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
                reason_cols = ['选德原因_迁移优势', '选德原因_文化兴趣', '选德原因_考研',
                               '选德原因_家人建议', '选德原因_被调剂', '选德原因_老师口碑',
                               '选德原因_同学', '选德原因_留学']
                reason_labels = ['迁移优势', '文化兴趣', '考研', '家人建议', '被调剂', '老师口碑', '同学', '留学']
                counts = df[reason_cols].sum().values.tolist()
                ui.echart({
                    'yAxis': {'type': 'category', 'data': reason_labels[::-1]},
                    'xAxis': {'type': 'value'},
                    'series': [{'type': 'bar', 'data': counts[::-1],
                                'itemStyle': {'color': '#4C72B0'}}],
                    'tooltip': {'trigger': 'axis'},
                }).style('height: 400px; width: 100%;')

        # ========== 页面4：语言迁移 ==========
        elif selected.value == '语言迁移':
            with ui.card().classes('card w-full'):
                ui.label('🔗 语言迁移分析').style('font-size: 28px; font-weight: bold;')
                desc_vars = ['理想德语自我', '德语学习体验', '语言迁移感知', '学习投入总分']
                corr = df[desc_vars].corr().round(3)
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

        # ========== 页面5：回归分析 ==========
        elif selected.value == '回归分析':
            x_vars = ['德语学习体验', '理想德语自我', '语言迁移感知']
            y_var = '学习投入总分'

            reg_data = df[x_vars + [y_var]].copy()
            for col in x_vars + [y_var]:
                reg_data[col] = reg_data[col].fillna(reg_data[col].mean())

            with ui.card().classes('card w-full'):
                ui.label('【表2】多元线性回归分析结果（模仿论文 Table 2）').classes('table-title')

                if len(reg_data) < 2:
                    ui.label('⚠️ 有效数据太少，无法计算回归。').style('color: red; font-size: 18px;')
                else:
                    X = reg_data[x_vars]
                    X = sm.add_constant(X)
                    y = reg_data[y_var]

                    model = sm.OLS(y, X).fit(method='pinv')

                    vif_data = []
                    for i, var in enumerate(X.columns):
                        if var != 'const':
                            vif = variance_inflation_factor(X.values, i)
                            vif_data.append(vif)
                        else:
                            vif_data.append(np.nan)

                    X_std = (X[x_vars] - X[x_vars].mean()) / X[x_vars].std()
                    y_std = (y - y.mean()) / y.std()
                    model_std = sm.OLS(y_std, X_std).fit()
                    beta_values = model_std.params.tolist()

                    table2_data = []
                    for i, var in enumerate(X.columns):
                        p_val = model.pvalues[var]
                        stars = '***' if p_val < 0.001 else ('**' if p_val < 0.01 else ('*' if p_val < 0.05 else ''))
                        beta_display = beta_values[i - 1] if var != 'const' else np.nan

                        table2_data.append({
                            '变量': var if var != 'const' else '(常量)',
                            'B (非标准化)': round(model.params[var], 3),
                            '标准误': round(model.bse[var], 3),
                            'Beta (标准化)': round(beta_display, 3) if not np.isnan(beta_display) else '-',
                            't值': round(model.tvalues[var], 3),
                            'p值': f"{round(p_val, 3)} {stars}",
                            'VIF': round(vif_data[i], 3) if not np.isnan(vif_data[i]) else '-'
                        })

                    ui.table(
                        columns=[{'name': '变量', 'label': '变量', 'field': '变量', 'align': 'left'},
                                 {'name': 'B (非标准化)', 'label': 'B (非标准化)', 'field': 'B (非标准化)'},
                                 {'name': '标准误', 'label': '标准误', 'field': '标准误'},
                                 {'name': 'Beta (标准化)', 'label': 'Beta (标准化)', 'field': 'Beta (标准化)'},
                                 {'name': 't值', 'label': 't值', 'field': 't值'},
                                 {'name': 'p值', 'label': 'p值', 'field': 'p值'},
                                 {'name': 'VIF', 'label': 'VIF', 'field': 'VIF'}],
                        rows=table2_data
                    ).classes('w-full')

                    ui.label(
                        f"注：R² = {model.rsquared:.3f}, 调整 R² = {model.rsquared_adj:.3f}, F = {model.fvalue:.3f}, p = {model.f_pvalue:.3f}。*p<0.05, **p<0.01, ***p<0.001。").style(
                        'font-size: 13px; color: #7F8C8D; margin-top: 10px;')

            with ui.card().classes('card w-full'):
                ui.label('模型预测效果图（实际值 vs 预测值）').style('font-size: 20px; font-weight: bold;')
                if len(reg_data) >= 2:
                    y_pred = model.predict(X)
                    scatter_data = [[float(real), float(pred)] for real, pred in zip(y, y_pred)]
                    line_data = [[1, 1], [6, 6]]

                    ui.echart({
                        'title': {'text': '模型预测效果：实际学习投入 vs 预测学习投入', 'left': 'center'},
                        'tooltip': {'trigger': 'item', 'formatter': '实际值: {c0}<br/>预测值: {c1}'},
                        'xAxis': {'type': 'value', 'name': '实际学习投入', 'min': 1, 'max': 6},
                        'yAxis': {'type': 'value', 'name': '预测学习投入', 'min': 1, 'max': 6},
                        'series': [
                            {
                                'name': '学生样本',
                                'type': 'scatter',
                                'data': scatter_data,
                                'symbolSize': 20,
                                'itemStyle': {'color': '#4C72B0'}
                            },
                            {
                                'name': '完美预测线',
                                'type': 'line',
                                'data': line_data,
                                'showSymbol': False,
                                'lineStyle': {'type': 'dashed', 'color': '#C44E52'}
                            }
                        ]
                    }).style('height: 500px; width: 100%; margin-top: 20px;')

                    ui.label("💡 解读：散点越靠近红色虚线，模型预测越准确。").style(
                        'font-size: 14px; margin-top: 10px; color: #7F8C8D;')

        # ========== 页面6：质性发现 ==========
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

        # ========== 页面7：问卷原文 ==========
        elif selected.value == '问卷原文':
            with ui.card().classes('card w-full'):
                ui.label('📄 调查问卷全文').style('font-size: 28px; font-weight: bold; color: #2C3E50;')
                ui.label('《英语专业本科生第二外语（德语）学习动机与投入调查问卷》').style(
                    'color: #7F8C8D; margin-bottom: 20px; font-size: 16px;')

                ui.markdown("""
### 第一部分：基本信息

**1. 你的性别：**
○ 男  ○ 女

**2. 你的生源地：**
○ 城市  ○ 县城  ○ 乡镇/农村

**3. 你的英语专业四级（TEM-4）成绩：**
○ 未考  ○ 未通过  ○ 合格  ○ 良好  ○ 优秀

**4. 你第一学期德语期末成绩（自报等级）：**
○ 90分以上  ○ 80-89分  ○ 70-79分  ○ 60-69分  ○ 60分以下

**5. 入学前你是否接触过德语？**
○ 从未接触  ○ 偶尔接触（如影视、音乐）  ○ 系统学习过（如中学选修课）


### 第二部分：选择德语的原因

**6. 你选择德语作为第二外语的主要原因是什么？（可多选，最多选3项）**
□ 英语和德语同属日耳曼语系，有语言迁移优势
□ 对德国文化、哲学、音乐、文学感兴趣
□ 听说德语考研竞争相对较小
□ 家人/老师建议
□ 被调剂/随机分配
□ 德语老师的口碑好
□ 身边同学都选了德语
□ 希望未来去德国留学或工作
□ 其他（请注明：______）


### 第三部分：德语学习动机（L2MSS 量表）

*以下题目均采用 1-6 级评分（1=完全不同意，6=完全同意）*

**7. 理想德语自我：**
1. 我经常想象自己未来能用德语与德语母语者自如交流
2. 我希望将来能从事与德语相关的工作或研究
3. 掌握德语是我未来理想自我形象的一部分
4. 我渴望有一天能读懂德语原版的哲学或文学作品
5. 如果我的德语能达到较高水平，我会觉得自己更有竞争力

**8. 应该德语自我：**
1. 家人认为学好德语对我未来的发展很重要
2. 我觉得不学好德语会辜负老师或家长的期望
3. 周围同学都在认真学德语，我不学好像说不过去
4. 如果德语考试不及格，我会觉得对不起父母的投入
5. 学好德语是我作为英语专业学生“应该”做到的事

**9. 德语学习体验：**
1. 上德语课让我感到愉快和充实
2. 我喜欢德语课上的互动和氛围
3. 德语老师讲课的方式让我对这门语言更感兴趣
4. 在德语学习中遇到困难时，我愿意花时间去克服
5. 相比其他课程，我更期待上德语课

**10. 英语与德语关系感知（语言迁移）：**
1. 我觉得英语基础对我学德语有帮助
2. 德语的词汇和英语有很多相似之处，这让我学起来更轻松
3. 我会主动将德语的语法规则与英语进行对比来帮助理解
4. 英语的语序习惯有时会干扰我学德语


### 第四部分：学习投入

**11. 你平均每周在课外花在德语学习上的时间大约是：**
○ 1小时以下  ○ 1-2小时  ○ 2-3小时  ○ 3-5小时  ○ 5小时以上

**12. 以下关于学习投入的描述：**
1. 我会按时完成德语作业并主动复习
2. 我在德语课上会积极参与互动和练习
3. 我会主动归纳德语的语法规则并整理笔记
4. 我会规划自己的德语学习进度并设定目标
5. 我对德语学习保持积极的态度
6. 即使遇到困难，我也不会轻易放弃德语学习


### 第五部分：学习困难感知

**13. 以下德语学习的典型难点，请根据你目前的感受评估其困难程度（1-5分）：**
1. 名词的语法性别（der/die/das）
2. 名词的格变化（Nominativ/Akkusativ/Dativ/Genitiv）
3. 动词变位
4. 语序（如动词第二位、从句动词末位）
5. 特殊发音（如 ü, ö, ch, r）
6. 词汇记忆（与英语形近但义不同的词）


### 第六部分：开放题

**14. 如果重新选择，你还会选择德语作为第二外语吗？为什么？**
（请填写：______）

**15. 你对目前的德语教学有什么建议？**
（请填写：______）
                """).style('font-size: 15px; line-height: 1.8;')


# 绑定事件并渲染
selected.on_value_change(lambda: render_page())
render_page()

# 启动应用
import os
# ... 其他代码 ...
import os
# ... 其他代码 ...
ui.run(
    host='0.0.0.0',  # 关键：绑定到 0.0.0.0 才能被 Render 扫描到
    port=int(os.environ.get('PORT', 8080)),  # 关键：动态读取 Render 分配的端口
    title='德语二外学习动机研究',
    reload=False
)