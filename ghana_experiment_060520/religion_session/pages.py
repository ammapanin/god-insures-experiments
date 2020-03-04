from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


## Change after discussion with eva
## login page instructions

class DecisionInstructions(Page):
    form_model = 'player'
    form_fields = ["member_name"]
                   
    def vars_for_template(self):
        pvars = self.participant.vars
        practice = pvars.get('practice')
        
        if practice == True:
            n_questions = pvars.get('n_practice')
        else:
            n_questions = Constants.num_rounds
        
        return{"n_questions": n_questions,
               "practice": practice,
               "practice_text": Constants.practice_text} 

    def is_displayed(self):
        return self.round_number == 1
    
    def before_next_page(self):
        if self.round_number == 1:
            pvars = self.participant.vars
            pvars['member_name'] = self.player.member_name
        else:
            pass
        
class AllocationsPage(Page):
    form_model = 'player'
    form_fields = ['allocation']
  
    def vars_for_template(self):
        pvars = self.participant.vars
        practice = pvars.get("practice")
        round_dic = pvars["round_dic"]
              
        info_dic = pvars.get("choice_param_dic")
        choice_name = round_dic.get(self.round_number)

        self.player.choice_name = choice_name
        image_path_base = "religion_session/{}/give{}.png"
        image_idx_list = list(range(0, Constants.endowment + 1))

        image_keys = ["image{}".format(i) for i in image_idx_list]
        image_paths = [image_path_base.format(choice_name, i)
                       for i in image_idx_list]

        #02251849, Huawei
        choice_info = info_dic.get(choice_name)

        c1 = choice_info[0]
        c2 = choice_info[1]

        # Edit the text of named giving to include the player
        # name
        member_name = pvars.get('member_name')

        if c1 == Constants.church_named_text:
            c1 = c1 + " ({})".format(member_name)
            
        if c2 == Constants.church_named_text:
                c2 = c2 + " ({})".format(member_name)

        allocations = [(c1.format(x).capitalize(),
                        c2.format((Constants.endowment - x)))
                       for x in image_idx_list]
        allocation_keys = ["allocation{}".format(i)
                           for i in image_idx_list]

        # Build the dictionary
        vars_dic = dict(zip(image_keys, image_paths))
        allocation_dic = dict(zip(allocation_keys, allocations))
    
        vars_dic.update(allocation_dic)

        vars_dic.update({"practice": practice,
                         "question_number":
                         "Q{}.".format(self.round_number)})
        return vars_dic
    
    def is_displayed(self):
        # Ensure that the correct number of pages are shown
        # for the practice rounds
        pvars = self.participant.vars
        practice = pvars.get('practice')
        
        if practice == True:            
            return self.round_number <= Constants.n_practice
        else:
            return True

    def before_next_page(self):
        round_dic = self.participant.vars["round_dic"]
        cdic = self.participant.vars["choice_dic"]
        
        round_name = round_dic.get(self.round_number)
        cdic.update({round_name:self.player.allocation})


page_sequence = [
    DecisionInstructions,
    AllocationsPage,
]
