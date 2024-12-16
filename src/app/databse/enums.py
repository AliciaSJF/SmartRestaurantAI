from enum import Enum

class MenuCategory(str, Enum):
    ANTIPASTI = "antipasti"
    PRIMI_PIATTI = "primi piatti"
    SECONDI_PIATTI = "secondi piatti"
    DOLCI = "dolci"
    BEVANDE = "bevande"  