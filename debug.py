import pandas as pd
import statsmodels.api as sm

# 读取数据
df = pd.read_csv('清理后的数据.csv', encoding='utf-8-sig')

# 定义变量
x_vars = ['德语学习体验', '理想德语自我', '语言迁移感知']
y_var = '学习投入总分'

# 均值填补
reg_data = df[x_vars + [y_var]].copy()
for col in x_vars + [y_var]:
    reg_data[col] = reg_data[col].fillna(reg_data[col].mean())

# 跑模型
X = sm.add_constant(reg_data[x_vars])
y = reg_data[y_var]
model = sm.OLS(y, X).fit(method='pinv')
y_pred = model.predict(X)

# 打印每一对实际值 vs 预测值
print("=" * 50)
print("【实际值 vs 预测值】坐标明细：")
for i, (real, pred) in enumerate(zip(y, y_pred)):
    print(f"第 {i+1} 位同学: 实际投入={real:.2f}, 预测投入={pred:.2f}")
print("=" * 50)
print(f"总共生成了 {len(y)} 个预测点！")