import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 1. 读取清理后的数据
df = pd.read_csv('清理后的数据.csv', encoding='utf-8-sig')

# 2. 定义学术变量（基于上面的映射表）
y_var = '学习投入总分'  # 因变量
x_vars = ['德语学习体验', '理想德语自我', '选择动机_考研', '选择动机_家人', '语言迁移感知']  # 自变量

# ==================== 表1：描述性统计与信度分析 ====================
print("=" * 70)
print("【表1】描述性统计（模仿论文 Table 1）")
print("=" * 70)
# 均值、标准差
desc_table = df[x_vars + [y_var]].agg(['mean', 'std']).T
desc_table.columns = ['均值 (M)', '标准差 (SD)']
print(desc_table.round(3))

# 信度分析（Cronbach's Alpha，模仿论文中的信度报告）
def cronbach_alpha(df_items):
    df_items = df_items.dropna()
    k = df_items.shape[1]
    var_items = df_items.var(axis=0, ddof=1)
    var_total = df_items.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - var_items.sum() / var_total)

print("\n--- 信度分析 (Cronbach's Alpha) ---")
print(f"学习投入量表 α = {cronbach_alpha(df[['投入1','投入2','投入3','投入4','投入5','投入6']]):.3f}")
print(f"德语学习体验 α = {cronbach_alpha(df[['体验1','体验2','体验3','体验4','体验5']]):.3f}")
print(f"理想德语自我 α = {cronbach_alpha(df[['理想1','理想2','理想3','理想4','理想5']]):.3f}")

# ==================== 表2：相关分析与多元回归 ====================
print("\n" + "=" * 70)
print("【表2】多元线性回归分析（模仿论文 Table 2）")
print("=" * 70)

# 准备回归数据（加上常数项）
X = df[x_vars]
X = sm.add_constant(X)
y = df[y_var]

# 拟合模型
model = sm.OLS(y, X).fit()

# 打印回归结果（包含 R²、F值、p值、系数、t值等）
print(model.summary())

# ==================== 表3：多重共线性检验（VIF） ====================
print("\n" + "=" * 70)
print("【表3】多重共线性检验（模仿论文 VIF 报告，应小于 5）")
print("=" * 70)
for i, var in enumerate(X.columns):
    if var != 'const':
        vif = variance_inflation_factor(X.values, i)
        print(f"{var:15s} | VIF: {vif:.3f}")

print("\n" + "=" * 70)
print("分析完成！")