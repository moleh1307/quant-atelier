"""Bounded personal Python runner; not a security boundary for hostile users."""
import ast, json, math, subprocess, sys
from pathlib import Path
from coding_bank import TASKS
ALLOWED = {'math','statistics','collections','heapq','itertools','functools','bisect','random'}
BLOCKED = {'eval','exec','open','compile','input','breakpoint','globals','locals','vars','getattr','setattr','delattr','dir','help','exit','quit','__import__'}

def validate(code):
    if len(code) > 30000:
        raise ValueError('Keep the solution below 30,000 characters.')
    tree = ast.parse(code)
    for item in ast.walk(tree):
        if isinstance(item, ast.Import) and any(a.name not in ALLOWED for a in item.names):
            raise ValueError('Available imports: '+', '.join(sorted(ALLOWED)))
        if isinstance(item, ast.ImportFrom) and (item.level or item.module not in ALLOWED or any(a.name.startswith('_') for a in item.names)):
            raise ValueError('This import is unavailable in the practice runner.')
        if isinstance(item, ast.Attribute) and item.attr.startswith('_'):
            raise ValueError('Private and dunder attributes are unavailable.')
        if isinstance(item, ast.Name) and (item.id in BLOCKED or item.id.startswith('__')):
            raise ValueError('This builtin is unavailable in the practice runner: '+item.id)

def case_copy(case, index):
    # JSON text preserves large integers, nested values and null without a
    # JavaScript parse/stringify round trip or the old truncated Python repr.
    # Compact separators keep large official cases within the debug text limit.
    copy = {'argumentsJSON': json.dumps(case['args'], allow_nan=False, separators=(',', ':')), 'caseNumber': index + 1}
    if 'expected' in case:
        copy['expectedJSON'] = json.dumps(case['expected'], allow_nan=False, separators=(',', ':'))
    return copy

def submission_cases(task_id):
    task = next((t for t in TASKS if t['id'] == task_id), None)
    if not task: return {'error': 'Unknown exercise.'}
    return {'cases': [case_copy(case, i) for i, case in enumerate(task['samples'] + task['tests'])]}

def parse_debug_cases(task, copies):
    if not isinstance(copies, list) or not 1 <= len(copies) <= 20:
        raise ValueError('Choose between 1 and 20 debugging cases.')
    definition = next(node for node in ast.parse(task['starter']).body if isinstance(node, ast.FunctionDef) and node.name == 'solve')
    arity = len(definition.args.args) + len(definition.args.posonlyargs)
    def finite(value, depth=0):
        if depth > 50: raise ValueError('JSON nesting is too deep (maximum 50 levels).')
        if isinstance(value, float) and not math.isfinite(value): raise ValueError('JSON numbers must be finite.')
        if isinstance(value, (list, dict)):
            for item in (value.values() if isinstance(value, dict) else value): finite(item, depth + 1)
    parsed = []
    for index, copy in enumerate(copies):
        try:
            if not isinstance(copy, dict): raise ValueError('Expected a case object.')
            args_text, expected_text = copy.get('argumentsJSON'), copy.get('expectedJSON', '')
            if not isinstance(args_text, str) or not isinstance(expected_text, str): raise ValueError('Arguments and expected output must be JSON text.')
            if len(args_text) + len(expected_text) > 500_000: raise ValueError('Use at most 500,000 characters per case.')
            args = json.loads(args_text)
            if not isinstance(args, list): raise ValueError('Arguments must be a JSON array, with one entry per function parameter.')
            if len(args) != arity: raise ValueError(f'solve expects {arity} arguments; this case has {len(args)}.')
            finite(args)
            case = {'args': args}
            if expected_text.strip():
                case['expected'] = json.loads(expected_text)
                finite(case['expected'])
            parsed.append(case)
        except (ValueError, TypeError, RecursionError) as error:
            raise ValueError(f'Debug case {index + 1}: {error}') from None
    return parsed

def run(task_id, code, mode='submit', debug_cases=None):
    task = next((t for t in TASKS if t['id']==task_id),None)
    if not task: return {'error':'Unknown exercise.'}
    if not isinstance(mode, str) or mode not in {'run', 'submit', 'debug'}: return {'error': 'Unknown check mode.'}
    try:
        validate(code)
        # A Submit request always uses the bank, regardless of supplied cases.
        cases = parse_debug_cases(task, debug_cases) if mode == 'debug' else task['samples'] + (task['tests'] if mode == 'submit' else [])
    except (ValueError,SyntaxError) as error:
        result={'error':str(error)}
        if isinstance(error,SyntaxError) and error.lineno: result['errorLine']=error.lineno
        return result
    try:
        child = subprocess.run([sys.executable,'-I',str(Path(__file__).with_name('runner.py'))],input=json.dumps({'code':code,'cases':cases}),capture_output=True,text=True,timeout=4)
        if child.returncode: return {'error':'The process exceeded its resource limit or exited unexpectedly.'}
        result = json.loads(child.stdout)
        result['mode'] = mode
        for index, entry in enumerate(result.get('results', [])):
            entry.update(case_copy(cases[index], index))
        return result
    except subprocess.TimeoutExpired: return {'error':'Time limit exceeded (4 seconds). Check your algorithm or loops.'}
    except (ValueError,OSError): return {'error':'Runner could not return a valid result.'}
