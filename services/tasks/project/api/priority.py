from flask import current_app
import json



class Priority(object):
    def __init__(self):
        pass
    
    def rice_formula(self, elements):
        R = elements['reach']
        I = elements['impact']
        C = elements['confidence']
        E = elements['effort']
        return (R*I*C)/E

    def calculate_priority(self, elements):
        return self.rice_formula(elements)


        
