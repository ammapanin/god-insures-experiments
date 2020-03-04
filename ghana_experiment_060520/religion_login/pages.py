from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player


class ReligionLoginPage(Page):
    form_model = 'player'
    # form_fields = ['enumerator',
    #                'experiment_session',
    #                'church',
    #                'revival',
    #                'treatment']

    def get_form_fields(self):
        base_fields = ['enumerator',
                       'experiment_session',
                       'church',
                       'revival',
                       'treatment']

        if self.session.config.get('truncated') == False:
            return base_fields
        else:
            return base_fields + ['explanation']

    def before_next_page(self):
        pvars = self.participant.vars
        pvars['insurance_treatment'] = self.player.treatment
        print(pvars.get('insurance_treatment'))
        
page_sequence = [
    ReligionLoginPage,
]
