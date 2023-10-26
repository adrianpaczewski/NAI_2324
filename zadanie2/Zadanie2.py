# Author: Kamil Kornatowski
# Author: Adrian Paczewski
"""
Szacowana wartość nieruchomości
-------------------
Nasz program stosuje Fuzzy Logic by korzystając z kilku cech oszacować wartość nieruchomości.
Cechy, o które się opieramy:
* Inputy
   - area, czyli całkowita powierzchnia nieruchomości. Zastosowane stopnie w fuzzy logic przyjmują wartość
     od 20 do 120 i stopnie poor, mediocre, average, decent, good
   - number of rooms, czyli liczba pomieszczeń, na które podzielona jest nieruchomość w momencie szacowania.
     Zastosowane stopnie przyjmują wartość od 1 do 5 i takie stopnie przyjmują.
   - communication, czyli ogólnie określony stopień skomunikowania nieruchomości (rozumiany jako łatwość
     dostępu do przystanków autobusowych, SKM, dojazd autem i tym podobne). Przyjmujemy trzy stopnie, bad,
     average i good
* Outputy
   - wartość nieruchomości, przyjmuje wartości liczbowe, mniej więcej od 150 000 do 1 500 000. Zestaw fuzzy
     logic określa stopnie Lowest, Lower, Low, Average, High, Higher, Highest

* Zasady
   - Nieruchomość ma optymalną liczbę pokoi zależnie od powierzchni ( area ). Jednopokojowa kawalerka jest
     czymś normalnym i wygodnym, ale większe mieszkanie ze zbyt małą liczbą pomieszczeń to problem
   - Stopień skomunikowania potrafi podnieść cenę mniej atrakcyjnej nieruchomości, lecz od pewnego etapu duża
   powierzchnia narzuca rosnącą cenę.
"""
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

area = ctrl.Antecedent(np.arange(20, 120, 2), 'area')
number_of_rooms = ctrl.Antecedent(np.arange(1, 6, 1), 'number of rooms')
communication = ctrl.Antecedent(np.arange(1, 4, 1), 'communication')
value = ctrl.Consequent(np.arange(150000, 1500000, 30000), 'value')
area.automf(5)
rooms = ['1', '2', '3', '4', '5']
number_of_rooms.automf(names=rooms)
communication_level = ['bad', 'average', 'good']
communication.automf(names=communication_level)
value['lowest'] = fuzz.trimf(value.universe, [150000, 150000, 200000])
value['lower'] = fuzz.trimf(value.universe, [200000, 300000, 400000])
value['low'] = fuzz.trimf(value.universe, [400000, 600000, 800000])
value['average'] = fuzz.trimf(value.universe, [600000, 800000, 1000000])
value['high'] = fuzz.trimf(value.universe, [800000, 1000000, 1200000])
value['higher'] = fuzz.trimf(value.universe, [1200000, 1300000, 1400000])
value['highest'] = fuzz.trimf(value.universe, [1400000, 1500000, 1500000])

'''Zestaw reguł rządzących programem. Zgodnie z syntaxem wykorzystywanej biblioteki podajemy wszystkie reguły, które doprowadzają do określonego outputu'''
rule1 = ctrl.Rule(antecedent=
                  # Area = poor
                  ((area['poor'] & number_of_rooms['1'] & communication['bad']) |
                   (area['poor'] & number_of_rooms['2'] & communication['bad']) |
                   (area['poor'] & number_of_rooms['2'] & communication['average']) |
                   (area['poor'] & number_of_rooms['2'] & communication['good']) |
                   (area['poor'] & number_of_rooms['3'] & communication['bad']) |
                   (area['poor'] & number_of_rooms['3'] & communication['average']) |
                   (area['poor'] & number_of_rooms['3'] & communication['good']) |
                   (area['poor'] & number_of_rooms['4'] & communication['bad']) |
                   (area['poor'] & number_of_rooms['4'] & communication['average']) |
                   (area['poor'] & number_of_rooms['4'] & communication['good']) |
                   (area['poor'] & number_of_rooms['5'] & communication['bad']) |
                   (area['poor'] & number_of_rooms['5'] & communication['average']) |
                   (area['poor'] & number_of_rooms['5'] & communication['good'])),
                  consequent=value['lowest'])

rule2 = ctrl.Rule(antecedent=(
    # Area = poor

        (area['poor'] & number_of_rooms['1'] & communication['average']) |
        (area['poor'] & number_of_rooms['1'] & communication['good']) |

        # Area = mediocre
        (area['mediocre'] & number_of_rooms['5'] & communication['bad']) |
        (area['mediocre'] & number_of_rooms['5'] & communication['average'])),
    consequent=value['lower'])

rule3 = ctrl.Rule(antecedent=((area['mediocre'] & number_of_rooms['1'] & communication['bad']) |
                              (area['mediocre'] & number_of_rooms['3'] & communication['bad']) |
                              (area['mediocre'] & number_of_rooms['3'] & communication['average']) |
                              (area['mediocre'] & number_of_rooms['3'] & communication['good']) |
                              (area['mediocre'] & number_of_rooms['4'] & communication['bad']) |
                              (area['mediocre'] & number_of_rooms['4'] & communication['average']) |
                              (area['mediocre'] & number_of_rooms['4'] & communication['good']) |
                              (area['mediocre'] & number_of_rooms['5'] & communication['bad']) |
                              (area['mediocre'] & number_of_rooms['5'] & communication['average']) |
                              (area['mediocre'] & number_of_rooms['5'] & communication['good'])),
                  consequent=value['low'])

rule4 = ctrl.Rule(antecedent=(
    # Area(mediocre)
        (area['mediocre'] & number_of_rooms['1'] & communication['average']) |
        (area['mediocre'] & number_of_rooms['1'] & communication['good']) |
        (area['mediocre'] & number_of_rooms['2'] & communication['average']) |
        (area['mediocre'] & number_of_rooms['2'] & communication['good']) |

        # Area(average)
        (area['average'] & number_of_rooms['1'] & communication['bad']) |
        (area['average'] & number_of_rooms['1'] & communication['average']) |
        (area['average'] & number_of_rooms['2'] & communication['bad']) |
        (area['average'] & number_of_rooms['4'] & communication['bad']) |
        (area['average'] & number_of_rooms['4'] & communication['average']) |
        (area['average'] & number_of_rooms['4'] & communication['good']) |
        (area['average'] & number_of_rooms['5'] & communication['bad']) |
        (area['average'] & number_of_rooms['5'] & communication['average']) |
        (area['average'] & number_of_rooms['5'] & communication['good'])),
    consequent=value['average'])
rule5 = ctrl.Rule(antecedent=(
    # Area(average)
        (area['average'] & number_of_rooms['1'] & communication['good']) |
        (area['average'] & number_of_rooms['2'] & communication['average']) |
        (area['average'] & number_of_rooms['2'] & communication['good']) |
        (area['average'] & number_of_rooms['3'] & communication['bad']) |
        (area['average'] & number_of_rooms['3'] & communication['average']) |
        (area['average'] & number_of_rooms['3'] & communication['good']) |
        # Area(decent)
        (area['decent'] & number_of_rooms['1'] & communication['bad']) |
        (area['decent'] & number_of_rooms['1'] & communication['average']) |
        (area['decent'] & number_of_rooms['2'] & communication['bad']) |
        (area['decent'] & number_of_rooms['2'] & communication['average']) |
        (area['decent'] & number_of_rooms['3'] & communication['bad']) |
        (area['decent'] & number_of_rooms['5'] & communication['bad']) |
        (area['decent'] & number_of_rooms['5'] & communication['average']) |
        (area['decent'] & number_of_rooms['5'] & communication['good']) |
        # Area(good)
        (area['good'] & number_of_rooms['2'] & communication['bad']) |
        (area['good'] & number_of_rooms['2'] & communication['average']) |
        (area['good'] & number_of_rooms['2'] & communication['good']) |
        (area['good'] & number_of_rooms['3'] & communication['average'])),
    consequent=value['high'])

rule6 = ctrl.Rule(antecedent=(
    # Area(decent)
        (area['decent'] & number_of_rooms['1'] & communication['good']) |
        (area['decent'] & number_of_rooms['2'] & communication['good']) |
        (area['decent'] & number_of_rooms['3'] & communication['average']) |
        (area['decent'] & number_of_rooms['3'] & communication['good']) |
        (area['decent'] & number_of_rooms['4'] & communication['bad']) |
        (area['decent'] & number_of_rooms['4'] & communication['average']) |
        (area['decent'] & number_of_rooms['4'] & communication['good']) |

        # Area(good)
        (area['good'] & number_of_rooms['1'] & communication['bad']) |
        (area['good'] & number_of_rooms['1'] & communication['average']) |
        (area['good'] & number_of_rooms['1'] & communication['good']) |
        (area['good'] & number_of_rooms['2'] & communication['bad']) |
        (area['good'] & number_of_rooms['2'] & communication['average']) |
        (area['good'] & number_of_rooms['2'] & communication['good']) |
        (area['good'] & number_of_rooms['3'] & communication['bad']) |
        (area['good'] & number_of_rooms['3'] & communication['average']) |
        (area['good'] & number_of_rooms['3'] & communication['good']) |
        (area['good'] & number_of_rooms['4'] & communication['bad']) |
        (area['good'] & number_of_rooms['4'] & communication['average']) |
        (area['good'] & number_of_rooms['4'] & communication['good'])),
    consequent=value['higher'])
rule7 = ctrl.Rule(antecedent=(
    # Area(good)
        (area['good'] & number_of_rooms['5'] & communication['bad']) |
        (area['good'] & number_of_rooms['5'] & communication['average']) |
        (area['good'] & number_of_rooms['5'] & communication['good'])
)
    ,
    consequent=value['highest'])
value_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
valuation = ctrl.ControlSystemSimulation(value_ctrl)
valuation.input['area'] = 105
valuation.input['number of rooms'] = 4
valuation.input['communication'] = 3
valuation.compute()
result = "Szacowana wartość nieruchomości: {:,.2f} PLN".format(valuation.output['value'])
print(result)
value.view(sim=valuation)
plt.show()