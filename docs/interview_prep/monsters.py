class Monster:
    def __init__(self, health, energy):
        self.health = health
        self.energy = energy
        super().__init__(speed=10, has_scales=False)


m = Monster(health=100, energy=50)
