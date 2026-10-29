"""
《赌徒破产定理：哪怕胜率 50%，只要你不离场，倾家荡产的概率是 100%》
视频全流程仿真代码（赌徒破产_完整代码.py）

运行环境：Python 3 + NumPy (pip install numpy)
随机种子固定为 1891（查尔斯·威尔斯走进蒙特卡洛赌场的年份）
"""

import numpy as np

N = 10000          # 实验人数：10,000 个赌徒
BANKROLL = 10000   # 初始本金：10,000 元
BET = 1000         # 每把下注：1,000 元
A = BANKROLL // BET  # 离破产线 10 步

print("=" * 72)
print(" 卷宗 A · 案号 1891-MC · 一万个赌徒仿真报告（Random Seed = 1891）")
print("=" * 72)

# ==============================================================================
# 【02｜代码实验一（上）：胜率严格五五开，赢到 20,000 元止盈离场】
# ==============================================================================
rng = np.random.default_rng(1891)
pos = np.full(N, A)
alive = np.ones(N, dtype=bool)
win = np.zeros(N, dtype=bool)

while alive.any():
    pos[alive] += rng.choice([-1, 1], alive.sum())
    w = alive & (pos >= 2 * A)   # 赢到 20,000 元（20 步）：止盈走人
    l = alive & (pos <= 0)       # 输光到 0 元：破产出局
    win |= w
    alive &= ~(w | l)

print("\n【代码实验一（有止盈）】本金 10,000 元，每把押 1,000 元，赢到 20,000 元离场：")
print(f"  - 赢到两万 · 出门 : {int(win.sum()):,} 人")
print(f"  - 输光本金 · 出局 : {int(N - win.sum()):,} 人")


# ==============================================================================
# 【02｜代码实验一（下）：拆掉止盈线，公平硬币（50%）一直玩 50 万局】
# 【04｜代码实验二：欧洲单零轮盘（18/37 ≈ 48.65%），共用完全同一组随机数】
# ==============================================================================
pos_f = np.full(N, A, dtype=np.int64)
alive_f = np.ones(N, dtype=bool)
maxpos_f = np.full(N, A, dtype=np.int64)
death_f = np.full(N, -1, dtype=np.int64)

pos_r = np.full(N, A, dtype=np.int64)
alive_r = np.ones(N, dtype=bool)

out_f = {}
out_r = {}
reach_790_r = None

for t in range(1, 500001):
    idx_f = np.flatnonzero(alive_f)
    if idx_f.size == 0:
        break
    u = rng.random(idx_f.size)

    # 1) 公平硬币 (50.0%)
    pos_f[idx_f] += np.where(u < 0.5, 1, -1)
    maxpos_f[idx_f] = np.maximum(maxpos_f[idx_f], pos_f[idx_f])
    dead_f = idx_f[pos_f[idx_f] <= 0]
    alive_f[dead_f] = False
    death_f[dead_f] = t
    if t in {1000, 10000, 100000, 500000}:
        out_f[t] = int(alive_f.sum())

    # 2) 欧洲单零轮盘 (18/37 ≈ 48.65%)，严格共用同一个 u
    r_in_f = alive_r[idx_f]
    if r_in_f.any():
        idx_r = idx_f[r_in_f]
        u_r = u[r_in_f]
        pos_r[idx_r] += np.where(u_r < 18 / 37, 1, -1)
        alive_r[idx_r[pos_r[idx_r] <= 0]] = False
    if t in {370, 1000, 1500}:
        out_r[t] = int(alive_r.sum())
    if reach_790_r is None and alive_r.sum() <= 790:
        reach_790_r = t

pk_f = int(((maxpos_f >= 50) & ~alive_f).sum())
you_idx = int(np.flatnonzero((maxpos_f >= 50) & (death_f >= 2000) & (death_f <= 30000))[0])

print("\n【代码实验一（拆掉止盈线）】胜率 50.0% 公平硬币，一直玩下去：")
for step in (1000, 10000, 100000, 500000):
    print(f"  - 第 {step:>7,} 局存活 : {out_f[step]:>5,} 人")
print(f"  - 曾赢到过 5 万（50,000 元）最后依然输光 : {pk_f:,} 人")
print(f"  - 画面蓝线「你」（#{you_idx} 号赌徒）: 最高到过 {int(maxpos_f[you_idx]) // 10} 万，第 {int(death_f[you_idx]):,} 局输光")


# ==============================================================================
# 【03｜吸收壁与翻倍法：本金 10,000 元，从 100 元起押，上限 2,000 把】
# ==============================================================================
rng = np.random.default_rng(1891)
busts = 0
rounds = []
peak = []

for i in range(N):
    b = 10000
    bet = 100
    t = 0
    pk = b
    while t < 2000:
        if bet > b:
            break
        t += 1
        if rng.random() < 0.5:
            b += bet
            bet = 100
        else:
            b -= bet
            bet *= 2
        pk = max(pk, b)
    if bet > b:
        busts += 1
        rounds.append(t)
        peak.append(pk)

print("\n【吸收壁与翻倍法】公平硬币，本金 10,000 元，从 100 元起押（2,000 把内）：")
print(f"  - 2,000 把内破产人数 : {busts:,} 人（{busts / N * 100:.0f}%）")
print(f"  - 破产者存活局数中位数 : {np.median(rounds):.0f} 把（一半人撑不过 118 把）")
print(f"  - 破产前最高资产中位数 : {np.median(peak):,.0f} 元（一半人曾净赚 {np.median(peak) - 10000:,.0f} 元以上）")


# ==============================================================================
# 【04｜代码实验二：只差 1.35 个百分点（单零轮盘 48.65%）】
# ==============================================================================
print("\n【代码实验二（单零轮盘）】胜率 18/37 ≈ 48.65%（庄家优势 2.7%），与公平局共用同一组随机数：")
for step in (370, 1000, 1500):
    print(f"  - 第 {step:>7,} 局存活 : {out_r[step]:>5,} 人")
print(f"  - 存活人数降至 790 人 : 公平赌局需 10,000 局 vs 轮盘只需 {reach_790_r:,} 局（快了 {10000 / reach_790_r:.1f} 倍）")


# ==============================================================================
# 【05｜结尾算账与互动：90% 概率存款翻倍 / 10% 概率全部清零】
# ==============================================================================
rng = np.random.default_rng(1891)
die_at = np.zeros(N, dtype=np.int32)
for k in range(1, 11):
    live = die_at == 0
    hit = live & (rng.random(N) < 0.1)
    die_at[hit] = k
surv = [int(((die_at == 0) | (die_at > k)).sum()) for k in range(11)]
mean = [surv[k] * 2 ** k / N for k in range(11)]

print("\n【结尾算账与互动｜按钮实验】90% 存款翻倍 / 10% 全部清零：")
print(f"  - 理论概率 : 连押 10 次全身而退 = {0.9**10 * 100:.0f}% ({0.9**10*100:.2f}%)，"
      f"连押 50 次 = {0.9**50 * 100:.1f}% ({0.9**50*100:.2f}%)")
print(f"  - 理论期望 : 连按 10 次人均财富 = {1.8**10:.0f} 倍 ({1.8**10:.2f} 倍)")
print(f"  - 10,000 人实测（连按 10 次）: 存活 {surv[10]:,} 人（{round(surv[10] / 100)}%），"
      f"人均财富 ×{round(mean[10])}（精确值 {mean[10]:.1f} 倍）")
print("=" * 72)
