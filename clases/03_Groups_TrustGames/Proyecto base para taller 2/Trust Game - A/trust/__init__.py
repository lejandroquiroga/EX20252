from otree.api import *


doc = """
App para el juego de Trust
"""


class C(BaseConstants):
    NAME_IN_URL = 'trust'
    
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10000)
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    dinero_enviado = models.CurrencyField(
        min = 0,
        max = C.ENDOWMENT,
        label = "¿Cuánto dinero quiere enviar al jugador 2?"
    )
    dinero_devuelto = models.CurrencyField(
        label = "¿Cuánto dinero quiere devolver al jugador 1?"
    )


class Player(BasePlayer):
    pass


## FUNCTIONS
def dinero_devuelto_choices(group: Group):
    return currency_range(0, group.dinero_enviado * C.MULTIPLIER, 1)


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.ENDOWMENT - group.dinero_enviado + group.dinero_devuelto
    p2.payoff = group.dinero_enviado * C.MULTIPLIER - group.dinero_devuelto


# PAGES
class Instrucciones(Page):
    pass


class Enviar(Page):
    form_model = ""
    form_fields = ["dinero_enviado"]
    
    @staticmethod
    def is_displayed(player: Player):
        return 


class EsperaJ1(WaitPage):
    pass


class Devolver(Page):
    form_model = "group"
    form_fields = ["dinero_devuelto"]
    
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(dinero_multiplicado = (group.dinero_enviado * C.MULTIPLIER))


class EsperaJ2(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [Instrucciones, Enviar, EsperaJ1, Devolver, EsperaJ2, Results]
