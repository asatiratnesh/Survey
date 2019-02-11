from django import template
register = template.Library()


@register.filter
def in_category(choices, question_id):
    return choices.filter(questions_id=question_id)


@register.filter
def in_result(choices, question_id):
    return choices.filter(question_id=question_id)
