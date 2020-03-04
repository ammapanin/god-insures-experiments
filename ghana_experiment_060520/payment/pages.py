from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class DrawRandom(Page):
    form_model = 'player'
    form_fields = ['random_letter',
                   'payment_password',
                   'enumerator_help']

    def random_letter_choices(self):
        pvars = self.participant.vars
        return pvars.get('letters_to_draw')

    def payment_password_error_message(self, value):
        pvars = self.participant.vars
        practice = pvars.get('practice')
        
        if practice == False:
            if value != Constants.password_real:
                return "Please enter the correct password"

        if practice == True:
            if value != Constants.password_practice:
                return "Please enter the correct password"

    def vars_for_template(self):
        pvars = self.participant.vars
        practice = pvars.get('practice')
        n_practice = pvars.get('n_practice')
        choice_names_dic = pvars.get('letter_to_round_dic')
        choice_names = list(choice_names_dic.keys())

        print("this is the practice")
        print(pvars.get('practice'))
        #practice = self.session.config.get('practice')
        if practice == True:
            letters_to_draw = choice_names[0:n_practice]
        else:
            letters_to_draw = choice_names

        letters_to_draw = [s.replace("choice", "")
                           for s in letters_to_draw]
        pvars['letters_to_draw'] = letters_to_draw
        return {'letter_text': letters_to_draw,
                'practice': pvars.get('practice')}

    def before_next_page(self):
        pvars = self.participant.vars
        
        payoff_letter = self.player.random_letter
        pvars['payoff_letter_in']= payoff_letter
        
        
class paymentResults(Page):
    def vars_for_template(self):
        pvars = self.participant.vars

        round_dic = pvars["letter_to_round_dic"]
        choices_dic = pvars["choice_dic"]

        payoff_letter = pvars.get("payoff_letter_in")
        
        payoff_round_name = "choice{}".format(payoff_letter)
        allocation = choices_dic.get(payoff_round_name)
        other_allocation = pvars.get('endowment') - allocation
        
        info_dic = pvars.get("choice_param_dic")

        payoff_round_name = "choice{}".format(payoff_letter)
        payoff_round_info = info_dic.get(payoff_round_name)

        opt1 = payoff_round_info[0]
        opt2 = payoff_round_info[1]
        
        if opt1 == pvars.get('keep_text'):
            additional_earnings = allocation
            plus_minus_1 = "+"
            plus_minus_2 = "-"
        else:
            if opt2 == pvars.get('keep_text'):
                additional_earnings = other_allocation
                plus_minus_1 = "-"
                plus_minus_2 = "+"
            else:
                plus_minus_1 = plus_minus_2 = "-"
                additional_earnings = 0

        past_tense_dic = {pvars.get('keep_text'):
                          "{} {} ghs kept for yourself",
                          pvars.get('church_text'):
                          "{} {} ghs given to your church",
                          pvars.get('church_name_text'):
                          "{} {} ghs given to your church with your name",
                          pvars.get('street_text'):
                          "{} {} ghs given to the street children",
                          pvars.get('thanks_text'):
                          "{} {} ghs given to the thanksgiving offering"}
        
        opt1_text = opt1.format(allocation)
        opt2_text = opt2.format(other_allocation)

        opt1_text_past = past_tense_dic.get(opt1).format(plus_minus_1,
                                                         allocation)
        opt2_text_past = past_tense_dic.get(opt2).format(plus_minus_2,
                                                         other_allocation)

        showup_fee = pvars.get('showup_fee')
        
        total_earnings = showup_fee + additional_earnings
        total_earnings_text = "{} GHS".format(total_earnings)

        self.participant.payoff = total_earnings
        vdic = {'choice_letter': payoff_letter,
                'allocation': allocation,
                'option_1': opt1_text, 
                'option_2': opt2_text,
                'option_1_past': opt1_text_past, 
                'option_2_past': opt2_text_past,
                'final_payout': total_earnings,
                'total_earnings_text': total_earnings_text,
                'showup_fee': showup_fee,
                'practice': pvars.get('practice'),
                'practice_text':pvars.get('practice_text'),
                'letter_text': pvars.get('practice_letters')
        }
        
        return vdic

    
    def before_next_page(self):
        # After the first run of the results page, the practice
        # variable will be set to False
        print('practice should be changing here')
        self.participant.vars['practice'] = False
        
    class Meta:
        abstract = True

class Results(paymentResults):
    pass
            
page_sequence = [
    DrawRandom,
    Results
]
