from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants, Player


class ExitSurvey(Page):
    form_model = 'player'
    form_fields = [field.name
                   for field in
                   Player._meta.get_fields(
                       include_parents = False,
                       include_hidden = False)][8:-2]


page_sequence = [
    ExitSurvey
]
