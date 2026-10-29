# 赌徒破产 精简版:pip install numpy 后运行,种子1891,结果同视频
import numpy as np
N,A=10000,10;R=np.random.default_rng
r=R(1891);p=np.full(N,A);a=p>0;w=~a
while a.any():p[a]+=r.choice([-1,1],a.sum());w|=a&(p>=20);a&=(p>0)&(p<20)
print('止盈 赢/输',w.sum(),N-w.sum())
f=np.full(N,A);m=f.copy();q=f.copy();fa=f>0;qa=fa.copy();g=0
for t in range(1,500001):
 i=np.flatnonzero(fa);u=r.random(i.size)
 f[i]+=np.where(u<.5,1,-1);m[i]=np.maximum(m[i],f[i]);fa[i[f[i]<1]]=0
 q[i]+=np.where(u<18/37,1,-1)*qa[i];qa[i[q[i]<1]]=0
 if t in(370,1000,1500,10**4,10**5,5*10**5):print(t,'局 公平/轮盘存活',fa.sum(),qa.sum())
 if g<1 and qa.sum()<=790:g=t
print('赢到5万后输光',(m>=50).sum()-fa[m>=50].sum(),'轮盘降到790人用',g,'局')
r=R(1891);B=[]
for _ in range(N):
 b,s,t,k=10000,100,0,10000
 while t<2000 and s<=b:
  t+=1
  if r.random()<.5:b+=s;s=100
  else:b-=s;s*=2
  k=max(k,b)
 if s>b:B+=[(t,k)]
B=np.array(B);print('翻倍法破产',len(B),'中位局数',np.median(B[:,0]),'破产前最高',np.median(B[:,1]))
r=R(1891);d=np.zeros(N)
for k in range(1,11):d[(d==0)&(r.random(N)<.1)]=k
s=(d==0).sum();print('按钮10次存活',s,'人均倍数',s*1024/N)
