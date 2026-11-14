"""Functional event model; timing assumptions are not device guarantees."""
import heapq, itertools, json
from pathlib import Path

def evaluate(intervals, delay, on_latency, off_latency):
    events=[]; serial=itertools.count(); token=0; a=d=0; n=0; p=1; overlap=False
    def put(t,k,v): heapq.heappush(events,(t,next(serial),k,v))
    t=0
    for interval in intervals:
        t+=interval;put(t,'input',None)
    t_end=t+delay*3
    ncmd=0;pcmd=0; nversion=0;pversion=0
    def commands(t):
        nonlocal ncmd,pcmd,nversion,pversion
        newn=a & d;newp=a | d
        if newn!=ncmd:
            ncmd=newn;nversion+=1;put(t+(on_latency if newn else off_latency),'n',(nversion,newn))
        if newp!=pcmd:
            pcmd=newp;pversion+=1;put(t+(off_latency if newp else on_latency),'p',(pversion,1-newp))
    while events:
        t,_,kind,value=heapq.heappop(events)
        if t>t_end:break
        if kind=='input':
            a=1-a;token+=1;put(t+delay,'qualified',(token,a));commands(t)
        elif kind=='qualified':
            version,state=value
            if version==token:d=state;commands(t)
        elif kind=='n':
            if value[0]==nversion:n=value[1]
        elif kind=='p':
            if value[0]==pversion:p=value[1]
        overlap=overlap or bool(n and p)
    return overlap

results=[]
# Time unit: microsecond. No claim that 0.5us bounds physical turn-off.
for intervals in itertools.product([0.1,1,9.9,10.1,20],repeat=5):
    for on,off in [(0,0.5),(0.5,0),(0.1,0.1)]:
        results.append(evaluate(intervals,10,on,off))
assert not any(results)
result={'model':'retriggered inertial both-edge qualifier; AND/OR; initially brake', 'time_unit':'us','delay':10,'input_sequences':5**5,'timing_cases':3,'total_cases':len(results),'overlap_cases':sum(results),'assumed_driver_and_FET_latencies_us':[[0,0.5],[0.5,0],[0.1,0.1]],'limitations':['Not an LTC6994 or MOSFET electrical model','No supply ramp, metastability, jitter, or parasitics','Chosen latency envelope is an assumption, not a verified device bound']}
Path(__file__).with_name('qualifier-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
