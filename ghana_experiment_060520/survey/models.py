from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from religion_session.models import Constants as generalConstants
from django import forms
import random

author = 'Amma Panin'

doc = """
Survey for Ghana sessions
"""


church_reasons_list = ['The teaching about God corresponds to what I believe in',
                  'I go for the moral guidance to me and my family',
                  'I like the atmosphere of the services',
                  'Friends or relatives brought me there',
                  'Other members made an effort to welcome me',
                  'The congregation contains many interesting and successful people',
                  'I hope to meet a good marriage partner for me or my children',
                  'The building is close to my home',
                'The facilities are comfortable (e.g. airconditioning, comfortable seating, etc.)']

church_reasons_options = tuple([(i, x)
                                for i, x in enumerate(church_reasons_list)])


ministries_list = ['Ushering or welcoming guests',
           "Children's ministry",
           'Praise, worship, or choir',
           'Prayer ministry',
           "Men or women's ministry",
           'Youth ministry',
           'Outreach',
           'Deacon or deaconess',
           'Protocol',
           'Pastoring',
           'Bible study or Home fellowship']

ministries_options = tuple([(i, x)
                            for i, x in enumerate(ministries_list)])


convince_list = ['Preaching or teaching in the church',
                'Preaching or teaching outside the church',
                'Inviting friends or family to church',
                'Distributing church material in public',
                'Speaking or writing in public media (newspapers, radio, television, etc.)',
                'Prayer']

convince_options = tuple([(i, x)
                          for i, x in enumerate(convince_list)])


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    showup_fee = generalConstants.showup_fee
    endowment = generalConstants.endowment
    
    income_options = ['0',
                      'Less than 50',
                      '50 to 100',
                      '100 to 150',
                      '150 to 200',
                      '200 to 250',
                      '250 to 300',
                      '300 to 350',
                      '350 to 400',
                      '400 to 450',
                      '450 to 500',
                      '500 to 600',
                      '600 to 700',
                      '700 to 800',
                      '800 to 900',
                      '900 to 1000',
                      'More than 1000']
    
    take_care = ["{} people".format(i)
                 for i in list(range(0, 5))] + ['More than 5']

    church_activity_time = ['Less than 1 hour',
                            '1 to 3 hours',
                            '3 to 5 hours',
                            'more than 5 hours']

    church_giving = ['Less than 5',
                     '5 to 10',
                     '10 to 15',
                     '15 to 20',
                     '20 to 25',
                     '25 to 30',
                     '30 to 35',
                     '35 to 40',
                     '40 to 45',
                     '45 to 50',
                     '50 to 55',
                     '55 to 60',
                     'More than 60']

    expenditure_options = ['0',
                           'Less than 5',
                           '5 to 10',
                           '10 to 15',
                           '15 to 20',
                           '20 to 25',
                           '25 to 30',
                           '30 to 35',
                           '35 to 40',
                           '40 to 50',
                           '50 to 60',
                           '60 to 70',
                           '70 to 80',
                           '80 to 90',
                           '90 to 100',
                           '100 to 110',
                           '110 to 120',
                           'More than 120']
    
    yes = ["Yes", "No"]

    aog_list = ["The Glory Assemblies of God",
                "Agape Assemblies of God",
                "Crossway Assemblies of God",
                "Maranatha Assemblies of God",
                "Central Assemblies of God",
                "Calvary Assemblies of God",
                "Grace Assemblies of God"] + ['Other']

    ministry_hours = ['Less than 1 hour',
                      '1-3 hours',
                      '3-5 hours',
                      'more than 5 hours']

    help_options = tuple(
        [(i, x)
         for i, x in enumerate(['No one',
                                'Government or NGO social services',
                                'Friends',
                                'Family',
                                'Pastor',
                                'Imam',
                                'Church member',
                                'Work superior',
                                'Medical professional',
                                'Bank or other financial institution'])])
    
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    age = models.IntegerField(
        label='How old are you?',
        min=18, max=75)

    gender = models.StringField(
        choices=['Male', 'Female', 'Other'],
        label='What is your gender?',
        widget=widgets.RadioSelect)

    activity = models.StringField(
        choices=['Unemployed', 'Student', 'Civil servant', 'Agriculture', 'Shopkeeper', 'Private sector', 'Other'],
        label='What is your principle activity?',
        widget=widgets.RadioSelect)

    birthplace = models.StringField(
        choices=['Accra', 'Rural Ghana', 'Urban Ghana', 'Outside Ghana in Africa', 'Outside Africa'],
        label='Where were you born?',
        widget=widgets.RadioSelect)

    accra = models.StringField(
        choices=['Whole life',
                 'More than 10 years',
                 '5 to 10 years',
                 '2 to 5 years',
                 'Less than 2 years'],
        label='How long have you lived in Accra',
        widget=widgets.RadioSelect)

    married = models.StringField(
        choices=['Single', 'Married', 'Widowed', 'Divorced'],
        label='Are you married?',
        widget=widgets.RadioSelect)
        
    ethnicity = models.StringField(
        choices=['Akan', 'Ewe', 'Ga Adangbe', 'Dagbani', 'Other'],
        label='What is your ethnic group?',
        widget=widgets.RadioSelect)

    education = models.StringField(
        choices=['No schooling', 'Primary', 'JHSS', 'SHS', 'Polytechnic', 'Professional degree', 'First degree', 'Advanced degree'
],
        label='What is the highest level of education you have completed?',
        widget=widgets.RadioSelect)

    left_ghana = models.StringField(
       choices=['Yes', 'No'],
        label='As an adult, have you ever left Ghana for more than 3 months for work or study?',
        widget=widgets.RadioSelect)
    
    left_ghana_location  = models.StringField(
        label='Where did you go?',
        blank = True)
     
    work_status = models.StringField(
        choices=['Student',
                 'Unemployed or casual worker',
                 'Employed', 'Self-employed',
                 'Inactive(e.g. housewife)',
                 'Retired'],
        label='What is your current work status?',
        widget=widgets.RadioSelect)


    work_sector = models.StringField(
        choices=['Unemployed',
                 'Student',
                 'Government',
                 'Agriculture',
                 'Services',
                 'Manufacturing or construction',
                 'Not-for-profit'],
        label='In which sector is your principal ativity?',
        widget=widgets.RadioSelect)

    income_source = models.StringField(
        choices=['Salaried job',
                 'Entrepreneur',
                 'Family',
                 'Pension',
                 'Social support'],
        label = 'What is your principal source of income?',
        widget = widgets.RadioSelect)
    
    income_individual = models.StringField(
        choices= Constants.income_options,
        label = 'How much do you individually earn per month in GHS?',
        widget = widgets.Select)

    income_household = models.StringField(
        choices= Constants.income_options,
        label = 'How much does your household earn per month in GHS?',
        widget = widgets.Select)

    financial_decisions = models.StringField(
        choices = ['Me',
                   'Spouse',
                   'Parent',
                   'Other senior relative',
                   'Joint decisions incl. me',
                   'Joint decisions not incl. me'],
        label = 'Who usually makes the final financial decisions in your household?',
        widget = widgets.RadioSelect)
    
    minor_care = models.StringField(
        choices = Constants.take_care,
        label = 'How many minor children do you take care of financially?',
        widget = widgets.Select)

    minor_care_live = models.StringField(
        choices = Constants.take_care,
        label = 'How many of those minor children that you take care of live with you?', 
        widget = widgets.Select,
        blank = True)

    adult_care = models.StringField(
        choices = Constants.take_care,
        label = 'How many adults do you take care of financially?',
        widget = widgets.Select)

    adult_care_live = models.StringField(
        choices = Constants.take_care,
        label = 'How many of those adults that you take care of live with you?', 
        widget = widgets.Select,
        blank = True)

    elderly_parent_care = models.StringField(
        choices = Constants.take_care,
        label = 'How many elderly parents do you take care of financially?',
        widget = widgets.Select)

    elderly_parent_care_live = models.StringField(
        choices = Constants.take_care,
        label = 'How many of those elderly parents that you take care of live with you?', 
        widget = widgets.Select)

    other_family_care_care = models.StringField(
        choices = Constants.take_care,
        label = 'How many other family members (not children or elderly parents) do you take care of financially?',
        widget = widgets.Select,
    blank = True)

    
    other_family_care_care_live = models.StringField(
        choices = Constants.take_care,
        label = 'How many of those other family members (not children or elderly parents) that you take care of live with you?', 
        widget = widgets.Select,
        blank = True)

    food_weekly = models.StringField(
        choices = Constants.expenditure_options,
        label = 'How much do you usually spend on food per week?', 
        widget = widgets.Select)

    transport_weekly = models.StringField(
        choices = Constants.expenditure_options,
        label = 'How much do you usually spend on transport per week?', 
        widget = widgets.Select)

    sickness_weekly = models.StringField(
        choices = Constants.expenditure_options,
        label = 'How much do you usually spend on sickness per year?', 
        widget = widgets.Select)

    social_contributions_weekly = models.StringField(
        choices = Constants.expenditure_options,
        label = 'How much do you usually spend on social contributions (e.g. pledge to a school or charity)  week?', 
        widget = widgets.Select)

    microfinance_weekly = models.StringField(
        choices = Constants.expenditure_options,
        label = 'How much do you usually spend on microfinance or susu per week?', 
        widget = widgets.Select)

    utilities_weekly = models.StringField(
        choices = Constants.expenditure_options,
        label = 'How much do you usually spend on utilities per week?', 
        widget = widgets.Select)

    business_investment = models.StringField(
        choices = Constants.income_options,
        label = 'How much have you spent in business investments (your own or others) in the last year in Ghana cedis?',
        widget = widgets.Select)

    business_ownership = models.StringField(
        choices = Constants.yes,
        label = 'Do you own a business?',
        widget = widgets.RadioSelect)


    business_length = models.StringField(
        choices = ['Less than 1 year',
                   '1 to 3 years',
                   '3 to 10 years',
                   'More than 10 years'],
        label = 'How many years have you owned your business?',
        widget = widgets.RadioSelect,
        blank = True)
    
    business_employees = models.StringField(
        choices = ["{} employees".format(i)
                   for i in list(range(0, 10))] + ["More than 10"],
        label = 'How many employees do you  have?',
        blank = True)

    religion = models.StringField(
        choices = ['Pentecostal or charismatic Christian',
                   'Catholic Christian',
                   'Traditional',
                   'Protestant Christian',
                   'Muslim',
                   'No religion'],
        label = 'Which religion do you belong to?',
        widget = widgets.RadioSelect)

    religion_birth = models.StringField(
        choices = Constants.yes,
        label = 'Were you born into this religion?',
        widget = widgets.RadioSelect)

    denomination = models.StringField(
        choices = Constants.aog_list,
        label = 'Which denomination do you belong to?',
        widget = widgets.RadioSelect)

    denomination_other = models.StringField(
        choices = Constants.aog_list,
        label = ('If you belong to another denomination, please'
                 ' state which one'))

    different_church = models.StringField(
        choices = ['No',
                   'Yes, I changed within the last 5 years' ,
                   'Yes, I changed more than 5 years ago',
                   'I have always been in this church'],
        label = 'Is this the same church you attended 5 years ago?',
        widget = widgets.RadioSelect)

    church_reasons = models.StringField(
        label = 'What are the main reasons you are with your current church? (Please check all that apply).',
        widget = forms.CheckboxSelectMultiple(choices = church_reasons_options))

    church_assistance = models.StringField(
        choices = Constants.yes,
        label = 'Have you received financial assistance from your church in the last 2 years (incl. provisions)?',
        widget = widgets.RadioSelect)

    church_attendance = models.StringField(
        choices = ['Less than once a year',
                   'A few times per year',
                   'A few times per month',
                   'Weekly',
                   'More than once per week',
                   'Daily'],
        label = 'How many times per week or per year do you attend your church?')
        
    ministries = models.StringField(
        label = 'Are you engaged in any of the following ministries of your church?',
        blank = True,
        widget = forms.CheckboxSelectMultiple(choices = ministries_options))

    ministry_hours_usher = models.StringField(
        choices =  Constants.church_activity_time,
        label = "How many hours a week do you spend on Ushering or welcoming guests?",
        widget = widgets.RadioSelect,
        blank = True)

    ministry_hours_children = models.StringField(
        choices =  Constants.church_activity_time,
        label = "How many hours a week do you spend on Children's ministry?",
        widget = widgets.RadioSelect,
        blank = True)

    ministry_hours_praise = models.StringField(
        choices =  Constants.church_activity_time,
        label = "How many hours a week do you spend on 'Praise, worship, or choir'",
        widget = widgets.RadioSelect,
    blank = True)

    ministry_hours_prayer = models.StringField(
        choices = Constants.church_activity_time,
        label = "How many hours a week do you spend on Prayer ministry?",
        widget = widgets.RadioSelect,
    blank = True)

    
    ministry_hours_men_women = models.StringField(
        choices = Constants.church_activity_time,
        label = "How many hours a week do you spend on Men or Women's ministry?",
        widget = widgets.RadioSelect,
    blank = True)

    ministry_hours_youth = models.StringField(
        choices = Constants.church_activity_time,
        label = "How many hours a week do you spend on the Youth ministry?",
        widget = widgets.RadioSelect,
    blank = True)
    
    ministry_hours_outreach = models.StringField(
        choices = Constants.church_activity_time,
        label = "How many hours a week do you spend on Outreach?",
        widget = widgets.RadioSelect,
    blank = True)
    
    ministry_hours_deaconess = models.StringField(
            choices = Constants.church_activity_time,
        label = "How many hours a week do you spend on being Deacon or deaconess?",
        widget = widgets.RadioSelect,
    blank = True)

    ministry_hours_protocol = models.StringField(
        choices = Constants.church_activity_time,
        label = "How many hours a week do you spend on the Protocol ministry?",
        widget = widgets.RadioSelect,
        blank = True)

    ministry_hours_pastoring = models.StringField(
        choices = Constants.church_activity_time,
        label = "How many hours a week do you spend on Pastoring",
        widget = widgets.RadioSelect,
    blank = True)

    ministry_hours_bible_study = models.StringField(
        choices = Constants.church_activity_time,
        label = "How many hours a week do you spend on Bible study or Home fellowship?",
        widget = widgets.RadioSelect,
    blank = True)

    church_length = models.StringField(
        choices = Constants.church_activity_time,
        label = "On average, how many hours do you spend each time you visit your church? (e.g duration of a service, prayer meeting, etc.)'?",
        widget = widgets.RadioSelect)
   
    church_distance = models.StringField(
        choices = ['Less than 30 minutes',
                   '30 minutes to 1 hour',
                   'More than 1 hour'],
        label = "How many hours do you travel (going and coming) to attend regular services?",
        widget = widgets.RadioSelect)
    
    church_move = models.StringField(
        choices = Constants.yes,
        label = "Have you moved your place of residence in order to be closer to your church?",
        widget = widgets.RadioSelect)
    
    church_convince = models.StringField(
        label = "In the last 6 weeks, have you engaged in any of the following activities to bring others to your church",
        blank = True,
        widget = forms.CheckboxSelectMultiple(choices = convince_options))
    
    pray = models.StringField(
        label = 'How often do you pray to God?',
        choices = ['Multiple times per day',
                   'Once per day',
                   'A few times per week',
                   'Occasionally'],
        widget = widgets.RadioSelect)

    food = models.StringField(
        label = 'Are there any foods you do not eat for religious reasons?',
        choices = Constants.yes,
        widget = widgets.RadioSelect)
    
    alcohol = models.StringField(
        label = 'Do you drink alcohol?',
        choices = Constants.yes,
        widget = widgets.RadioSelect)

    alcohol_reasons = models.StringField(
        label = 'Is this decision for religious reasons?',
        choices = Constants.yes,
        widget = widgets.RadioSelect)
    
    newborn = models.StringField(
        blank = True,
        label = ('Which of the following ceremonies have '
                 'you done or would you do for your newborn'
                 ' child? (Please check all that apply)'),
        widget = forms.CheckboxSelectMultiple(
            choices = tuple(
                [(i, x)
                 for i, x in enumerate(['Traditional naming',
                                     'Church blessing',
                                     'Baptism',
                                     'Outdooring party',
                                     'Nothing'])]))
    )
    
    family_death = models.StringField(
        label = 'What was the main cause of the most recent death in your extended family?',
        choices = ['Accident',
                   'Illness',
                   'Violence',
                   'Old age',
                   'Other'],
        widget = widgets.RadioSelect)

    spiritual_attack = models.StringField(
        label = 'Do you think there was a spiritual element involved?',
        choices = Constants.yes, 
        widget = widgets.RadioSelect)
    
    church_giving = models.StringField(
    label = 'How much on average do you give to the church per week in ghana cedis?',
        choices = Constants.church_giving, 
        widget = widgets.Select)
    
    tithes = models.StringField(
        label = 'Have you already paid tithes this month?',
        choices = ['Yes',
                   'No',
                   'I do not regularly pay tithes'],
        widget = widgets.RadioSelect)
    
    church_debt = models.StringField(
        label = 'Have you ever gone into debt to pay a church pledge?',
        choices = Constants.yes,
        widget = widgets.RadioSelect)
    
    charity = models.StringField(
        label = 'Does giving to charity serve the same spiritual duty as giving directly to your church?',
        choices = ['No, charity is more important',
                   'No, charity is less important',
                   'Yes, they are equally important',
                   'I do not think I have a duty to either.'],
        widget = widgets.RadioSelect)
    

    god_finances = models.StringField(
        label = 'How is God involved in your finances?',
        choices = ['God leaves me to run my own financial affairs',
                   'God provides enough that I do not suffer',
                   'God blesses me with financial abundance',
                   'God is not interested in my finances'],
        widget = widgets.RadioSelect)
    
    close_friends = models.StringField(
        label = 'Is it important for you that your close friends come from the same church as you?',
        choices = ['Yes, I try to only make friends with people from my church',
                   'Yes, I try to seek people from my church but it is not so important',
                   'No, it is not important at all',
                   'No, I prefer not to be friends with people from my church'],
        widget = widgets.RadioSelect)
    
    coworkers = models.StringField(
        label = 'Is it important that your coworkers come from the same church as you?',
        choices = ['Yes, I try to only seek work with people from my church',
                   'Yes, I try to seek work with people from my church or but it is not so important',
                   'No, it is not important at all',
                   'No, I prefer not to work with people from my church'],
        widget = widgets.RadioSelect)
   
    business_partners = models.StringField(
        label = 'Do you try to do business with people from the same church?',
        choices = ['Yes, I try to only do business with people from my church',
                   'Yes, I try to do business with people from my church but it is not so important',
                   'No, it is not important at all',
                   'No, I prefer not to do business with  people from my church'],
        widget = widgets.RadioSelect)
   
   
    help_family = models.StringField(
        label = 'Who do you call when you need counselling about personal or family issues?',
        widget = forms.CheckboxSelectMultiple(
            choices = Constants.help_options))
   
    help_financial = models.StringField(
        label = 'Who would you go to for financial help (e.g a loan, or money in an emergency)?',
        widget = forms.CheckboxSelectMultiple(
            choices = Constants.help_options))

    help_health = models.StringField(
        label = 'Who do you go to for medical support when you are sick?',
            widget = forms.CheckboxSelectMultiple(
            choices = Constants.help_options))
   
    prayercamp = models.StringField(
        label = 'Within the last 2 years, have you ever attended a prayer camp either for yourself or on behalf of a friend or family member?',
        choices = Constants.yes,
        widget = widgets.RadioSelect)

    clubs = models.StringField(
    label = 'Which other clubs or associations are you an active member of?')
        
    political_taxes = models.StringField(
        label = 'You have money and you are willing to support a national developmental project. Who will you give it to?',
        choices = ['Government controlled by NPP',
                   'Government controlled by NDC',
                   'Another party other than NDC or NPP',
                   'Any government in power',
                   'I prefer to give money directly to my church',
                   'I prefer to keep money for my own business'],
        widget = widgets.RadioSelect)

    spouse = models.StringField(
        label = 'How did you meet your spouse if you are married? Where is the most likely place you will meet your spouse if you are not married?',
        choices =["Church",
                  "Through friends",
                  "Through family",
                  "Through work",
                  "Through school",
                  "Other social gathering 6 Internet",
                  "Other"])
   
    trust_ghana = models.StringField(
        label = 'Generally speaking, would you say other Ghanaians can be trusted?',
        choices = ['People can almost always be trusted',
                   'People can usually be trusted',
                   'You usually cannot be too careful dealing with people',
                   'You always cannot be too careful dealing with people'],
        widget = widgets.RadioSelect)
    
    trust_ghana_govt = models.StringField(
        label = 'Generally speaking, would you say the Ghanaian government can be trusted?',
        choices = ["I always trust the government",
                   "I mostly trust the government",
                   "I mostly mistrust the government",
                   "I always mistrust the government"],
        widget = widgets.RadioSelect)
    
    
    nih = models.StringField(
        label = 'Are you registered for the National Health Insurance Scheme?',
        choices = Constants.yes,
        widget = widgets.RadioSelect)
    
    nih_reason = models.StringField(
        label = 'Why not?',
        blank = True)
    
    other_insurance = models.StringField(
        label = 'Do you hold any other sorts of insurance?',
        choices = Constants.yes,
        widget = widgets.RadioSelect)
    
    other_insurance_specify = models.StringField(
        label = 'Please specify which ones, including the type (e.g life insurance, car insurance, etc.)',
        blank = True)
        




    
 
    
    


