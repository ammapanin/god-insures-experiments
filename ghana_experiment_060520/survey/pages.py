from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants, Player


class Instructions(Page):
    pass
    
class Demographics(Page):
    form_model = 'player'
    form_fields = [field.name
                   for field in
                   Player._meta.get_fields(
                       include_parents = False,
                       include_hidden = False)][8:-2]


class EndSurvey(Page):
    def vars_for_template(self):
        pvars = self.participant.vars
        return {"insurance_treatment":
                pvars.get('insurance_treatment').lower() == "insurance"}





page_sequence = [
    Instructions,
    Demographics,
    EndSurvey
]
