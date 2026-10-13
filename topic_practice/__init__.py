"""Original, lesson-specific practice and its build-time coverage contract.

IDs are permanent. Adding practice never invalidates an existing assessment.
Every registered lesson must satisfy the complete difficulty contract;
an unregistered new lesson fails the build instead of inheriting generic tasks.
"""
from collections import Counter

DIFFICULTIES = ('Easy', 'Medium', 'Hard')
COMPLETE_TOPICS = ('l01', 'l02', 'l03', 'l04', 'l05', 'l06', 'l07', 'l08', 'l26', 'l27', 'l09', 'l25', 'l10', 'l11', 'l12', 'l13', 'l14', 'l15', 'l16', 'l17', 'l18', 'l19', 'l20', 'l21', 'l22', 'l23', 'l24')

CODING_LINKS = {
    'l26': ['c_l26_easy', 'c_l26_medium', 'c_l26_hard'],
    'l27': ['c_l27_easy', 'c_l27_medium', 'c_l27_hard'],
    'l01': ['c01', 'c_l01_medium', 'c_l01_hard'],
    'l02': ['c_l02_easy', 'c_l02_medium', 'c_l02_hard'],
    'l03': ['c_l03_easy', 'c02', 'c_l03_hard'],
    'l04': ['c_l04_easy', 'c_l04_medium', 'c_l04_hard'],
    'l05': ['c_l05_easy', 'c03', 'c_l05_hard'],
    'l06': ['c_l06_easy', 'c_l06_medium', 'c_l06_hard'],
    'l07': ['c_l07_easy', 'c04', 'c_l07_hard'],
    'l08': ['c_l08_easy', 'c06', 'c_l08_hard'],
    'l09': ['c_l09_easy', 'c04', 'c_l09_hard'],
    'l25': ['c_l25_easy', 'c15', 'c_l25_hard'],
    'l10': ['c_l10_easy', 'c_l10_medium', 'c_l10_hard'],
    'l11': ['c_l11_easy', 'c07', 'c_l11_hard'],
    'l12': ['c_l12_easy', 'c_l12_medium', 'c_l12_hard'],
    'l13': ['c_l13_easy', 'c08', 'c_l13_hard'],
    'l14': ['c_l14_easy', 'c09', 'c_l14_hard'],
    'l15': ['c_l15_easy', 'c_l15_medium', 'c_l15_hard'],
    'l16': ['c_l16_easy', 'c11', 'c_l16_hard'],
    'l17': ['c_l17_easy', 'c12', 'c_l17_hard'],
    'l18': ['c_l18_easy', 'c05', 'c13'],
    'l19': ['c_l19_easy', 'c_l19_medium', 'c_l19_hard'],
    'l20': ['c_l20_easy', 'c_l20_medium', 'c_l20_hard'],
    'l21': ['c_l21_easy', 'c_l21_medium', 'c_l21_hard'],
    'l22': ['c_l22_easy', 'c_l22_medium', 'c_l22_hard'],
    'l23': ['c_l23_easy', 'c_l23_medium', 'c_l23_hard'],
    'l24': ['c14', 'c_l24_medium', 'c_l24_hard'],
}
# These permanent activities remain bookmarkable, but are outside current slots.
LEGACY_CODING_LINKS = {'l08': ['c05'], 'l14': ['c10'], 'l18': ['c14']}


def add_questions(add, questions):
    from .calculus_optimization import add_questions as differential_questions
    differential_questions(add, questions)
    from .foundation_questions import add_foundation_questions
    add_foundation_questions(add, questions)
    from .distributions import add_questions as distributions_questions
    from .stopping import add_questions as stopping_questions
    distributions_questions(add, questions)
    stopping_questions(add, questions)
    from .arithmetic import add_questions as arithmetic_questions
    from .variance import add_questions as variance_questions
    arithmetic_questions(add, questions)
    variance_questions(add, questions)
    from .data_time import add_questions as data_time_questions
    data_time_questions(add, questions)
    from .estimation import add_questions as estimation_questions
    estimation_questions(add, questions)
    from .likelihood import add_questions as likelihood_questions
    likelihood_questions(add, questions)
    from .covariance import add_questions as covariance_questions
    covariance_questions(add, questions)
    from .regression import add_questions as regression_questions
    regression_questions(add, questions)
    from .inference import add_questions as inference_questions
    inference_questions(add, questions)
    from .time_series import add_questions as time_series_questions
    time_series_questions(add, questions)
    from .validation import add_questions as validation_questions
    validation_questions(add, questions)
    from .search import add_questions as search_questions
    search_questions(add, questions)
    from .research_defence import add_questions as defence_questions
    defence_questions(add, questions)
    from .monte_carlo import add_questions as monte_carlo_questions
    monte_carlo_questions(add, questions)
    from .algorithms import add_questions as algorithms_questions
    algorithms_questions(add, questions)
    from .fair_value import add_questions as fair_value_questions
    fair_value_questions(add, questions)
    from .order_flow import add_questions as order_flow_questions
    order_flow_questions(add, questions)
    from .continuation_growth import add_questions as continuation_questions
    continuation_questions(add, questions)
    from .joint_risk import add_questions as risk_questions
    risk_questions(add, questions)
    from .finance_core import add_questions as finance_questions
    finance_questions(add, questions)
    from .calibration import add_questions as calibration_questions
    calibration_questions(add, questions)
    from .original_review import review_original_questions
    review_original_questions(questions)


def add_coding(add, tasks):
    from .calculus_optimization_coding import add_coding as differential_coding
    differential_coding(add, tasks)
    from .foundation_coding import add_foundation_coding
    add_foundation_coding(add, tasks)
    from .distributions import add_coding as distributions_coding
    from .stopping import add_coding as stopping_coding
    distributions_coding(add, tasks)
    stopping_coding(add, tasks)
    from .arithmetic import add_coding as arithmetic_coding
    from .variance import add_coding as variance_coding
    arithmetic_coding(add, tasks)
    variance_coding(add, tasks)
    from .data_time import add_coding as data_time_coding
    data_time_coding(add, tasks)
    from .estimation import add_coding as estimation_coding
    estimation_coding(add, tasks)
    from .likelihood import add_coding as likelihood_coding
    likelihood_coding(add, tasks)
    from .covariance import add_coding as covariance_coding
    covariance_coding(add, tasks)
    from .regression import add_coding as regression_coding
    regression_coding(add, tasks)
    from .inference import add_coding as inference_coding
    inference_coding(add, tasks)
    from .time_series import add_coding as time_series_coding
    time_series_coding(add, tasks)
    from .validation import add_coding as validation_coding
    validation_coding(add, tasks)
    from .search import add_coding as search_coding
    search_coding(add, tasks)
    from .research_defence import add_coding as defence_coding
    defence_coding(add, tasks)
    from .monte_carlo import add_coding as monte_carlo_coding
    monte_carlo_coding(add, tasks)
    from .algorithms import add_coding as algorithms_coding
    algorithms_coding(add, tasks)
    from .fair_value import add_coding as fair_value_coding
    fair_value_coding(add, tasks)
    from .order_flow import add_coding as order_flow_coding
    order_flow_coding(add, tasks)
    from .continuation_growth import add_coding as continuation_coding
    continuation_coding(add, tasks)
    from .joint_risk import add_coding as risk_coding
    risk_coding(add, tasks)
    from .finance_core import add_coding as finance_coding
    finance_coding(add, tasks)
    from .calibration import add_coding as calibration_coding
    calibration_coding(add, tasks)


def validate_coding(tasks):
    """Reject incomplete exercise scaffolds in either public-bank build."""
    for task in tasks:
        for key in ('prompt', 'starter', 'solution', 'explanation'):
            if not isinstance(task.get(key), str) or not task[key].strip():
                raise ValueError(f"Exercise {task['id']} needs authored {key}")
        for key in ('samples', 'tests'):
            cases = task.get(key)
            if not isinstance(cases, list) or not cases:
                raise ValueError(f"Exercise {task['id']} needs visible and hidden cases")
            if any(not isinstance(case, dict) or not isinstance(case.get('args'), list)
                   or 'expected' not in case for case in cases):
                raise ValueError(f"Exercise {task['id']} needs complete case arguments and expectations")


def attach_and_validate(lessons, questions, tasks):
    """Require honest coverage before a topic can be declared complete."""
    lesson_ids = [l['id'] for l in lessons]
    registered = set(COMPLETE_TOPICS)
    if set(lesson_ids) != registered or len(lesson_ids) != len(registered):
        raise ValueError('Register every new lesson in topic_practice and author its practice before publishing it.')
    if not set(LEGACY_CODING_LINKS) <= registered:
        raise ValueError('Additional practice must name a registered lesson.')
    q_by_id = {q['id']: q for q in questions}
    c_by_id = {c['id']: c for c in tasks}
    if len(q_by_id) != len(questions) or len(c_by_id) != len(tasks):
        raise ValueError('Practice IDs must be unique and permanent.')
    validate_coding(tasks)
    for q in questions:
        if q['lesson'] not in registered:
            raise ValueError(f"Question {q['id']} needs a registered topic owner")
        fields = ('prompt', 'solution', 'followup', 'followSolution')
        if any(not isinstance(q.get(key), str) or not q[key].strip() for key in fields):
            raise ValueError(f"Question {q['id']} needs an authored prompt, solution and follow-up")
        hints = q.get('hints')
        if not isinstance(hints, list) or len(hints) < 2 or any(not isinstance(hint, str) or not hint.strip() for hint in hints):
            raise ValueError(f"Question {q['id']} needs at least two meaningful hints")
        rubric = q.get('rubric')
        if not isinstance(rubric, list) or len(rubric) < 2 or any(not isinstance(item, str) or not item.strip() for item in rubric):
            raise ValueError(f"Question {q['id']} needs specific assessment obligations")
        if 'State the assumptions and the object you are computing.' in q['rubric']:
            raise ValueError(f"Question {q['id']} retains the generic assessment placeholder")
    for l in lessons:
        # Original shared links are retained; new questions name their owner.
        extra = [q['id'] for q in questions if q['lesson'] == l['id'] and q['id'] not in l['questions']]
        l['questions'] = l['questions'] + extra
        if l['id'] in CODING_LINKS:
            removed = set(l['coding']) - set(CODING_LINKS[l['id']])
            if not removed <= set(LEGACY_CODING_LINKS.get(l['id'], [])):
                raise ValueError(f"Preserve removed coding bookmarks explicitly in {l['id']}")
            l['coding'] = CODING_LINKS[l['id']].copy()
        legacy = LEGACY_CODING_LINKS.get(l['id'], [])
        if legacy:
            l['legacyCoding'] = legacy.copy()
        if len(set(legacy)) != len(legacy) or set(legacy) & set(l['coding']):
            raise ValueError(f"Additional practice must be distinct from current slots in {l['id']}")
        if any(id not in c_by_id for id in legacy):
            raise ValueError(f"Broken additional-practice coding bookmark in {l['id']}")
        if len(set(l['questions'])) != len(l['questions']) or len(set(l['coding'])) != len(l['coding']):
            raise ValueError(f"Duplicate practice links in {l['id']}")
        if any(id not in q_by_id for id in l['questions']) or any(id not in c_by_id for id in l['coding']):
            raise ValueError(f"Broken practice link in {l['id']}")
        qs = Counter(q_by_id[id]['difficulty'] for id in l['questions'])
        cs = Counter(c_by_id[id]['difficulty'] for id in l['coding'])
        if any(qs[level] < 2 for level in DIFFICULTIES) or set(qs) != set(DIFFICULTIES):
            raise ValueError(f"{l['id']} needs at least two interview questions per difficulty")
        if cs != Counter(DIFFICULTIES):
            raise ValueError(f"{l['id']} needs exactly one coding exercise per difficulty")
        l['practiceExpanded'] = True
