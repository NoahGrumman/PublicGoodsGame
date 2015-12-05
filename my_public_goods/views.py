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
    form_fields = ['understanding_question_1','understanding_question_2','understanding_question_3','understanding_question_4','understanding_question_5','understanding_question_6']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def understanding_question_1_error_message(self, value):
        if not (value == 20):
            return 'Hint: a total of $40 was contributed to the group. This amount will be multiplied by 2 and then divided evenly between the members of the group.'

    def understanding_question_2_error_message(self, value):
        if not (value == 20):
            return 'Hint: refer to the previous question.'

    def understanding_question_3_error_message(self, value):
        if not (value == 0):
            return 'Hint: a total of $0 was contributed to the group. This amount will be multiplied by 2 and then divided evenly between the members of the group.'

    def understanding_question_4_error_message(self, value):
        if not (value == 10.0):
            return 'Hint: since no one contributed to the group, each group member will receive the amount of their initial endowment.'

    def understanding_question_5_error_message(self, value):
        if not (value == 1):
            return 'Hint: refer the instructions above.'

    def understanding_question_6_error_message(self, value):
        if not (value == 3):
            return 'Hint: refer to the instructions above.'

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

class Questionnaire(Page):

    form_model = models.Player
    form_fields = ['questionnaire_1','questionnaire_2','questionnaire_3','questionnaire_4','questionnaire_5','questionnaire_6']

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

class Finished(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

page_sequence = [
	Introduction,
	UnderstandingQuestions,
	UnderstandingQuestionsWaitPage,
    ControlExplanation,
	MonetaryTreatmentExplanation,
	CandyTreatmentExplanation,
	Contribute,
    ContributeWaitPage,
    Sanction,
    SanctionWaitPage,
    RoundResults,
    Questionnaire,
    Finished
]