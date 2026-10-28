"""Exact rational Diamond-lemma certificate for B and B/(S-1).
B=Q<x,y>/(x^4,y^2+yx^2+x^2y+xyx), wt(x,y)=(1,2).
Uses no numerical approximation. Proves identities by complete finite critical pairs.
"""
from fractions import Fraction as F
from functools import lru_cache
from collections import deque
import itertools, json, time
from pathlib import Path
import argparse

class GB:
 def __init__(self):
  self.gb=[];self.lms=[];self.queue=deque();self.seen=set();self.cache={};self.pairs=0
 @staticmethod
 def wt(w): return w.count('x')+2*w.count('y')
 @classmethod
 def key(cls,w): return (-cls.wt(w),tuple(-ord(c) for c in w))
 def nfword(self,w):
  if w in self.cache:return self.cache[w]
  for lm,g in zip(self.lms,self.gb):
   k=w.find(lm)
   if k>=0:
    out={};pre=w[:k];post=w[k+len(lm):]
    for v,c in g.items():
     if v==lm:continue
     for z,b in self.nfword(pre+v+post).items():
      out[z]=out.get(z,0)-c*b
      if not out[z]:del out[z]
    self.cache[w]=out;return out
  self.cache[w]={w:F(1)};return self.cache[w]
 def nf(self,f):
  out={}
  for w,c in f.items():
   if not c:continue
   for v,b in self.nfword(w).items():
    out[v]=out.get(v,0)+F(c)*b
    if not out[v]:del out[v]
  return out
 def put(self,i,pi,si,j,pj,sj):
  if (i,pi,si)==(j,pj,sj):return
  a,b=sorted(((i,pi,si),(j,pj,sj)))
  if (a,b) not in self.seen:self.seen.add((a,b));self.queue.append((a,b))
 def overlap(self,i,j):
  u,v=self.lms[i],self.lms[j]
  for k in range(len(u)-len(v)+1):
   if u[k:k+len(v)]==v:self.put(i,'','',j,u[:k],u[k+len(v):])
  for k in range(1,min(len(u),len(v))):
   if u[-k:]==v[:k]:self.put(i,'',v[k:],j,u[:-k],'')
 def add(self,f):
  f=self.nf(f)
  if not f:return
  u=min(f,key=self.key);c=f[u];f={v:b/c for v,b in f.items()}
  n=len(self.gb);self.gb.append(f);self.lms.append(u);self.cache.clear()
  for i in range(n+1):self.overlap(n,i);self.overlap(i,n)
 def complete(self,rs):
  for r in rs:self.add(r)
  while self.queue:
   a,b=self.queue.popleft();f={}
   for sign,(i,pre,post) in [(1,a),(-1,b)]:
    for v,c in self.gb[i].items():
     w=pre+v+post;f[w]=f.get(w,0)+sign*c
   self.pairs+=1;self.add(f)
   if len(self.gb)>100:raise RuntimeError('large basis')
  return self
 def normal_words(self,cutoff=None):
  stack=[''];out=[]
  while stack:
   u=stack.pop();out.append(u)
   for a in 'xy':
    w=u+a
    if cutoff is not None and self.wt(w)>cutoff:continue
    if not any(lm in w for lm in self.lms):stack.append(w)
  return sorted(out,key=lambda w:(self.wt(w),w))

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".json"))
 args=ap.parse_args()
 import sympy as sp
 Q={'yy':1,'yxx':1,'xxy':1,'xyx':1};S={'yxy':1,'yyx':1,'yxxx':1}
 b=GB().complete([{'xxxx':1},Q]);print('homogeneous basis',len(b.gb),'critical pairs',b.pairs,flush=True)
 for a in 'xy':
  z={}
  for w,c in S.items():z[w+a]=z.get(w+a,0)+c;z[a+w]=z.get(a+w,0)-c
  assert not b.nf(z)
 zero=GB().complete([{'xxxx':1},Q,S]); zws=zero.normal_words(); assert len(zws)==40
 print('S=0 dimension',len(zws),flush=True)
 # Specialization S=1 is an ORDINARY algebra, not an augmented completion.
 one=GB().complete([{'xxxx':1},Q,{**S,'':-1}]);ws=one.normal_words();n=len(ws)
 print('S=1 basis',len(one.gb),'critical pairs',one.pairs,'dimension',n,flush=True)
 assert n==25
 index={w:i for i,w in enumerate(ws)}
 def right(w):
  M=sp.zeros(n)
  for j,u in enumerate(ws):
   for v,c in one.nfword(u+w).items():M[index[v],j]=sp.Rational(c.numerator,c.denominator)
  return M
 X=right('x');Y=right('y')
 # Right multiplication reverses composition; polynomial relations still checked.
 assert X**4==sp.zeros(n)
 assert Y**2+X**2*Y+Y*X**2+X*Y*X==sp.zeros(n)
 assert Y*X*Y+X*Y**2+X**3*Y==sp.eye(n)
 def left(w):
  M=sp.zeros(n)
  for j,u in enumerate(ws):
   for v,c in one.nfword(w+u).items():M[index[v],j]=sp.Rational(c.numerator,c.denominator)
  return M
 Lx=left('x');Ly=left('y');basis=(X**3).columnspace();V=sp.Matrix.hstack(*basis)
 assert V.cols==5
 X5=V.gauss_jordan_solve(Lx*V)[0];Y5=V.gauss_jordan_solve(Ly*V)[0]
 assert X5**4==sp.zeros(5)
 assert Y5**2+Y5*X5**2+X5**2*Y5+X5*Y5*X5==sp.zeros(5)
 assert Y5*X5*Y5+Y5**2*X5+Y5*X5**3==sp.eye(5)
 print('X5 =',X5.tolist(),'Y5 =',Y5.tolist(),flush=True)
 matrices=[right(w) for w in ws]
 # The regular trace form is nondegenerate iff this characteristic-zero algebra is semisimple.
 tr=sp.Matrix(n,n,lambda i,j:sp.trace(matrices[i]*matrices[j]))
 determinant=tr.det(method='domain-ge')
 assert determinant!=0
 comm=sp.Matrix.vstack(*[sp.Matrix.hstack(*[(M*Z-Z*M).reshape(n*n,1) for M in matrices]) for Z in [X,Y]])
 centre=n-comm.rank()
 assert centre==1
 print('regular trace determinant',determinant,'centre dimension',centre,flush=True)
 print('B/(S-1) is central simple of dimension 25, hence over C is M_5(C).',flush=True)
 # Hilbert series by the finite automaton avoiding the Groebner leading words.
 prefixes={''}
 for w in b.lms:
  for k in range(1,len(w)):prefixes.add(w[:k])
 states=sorted(prefixes);idx={w:i for i,w in enumerate(states)};t=sp.symbols('t');T=sp.zeros(len(states))
 for i,u in enumerate(states):
  for a in 'xy':
   w=u+a
   if any(w.endswith(lm) for lm in b.lms):continue
   v=max((p for p in states if w.endswith(p)),key=len)
   T[i,idx[v]]+=t**b.wt(a)
 H=sp.cancel(((sp.eye(len(states))-T).inv()*sp.ones(len(states),1))[idx[''],0])
 print('Hilbert series',sp.factor(H),'generic rank',(sp.limit((1-t**5)*H,t,1)),flush=True)
 assert sp.limit((1-t**5)*H,t,1)==25
 data={'homogeneous_groebner_basis':[{w:str(c) for w,c in g.items()} for g in b.gb],
 'ordinary_S_equal_1_groebner_basis':[{w:str(c) for w,c in g.items()} for g in one.gb],
 'ordinary_S_equal_1_basis_words':ws,'regular_trace_determinant':str(determinant),'centre_dimension':int(centre),
 'hilbert_series':str(sp.factor(H)), 'X5':[[str(a) for a in row] for row in X5.tolist()], 'Y5':[[str(a) for a in row] for row in Y5.tolist()], 'S_zero_dimension':40, 'ordinary_S_equal_0_groebner_basis':[{w:str(c) for w,c in g.items()} for g in zero.gb], 'ordinary_S_equal_0_basis_words':zws, 'critical_pairs':{'homogeneous':b.pairs,'S_equal_0':zero.pairs,'S_equal_1':one.pairs}}
 args.output.parent.mkdir(parents=True, exist_ok=True)
 with args.output.open('w', encoding='utf-8') as f:json.dump(data,f,indent=2)
 print('Certificate written to', args.output)
if __name__=='__main__':main()
