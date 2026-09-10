import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import warnings
warnings.filterwarnings('ignore')

# 中文字体设置（Windows 用 SimHei）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid', font='SimHei')

# ============================================================
# 第1步：读取 Excel
# ============================================================
df = pd.read_excel('问卷数据.xlsx')
print(f"数据形状：{df.shape[0]} 份问卷，{df.shape[1]} 个变量")

# ============================================================
# 第2步：自动重命名列
# ============================================================
rename_map = {
    '作答ID': 'ID',
    '你的性别': '性别',
    '入学前你是否接触过德语': '入学前接触',
    '英语和德语同属日耳曼语系': '选德原因_迁移优势',
    '对德国文化、哲学、音乐、文学感兴趣': '选德原因_文化兴趣',
    '听说德语考研竞争相对较小': '选德原因_考研',
    '家人/老师建议': '选德原因_家人建议',
    '被调剂/随机分配': '选德原因_被调剂',
    '德语老师的口碑好': '选德原因_老师口碑',
    '身边同学都选了德语': '选德原因_同学',
    '希望未来去德国留学或工作': '选德原因_留学',
    '其他（请注明': '选德原因_其他',
    '我选择德语是因为觉得英语基础对学德语有帮助': '选择动机_迁移帮助',
    '我选择德语是因为对德国的历史和文化有浓厚兴趣': '选择动机_文化',
    '我选择德语是因为听说德语对考研二外比较有利': '选择动机_考研',
    '我选择德语主要是听从了家人或老师的建议': '选择动机_家人',
    '我选择德语是因为喜欢的同学/朋友也选了德语': '选择动机_同学',
    '我选择德语是因为觉得德语听起来很有吸引力': '选择动机_吸引',
    '我经常想象自己未来能用德语与德语母语者自如交流': '理想1',
    '我希望将来能从事与德语相关的工作或研究': '理想2',
    '掌握德语是我未来理想自我形象的一部分': '理想3',
    '我渴望有一天能读懂德语原版的哲学或文学作品': '理想4',
    '如果我的德语能达到较高水平，我会觉得自己更有竞争力': '理想5',
    '上德语课让我感到愉快和充实': '体验1',
    '我喜欢德语课上的互动和氛围': '体验2',
    '德语老师讲课的方式让我对这门语言更感兴趣': '体验3',
    '在德语学习中遇到困难时，我愿意花时间去克服': '体验4',
    '相比其他课程，我更期待上德语课': '体验5',
    '我觉得英语基础对我学德语有帮助': '迁移1',
    '德语的词汇和英语有很多相似之处，这让我学起来更轻松': '迁移2',
    '我会主动将德语的语法规则与英语进行对比来帮助理解': '迁移3',
    '英语的语序习惯有时会干扰我学德语': '迁移4_反向',
    '你平均每周在课外花在德语学习上的时间大约是': '课外时间',
    '我会按时完成德语作业并主动复习': '投入1',
    '我在德语课上会积极参与互动和练习': '投入2',
    '我会主动归纳德语的语法规则并整理笔记': '投入3',
    '我会规划自己的德语学习进度并设定目标': '投入4',
    '我对德语学习保持积极的态度': '投入5',
    '即使遇到困难，我也不会轻易放弃德语学习': '投入6',
    '名词的语法性别': '难点_性别',
    '名词的格变化': '难点_格变化',
    '动词变位': '难点_动词变位',
    '语序（如动词第二位': '难点_语序',
    '特殊发音': '难点_发音',
    '词汇记忆': '难点_词汇',
    '如果重新选择': '开放题1',
    '你对目前的德语教学有什么建议': '开放题2',
}

new_columns = {}
for col in df.columns:
    for keyword, new_name in rename_map.items():
        if keyword in col:
            new_columns[col] = new_name
            break
df = df.rename(columns=new_columns)

print("\n重命名后的列名：")
print(df.columns.tolist())

# ============================================================
# 第3步：数据清洗与维度计算
# ============================================================

# 3.1 反向题计分
df['迁移4_正向'] = 7 - df['迁移4_反向']
print(f"\n迁移4原始均值：{df['迁移4_反向'].mean():.2f}")
print(f"迁移4正向均值：{df['迁移4_正向'].mean():.2f}")

# 3.2 计算各维度总分
df['理想德语自我'] = df[['理想1','理想2','理想3','理想4','理想5']].mean(axis=1)
df['德语学习体验'] = df[['体验1','体验2','体验3','体验4','体验5']].mean(axis=1)
df['语言迁移感知'] = df[['迁移1','迁移2','迁移3','迁移4_正向']].mean(axis=1)
df['行为投入'] = df[['投入1','投入2']].mean(axis=1)
df['认知投入'] = df[['投入3','投入4']].mean(axis=1)
df['情感投入'] = df[['投入5','投入6']].mean(axis=1)
df['学习投入总分'] = df[['投入1','投入2','投入3','投入4','投入5','投入6']].mean(axis=1)

print("\n各维度描述统计：")
print(df[['理想德语自我','德语学习体验','语言迁移感知',
          '行为投入','认知投入','情感投入','学习投入总分']].describe().round(2))

# 3.3 多选题统计
reason_cols = ['选德原因_迁移优势','选德原因_文化兴趣','选德原因_考研',
               '选德原因_家人建议','选德原因_被调剂','选德原因_老师口碑',
               '选德原因_同学','选德原因_留学','选德原因_其他']
reason_counts = df[reason_cols].sum().sort_values(ascending=False)
print("\n选择德语的原因分布（人数）：")
print(reason_counts)

# 3.4 创建分组变量
df['是否被调剂'] = df['选德原因_被调剂'].apply(lambda x: '被调剂' if x == 1 else '主动选择')
df['接触程度'] = df['入学前接触'].map({
    '从未接触': '从未接触',
    '偶尔接触（如影视、音乐）': '偶尔接触',
    '系统学习过（如中学选修课）': '系统学习'
})

print("\n是否被调剂分组人数：")
print(df['是否被调剂'].value_counts())
print("\n性别分组人数：")
print(df['性别'].value_counts())

# 3.5 保存清理后的数据
df.to_csv('清理后的数据.csv', index=False, encoding='utf-8-sig')
print("\n清理后的数据已保存为 清理后的数据.csv")

# ============================================================
# 第4步：统计分析（不依赖 scipy/pingouin）
# ============================================================

# ----- 4.1 手动实现 Cronbach's α -----
def cronbach_alpha(df_items):
    """手动计算 Cronbach's α"""
    df_items = df_items.dropna()
    k = df_items.shape[1]
    if k < 2 or len(df_items) < 2:
        return np.nan
    var_items = df_items.var(axis=0, ddof=1)
    var_total = df_items.sum(axis=1).var(ddof=1)
    if var_total == 0:
        return np.nan
    alpha = (k / (k - 1)) * (1 - var_items.sum() / var_total)
    return alpha

# ----- 4.2 手动实现独立样本 t 检验 -----
def t_test_ind(g1, g2):
    """手动实现独立样本t检验，返回(t值, p值近似)"""
    g1 = np.array(g1, dtype=float)
    g2 = np.array(g2, dtype=float)
    g1 = g1[~np.isnan(g1)]
    g2 = g2[~np.isnan(g2)]
    n1, n2 = len(g1), len(g2)
    if n1 < 2 or n2 < 2:
        return np.nan, np.nan
    m1, m2 = np.mean(g1), np.mean(g2)
    v1, v2 = np.var(g1, ddof=1), np.var(g2, ddof=1)
    sp2 = ((n1-1)*v1 + (n2-1)*v2) / (n1+n2-2)
    if sp2 == 0:
        return np.nan, np.nan
    se = np.sqrt(sp2 * (1/n1 + 1/n2))
    t = (m1 - m2) / se
    # 用正态近似算p值（双尾）
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(t) / math.sqrt(2))))
    return t, p

# ----- 4.3 手动实现相关系数 p 值 -----
def pearson_with_p(x, y):
    """计算Pearson相关系数及其p值（正态近似）"""
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    mask = ~(np.isnan(x) | np.isnan(y))
    x, y = x[mask], y[mask]
    n = len(x)
    if n < 3:
        return np.nan, np.nan
    r = np.corrcoef(x, y)[0, 1]
    if abs(r) >= 1:
        return r, 0.0
    t = r * math.sqrt((n-2) / (1 - r**2))
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(t) / math.sqrt(2))))
    return r, p

# ----- 4.4 信度检验 -----
print("\n" + "=" * 50)
print("信度检验（Cronbach's α）")
print("=" * 50)

dimensions = {
    '理想德语自我': ['理想1','理想2','理想3','理想4','理想5'],
    '德语学习体验': ['体验1','体验2','体验3','体验4','体验5'],
    '语言迁移感知': ['迁移1','迁移2','迁移3','迁移4_正向'],
    '行为投入': ['投入1','投入2'],
    '认知投入': ['投入3','投入4'],
    '情感投入': ['投入5','投入6'],
    '学习投入总分': ['投入1','投入2','投入3','投入4','投入5','投入6'],
}

alpha_results = []
for name, cols in dimensions.items():
    if all(c in df.columns for c in cols):
        alpha = cronbach_alpha(df[cols])
        alpha_results.append({'维度': name, '题项数': len(cols), 'Cronbach α': round(alpha, 3)})
        print(f"{name}：α = {alpha:.3f}")
alpha_df = pd.DataFrame(alpha_results)

# ----- 4.5 描述统计与分组比较 -----
desc_vars = ['理想德语自我','德语学习体验','语言迁移感知',
             '行为投入','认知投入','情感投入','学习投入总分']

print("\n" + "=" * 50)
print("总体描述性统计")
print("=" * 50)
print(df[desc_vars].describe().round(2))

# 按性别分组
print("\n按性别分组均值：")
gender_means = df.groupby('性别')[desc_vars].mean().round(2)
print(gender_means)

if df['性别'].nunique() == 2:
    print("\n性别差异 t 检验：")
    for var in desc_vars:
        g1 = df[df['性别'] == df['性别'].unique()[0]][var]
        g2 = df[df['性别'] == df['性别'].unique()[1]][var]
        t, p = t_test_ind(g1, g2)
        if not np.isnan(t):
            print(f"{var}：t = {t:.3f}, p = {p:.3f} ({'显著' if p<0.05 else '不显著'})")

# 按是否被调剂分组
print("\n按是否被调剂分组均值：")
adjust_means = df.groupby('是否被调剂')[desc_vars].mean().round(2)
print(adjust_means)

print("\n主动选择 vs 被调剂 t 检验：")
for var in desc_vars:
    g1 = df[df['是否被调剂'] == '主动选择'][var]
    g2 = df[df['是否被调剂'] == '被调剂'][var]
    t, p = t_test_ind(g1, g2)
    if not np.isnan(t):
        print(f"{var}：t = {t:.3f}, p = {p:.3f} ({'显著' if p<0.05 else '不显著'})")

# 按接触程度分组
print("\n按接触程度分组均值：")
contact_means = df.groupby('接触程度')[desc_vars].mean().round(2)
print(contact_means)

# ----- 4.6 相关分析 -----
corr_vars = desc_vars
corr_matrix = df[corr_vars].corr()
print("\n" + "=" * 50)
print("相关系数矩阵")
print("=" * 50)
print(corr_matrix.round(3))

print("\n关键相关显著性：")
for i, var1 in enumerate(corr_vars):
    for var2 in corr_vars[i+1:]:
        r, p = pearson_with_p(df[var1], df[var2])
        if not np.isnan(r):
            sig = "**" if p < 0.01 else ("*" if p < 0.05 else "")
            print(f"{var1} ↔ {var2}：r = {r:.3f}{sig}, p = {p:.3f}")

# ============================================================
# 第5步：数据可视化
# ============================================================

# 图1：动机维度均值对比
means = [df['理想德语自我'].mean(), df['德语学习体验'].mean(),
         df['语言迁移感知'].mean(), df['学习投入总分'].mean()]
labels = ['理想德语自我', '德语学习体验', '语言迁移感知', '学习投入']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, means, color=['#4C72B0','#55A868','#C44E52','#8172B3'])
for bar, m in zip(bars, means):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05, f'{m:.2f}', ha='center')
ax.set_ylabel('均值（1-6）')
ax.set_title('各维度均值对比')
ax.set_ylim(0, 6)
plt.tight_layout()
plt.savefig('图1_动机维度对比.png', dpi=150)
plt.close()
print("\n已保存 图1_动机维度对比.png")

# 图2：选德原因频率
plt.figure(figsize=(10, 6))
reason_counts.plot(kind='barh', color='#4C72B0')
plt.xlabel('选择人数')
plt.title('选择德语的原因分布')
plt.tight_layout()
plt.savefig('图2_选德原因.png', dpi=150)
plt.close()
print("已保存 图2_选德原因.png")

# 图3：相关热力图
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, fmt='.2f')
plt.title('各维度相关系数矩阵')
plt.tight_layout()
plt.savefig('图3_相关热力图.png', dpi=150)
plt.close()
print("已保存 图3_相关热力图.png")

# 图4：分组对比（箱线图）
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(x='是否被调剂', y='理想德语自我', data=df, ax=axes[0])
axes[0].set_title('理想德语自我：主动选择 vs 被调剂')
sns.boxplot(x='是否被调剂', y='学习投入总分', data=df, ax=axes[1])
axes[1].set_title('学习投入：主动选择 vs 被调剂')
plt.tight_layout()
plt.savefig('图4_分组对比.png', dpi=150)
plt.close()
print("已保存 图4_分组对比.png")

# ============================================================
# 第6步：保存分析结果到 Excel
# ============================================================
with pd.ExcelWriter('分析结果.xlsx') as writer:
    alpha_df.to_excel(writer, sheet_name='信度检验', index=False)
    df[desc_vars].describe().round(2).to_excel(writer, sheet_name='描述统计')
    gender_means.to_excel(writer, sheet_name='按性别分组')
    adjust_means.to_excel(writer, sheet_name='按是否被调剂分组')
    contact_means.to_excel(writer, sheet_name='按接触程度分组')
    corr_matrix.round(3).to_excel(writer, sheet_name='相关矩阵')

print("\n分析结果已保存为 分析结果.xlsx")
print("\n" + "=" * 50)
print("全部分析完成！")
print("=" * 50)