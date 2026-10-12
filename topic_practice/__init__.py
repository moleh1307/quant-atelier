"""Original, lesson-specific practice and its build-time coverage contract.

IDs are permanent. Adding practice never invalidates an existing assessment.
During the curriculum expansion, unfinished lessons are listed explicitly;
an unregistered new lesson fails the build instead of inheriting generic tasks.
"""
from collections import Counter

DIFFICULTIES = ('Easy', 'Medium', 'Hard')
COMPLETE_TOPICS = ('l01', 'l02', 'l03', 'l04', 'l05')
PENDING_TOPICS = (
    'l06', 'l07', 'l08', 'l09', 'l25', 'l10', 'l11',
    'l12', 'l13', 'l14', 'l15', 'l16', 'l17', 'l18', 'l19', 'l20',
    'l21', 'l22', 'l23', 'l24',
)

CODING_LINKS = {
    'l01': ['c01', 'c_l01_medium', 'c_l01_hard'],
    'l02': ['c_l02_easy', 'c_l02_medium', 'c_l02_hard'],
    'l03': ['c_l03_easy', 'c02', 'c_l03_hard'],
    'l04': ['c_l04_easy', 'c_l04_medium', 'c_l04_hard'],
    'l05': ['c_l05_easy', 'c03', 'c_l05_hard'],
}


def add_questions(add, questions):
    from .foundation_questions import add_foundation_questions
    add_foundation_questions(add, questions)
    from .distributions import add_questions as distributions_questions
    from .stopping import add_questions as stopping_questions
    distributions_questions(add, questions)
    stopping_questions(add, questions)


def add_coding(add, tasks):
    from .foundation_coding import add_foundation_coding
    add_foundation_coding(add, tasks)
    from .distributions import add_coding as distributions_coding
    from .stopping import add_coding as stopping_coding
    distributions_coding(add, tasks)
    stopping_coding(add, tasks)


def attach_and_validate(lessons, questions, tasks):
    """Require honest coverage before a topic can be declared complete."""
    lesson_ids = [l['id'] for l in lessons]
    registered = set(COMPLETE_TOPICS) | set(PENDING_TOPICS)
    if set(lesson_ids) != registered or len(lesson_ids) != len(registered):
        raise ValueError('Register every new lesson in topic_practice and author its practice before publishing it.')
    if set(COMPLETE_TOPICS) & set(PENDING_TOPICS):
        raise ValueError('A topic cannot be both complete and pending.')
    q_by_id = {q['id']: q for q in questions}
    c_by_id = {c['id']: c for c in tasks}
    if len(q_by_id) != len(questions) or len(c_by_id) != len(tasks):
        raise ValueError('Practice IDs must be unique and permanent.')
    for l in lessons:
        # Original shared links are retained; new questions name their owner.
        extra = [q['id'] for q in questions if q['lesson'] == l['id'] and q['id'] not in l['questions']]
        l['questions'] = l['questions'] + extra
        if l['id'] in CODING_LINKS:
            l['coding'] = CODING_LINKS[l['id']].copy()
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
