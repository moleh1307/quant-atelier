import builtins, contextlib, io, json, math, resource, sys, time, traceback
resource.setrlimit(resource.RLIMIT_CPU,(3,3))
resource.setrlimit(resource.RLIMIT_FSIZE,(1024*1024,1024*1024))
payload=json.load(sys.stdin)
allowed={'math','statistics','collections','heapq','itertools','functools','bisect','random'}
def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name not in allowed or level: raise ImportError('Unavailable import')
    return builtins.__import__(name,globals,locals,fromlist,level)
names='abs all any bool dict enumerate filter float int isinstance len list map max min next pow print range reversed round set slice sorted str sum tuple zip Exception ValueError TypeError IndexError ZeroDivisionError StopIteration object'.split()
safe={key:getattr(builtins,key) for key in names}
safe['__import__']=safe_import
class LimitedOutput(io.StringIO):
    def write(self,text):
        if self.tell() < 4000: return super().write(text[:4000-self.tell()])
        return len(text)
def equal(a,b):
    if isinstance(b,(int,float)) and not isinstance(b,bool):
        return isinstance(a,(int,float)) and not isinstance(a,bool) and math.isfinite(a) and abs(a-b) <= max(1e-7, 8*math.ulp(float(b)))
    if isinstance(b,list): return isinstance(a,(list,tuple)) and len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    if isinstance(b,dict): return isinstance(a,dict) and a.keys()==b.keys() and all(equal(a[k],b[k]) for k in b)
    return a==b
output=LimitedOutput(); scope={'__builtins__':safe}; results=[]; start=time.perf_counter()
def error_details(error):
    details={'error':type(error).__name__+': '+str(error)[:500]}
    frames=[frame for frame in traceback.extract_tb(error.__traceback__) if frame.filename=='solution.py']
    if frames: details['errorLine']=frames[-1].lineno
    return details
try:
    with contextlib.redirect_stdout(output):
        exec(compile(payload['code'],'solution.py','exec'),scope)
        solve=scope.get('solve')
        if not callable(solve): raise ValueError('Define a function named solve with the required parameters.')
        for index,case in enumerate(payload['cases']):
            try:
                result=solve(*case['args'])
                passed=equal(result,case['expected'])
                entry={'passed':passed,'actual':repr(result)[:450],'expected':repr(case['expected'])[:450]}
                if not passed: entry['arguments']=repr(case['args'])[:450]
                results.append(entry)
            except Exception as error:
                results.append({'passed':False,'arguments':repr(case['args'])[:450],**error_details(error)})
    response={'results':results,'passed':sum(r['passed'] for r in results),'total':len(results),'elapsedMs':round((time.perf_counter()-start)*1000,1),'stdout':output.getvalue()}
except Exception as error: response={**error_details(error),'stdout':output.getvalue()}
print(json.dumps(response,allow_nan=False))
