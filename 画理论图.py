import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体，防止方框乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建画布
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off') # 隐藏坐标轴

# 颜色配置
color_ellipse = '#F0F4F8' # 潜变量浅蓝
color_box = '#FFFFFF'     # 观测变量白色
color_line = '#2C3E50'    # 线条深灰

# ========== 1. 画潜变量（椭圆） ==========
# 理想二语自我 (左上)
ax.add_patch(patches.Ellipse((2, 6), 2.5, 1.2, facecolor=color_ellipse, edgecolor=color_line, lw=2))
ax.text(2, 6, '理想二语自我', ha='center', va='center', fontsize=12, fontweight='bold')

# 应该二语自我 (左下)
ax.add_patch(patches.Ellipse((2, 2), 2.5, 1.2, facecolor=color_ellipse, edgecolor=color_line, lw=2))
ax.text(2, 2, '应该二语自我', ha='center', va='center', fontsize=12, fontweight='bold')

# 二语学习经历 (中上)
ax.add_patch(patches.Ellipse((6, 5), 2.5, 1.2, facecolor=color_ellipse, edgecolor=color_line, lw=2))
ax.text(6, 5, '二语学习经历', ha='center', va='center', fontsize=12, fontweight='bold')

# 自主学习行为 (右侧)
ax.add_patch(patches.Ellipse((10.5, 4), 2.8, 1.4, facecolor=color_ellipse, edgecolor=color_line, lw=2))
ax.text(10.5, 4, '自主学习行为', ha='center', va='center', fontsize=12, fontweight='bold')

# ========== 2. 画观测变量（方框） ==========
def draw_box(x, y, text):
    ax.add_patch(patches.Rectangle((x, y), 0.8, 0.6, facecolor=color_box, edgecolor=color_line, lw=1.5))
    ax.text(x + 0.4, y + 0.3, text, ha='center', va='center', fontsize=10)

# 理想二语自我的观测变量 (a1-a4)
for i in range(4):
    draw_box(0.2, 6.8 - i*0.8, f'a{i+1}')
    ax.annotate('', xy=(1.0, 6.8 - i*0.8 + 0.3), xytext=(1.5, 6),
                arrowprops=dict(arrowstyle='->', color=color_line, lw=1.5))

# 应该二语自我的观测变量 (a5-a8)
for i in range(4):
    draw_box(0.2, 2.8 - i*0.8, f'a{i+5}')
    ax.annotate('', xy=(1.0, 2.8 - i*0.8 + 0.3), xytext=(1.5, 2),
                arrowprops=dict(arrowstyle='->', color=color_line, lw=1.5))

# 二语学习经历的观测变量 (a9-a12)
for i in range(4):
    draw_box(5.2, 6.8 - i*0.8, f'a{i+9}')
    ax.annotate('', xy=(6.0, 6.8 - i*0.8 + 0.3), xytext=(6, 5.6),
                arrowprops=dict(arrowstyle='->', color=color_line, lw=1.5))

# 自主学习行为的观测变量 (a13-a21)
for i in range(9):
    draw_box(12.0, 7.2 - i*0.75, f'a{i+13}')
    ax.annotate('', xy=(12.0, 7.2 - i*0.75 + 0.3), xytext=(11.5, 4),
                arrowprops=dict(arrowstyle='->', color=color_line, lw=1.5))

# ========== 3. 画潜变量之间的关系（箭头和系数） ==========
# 理想 -> 经历
ax.annotate('', xy=(4.8, 5.2), xytext=(3.2, 5.8), arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2))
ax.text(4.0, 5.7, '.31', color='#E74C3C', fontsize=11, fontweight='bold')

# 应该 -> 经历
ax.annotate('', xy=(4.8, 4.8), xytext=(3.2, 2.2), arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2))
ax.text(4.0, 3.5, '-.18', color='#E74C3C', fontsize=11, fontweight='bold')

# 理想 -> 行为
ax.annotate('', xy=(9.1, 4.5), xytext=(3.2, 5.8), arrowprops=dict(arrowstyle='->', color='#2980B9', lw=2))
ax.text(6.0, 5.2, '.38', color='#2980B9', fontsize=11, fontweight='bold')

# 应该 -> 行为
ax.annotate('', xy=(9.1, 4.0), xytext=(3.2, 2.2), arrowprops=dict(arrowstyle='->', color='#2980B9', lw=2))
ax.text(6.0, 2.8, '.08', color='#2980B9', fontsize=11, fontweight='bold')

# 经历 -> 行为
ax.annotate('', xy=(9.1, 4.2), xytext=(7.2, 4.8), arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2))
ax.text(8.0, 4.6, '.43', color='#27AE60', fontsize=11, fontweight='bold')

# 理想 <-> 应该 (协方差)
ax.annotate('', xy=(2, 2.6), xytext=(2, 5.4), arrowprops=dict(arrowstyle='<->', color='#8E44AD', lw=2, linestyle='dashed'))
ax.text(1.2, 4.0, '-.28', color='#8E44AD', fontsize=11, fontweight='bold')

plt.title('英语专业学生德语二外学习动机理论假设模型', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('sem_model.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ 成功！已在项目文件夹生成 sem_model.png")