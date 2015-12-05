# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):

    form_model = models.Player
    form_fields = []

    def is_displayed(self):
        return self.subsession.round_number == 1        

class UnderstandingQuestions(Page):

    form_model = models.Player
    form_fields = ['understanding_question_1','understanding_question_2','understanding_question_3','understanding_question_4']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def understanding_question_1_error_message(self, value):
        if not (value == 22.5):
            return 'Hint: a total of $50 was contributed to the group. This amount will be multiplied by 1.8 and then divided evenly between the members of the group.'

    def understanding_question_2_error_message(self, value):
        if not (value == 32.0):
            return 'Hint: $108 will be divided evenly between the members of the group.'

    def understanding_question_3_error_message(self, value):
        if not (value == 14.0):
            return 'Hint: you begin with a $20 endowment, contribute $10, receive $5 back, and then sanction another group member at a cost of $1.'

    def understanding_question_4_error_message(self, value):
        if not (value == 10.0):
            return 'Hint: refer to the sixth bullet point in the directions above.'

class UnderstandingQuestionsWaitPage(WaitPage):
    def is_displayed(self):
        return self.subsession.round_number == 1

class Contribute(Page):

    form_model = models.Player
    form_fields = ['contribution']

class ContributeWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_preliminary_payoffs()

class Sanction(Page):
    form_model = models.Player
    form_fields = ['sanctions_rank_1','sanctions_rank_2','sanctions_rank_3','sanctions_rank_4']

class SanctionWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_final_payoffs()

class RoundResults(Page):
    pass

class MonetaryTreatmentExplanation(Page):
    def is_displayed(self):
        round_number = self.subsession.round_number
        treatment_group_1 = self.player.participant.vars['treatment_group_1']
        treatment_group_2 = self.player.participant.vars['treatment_group_2']
        treatment_group_3 = self.player.participant.vars['treatment_group_3']
        return (round_number in range(1,5) and treatment_group_1 == 'Monetary') or (round_number in range(5,9) and treatment_group_2 == 'Monetary') or (round_number in range(9,13) and treatment_group_3 == 'Monetary')

class CandyTreatmentExplanation(Page):
    def is_displayed(self):
        round_number = self.subsession.round_number
        treatment_group_1 = self.player.participant.vars['treatment_group_1']
        treatment_group_2 = self.player.participant.vars['treatment_group_2']
        treatment_group_3 = self.player.participant.vars['treatment_group_3']
        return (round_number in range(1,5) and treatment_group_1 == 'Candy') or (round_number in range(5,9) and treatment_group_2 == 'Candy') or (round_number in range(9,13) and treatment_group_3 == 'Candy')

class ControlExplanation(Page):
    def is_displayed(self):
        round_number = self.subsession.round_number
        treatment_group_1 = self.player.participant.vars['treatment_group_1']
        treatment_group_2 = self.player.participant.vars['treatment_group_2']
        treatment_group_3 = self.player.participant.vars['treatment_group_3']
        return (round_number in range(1,5) and treatment_group_1 == 'Control') or (round_number in range(5,9) and treatment_group_2 == 'Control') or (round_number in range(9,13) and treatment_group_3 == 'Control')

class FinalResults(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

class Questionnaire(Page):

    form_model = models.Player
    form_fields = ['questionnaire_1','questionnaire_2','questionnaire_3','questionnaire_4','questionnaire_5','questionnaire_6']

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def understanding_question_1_error_message(self, value):
        if not (value == 22.5):
            return 'Hint: a total of $50 was contributed to the group. This amount will be multiplied by 1.8 and then divided evenly between the members of the group.'

    def understanding_question_2_error_message(self, value):
        if not (value == 32.0):
            return 'Hint: $108 will be divided evenly between the members of the group.'

    def understanding_question_3_error_message(self, value):
        if not (value == 14.0):
            return 'Hint: you begin with a $20 endowment, contribute $10, receive $5 back, and then sanction another group member at a cost of $1.'

    def understanding_question_4_error_message(self, value):
        if not (value == 10.0):
            return 'Hint: refer to the sixth bullet point in the directions above.'

class Finished(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

page_sequence = [
	Introduction,
	# UnderstandingQuestions,
	# UnderstandingQuestionsWaitPage,
    ControlExplanation,
	MonetaryTreatmentExplanation,
	CandyTreatmentExplanation,
	Contribute,
    ContributeWaitPage,
    Sanction,
    SanctionWaitPage,
    RoundResults,
    FinalResults,
    Questionnaire,
    Finished
]