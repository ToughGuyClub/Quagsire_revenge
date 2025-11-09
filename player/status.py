class Status:
    def __init__(self, health=100, mana=50, stamina=75):
        self.health = health
        self.mana = mana
        self.stamina = stamina

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def heal(self, amount):
        self.health += amount

    def use_mana(self, amount):
        if amount <= self.mana:
            self.mana -= amount
            return True
        return False

    def recover_stamina(self, amount):
        self.stamina += amount