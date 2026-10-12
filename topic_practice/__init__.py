"""Original, lesson-specific practice and its build-time coverage contract.

IDs are permanent. Adding practice never invalidates an existing assessment.
During the curriculum expansion, unfinished lessons are listed explicitly;
an unregistered new lesson fails the build instead of inheriting generic tasks.
"""
from collections import Counter

DIFFICULTIES = ('Easy', 'Medium', 'Hard')
COMPLETE_TOPICS = ('l01', 'l02', 'l03', 'l04', 'l05', 'l06', 'l07', 'l08', 'l09', 'l25', 'l10', 'l11', 'l12')
PENDING_TOPICS = (
    'l13', 'l14', 'l15', 'l16', 'l17', 'l18', 'l19', 'l20',
    'l21', 'l22', 'l23', 'l24',
)

CODING_LINKS = {
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
}
# These permanent activities remain bookmarkable, but are outside current slots.
LEGACY_CODING_LINKS = {'l08': ['c05']}


def add_questions(add, questions):
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


def add_coding(add, tasks):
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


def attach_and_validate(lessons, questions, tasks):
    """Require honest coverage before a topic can be declared complete."""
    lesson_ids = [l['id'] for l in lessons]
    registered = set(COMPLETE_TOPICS) | set(PENDING_TOPICS)
    if set(lesson_ids) != registered or len(lesson_ids) != len(registered):
        raise ValueError('Register every new lesson in topic_practice and author its practice before publishing it.')
    if set(COMPLETE_TOPICS) & set(PENDING_TOPICS):
        raise ValueError('A topic cannot be both complete and pending.')
    if not set(LEGACY_CODING_LINKS) <= registered:
        raise ValueError('Additional practice must name a registered lesson.')
    q_by_id = {q['id']: q for q in questions}
    c_by_id = {c['id']: c for c in tasks}
    if len(q_by_id) != len(questions) or len(c_by_id) != len(tasks):
        raise ValueError('Practice IDs must be unique and permanent.')
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
        if l['id'] in COMPLETE_TOPICS:
            qs = Counter(q_by_id[id]['difficulty'] for id in l['questions'])
            cs = Counter(c_by_id[id]['difficulty'] for id in l['coding'])
            if any(qs[level] < 2 for level in DIFFICULTIES) or set(qs) != set(DIFFICULTIES):
                raise ValueError(f"{l['id']} needs at least two interview questions per difficulty")
            if cs != Counter(DIFFICULTIES):
                raise ValueError(f"{l['id']} needs exactly one coding exercise per difficulty")
        l['practiceExpanded'] = l['id'] in COMPLETE_TOPICS
