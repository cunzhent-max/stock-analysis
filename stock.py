import akshare as ak
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取数据
df = ak.stock_zh_index_daily(symbol="sh000001")
df = df.tail(200).reset_index(drop=True)

# 计算均线
df['MA5'] = df['close'].rolling(5).mean()
df['MA20'] = df['close'].rolling(20).mean()

# 找金叉死叉
golden = []  # 金叉
death = []   # 死叉

for i in range(1, len(df)):
    if df['MA5'][i] > df['MA20'][i] and df['MA5'][i-1] <= df['MA20'][i-1]:
        golden.append(i)
    if df['MA5'][i] < df['MA20'][i] and df['MA5'][i-1] >= df['MA20'][i-1]:
        death.append(i)

# 画图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7),
                                gridspec_kw={'height_ratios': [3, 1]})

ax1.plot(df['date'], df['close'], color='blue', linewidth=1.5, label='收盘价')
ax1.plot(df['date'], df['MA5'], color='orange', linewidth=1, label='MA5')
ax1.plot(df['date'], df['MA20'], color='red', linewidth=1, label='MA20')

# 标记金叉（绿色向上箭头）
for i in golden:
    ax1.annotate('金叉', xy=(df['date'][i], df['MA5'][i]),
                 xytext=(0, -30), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='green'),
                 color='green', fontsize=9)

# 标记死叉（红色向下箭头）
for i in death:
    ax1.annotate('死叉', xy=(df['date'][i], df['MA5'][i]),
                 xytext=(0, 30), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='red'),
                 color='red', fontsize=9)

ax1.legend()
ax1.set_title('上证指数 金叉死叉标记')

ax2.bar(df['date'], df['volume'], color='grey', alpha=0.6)
ax2.set_ylabel('成交量')

plt.tight_layout()
plt.savefig('上证指数.png')
plt.show()