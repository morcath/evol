import math
import random
import pygame

WIDTH = 720
HEIGHT = 480
BLUE = (66, 135, 245)
RED = (245, 93, 66)

display = pygame.display.set_mode((WIDTH, HEIGHT))


class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = RED

    def draw(self):
        pygame.draw.circle(display, self.color, (self.x, self.y), 5)


class Individual(Unit):
    def __init__(self, strategy):
        super().__init__(0, 0)
        self.step = 0
        self.strategy = strategy
        self.color = BLUE

    def make_step(self):
        self.x += self.strategy[self.step][0]
        self.y += self.strategy[self.step][1]
        self.step += 1

    def distance(self, x_target, y_target):
        return math.sqrt(abs(x_target - self.x) ** 2 + abs(y_target - self.y) ** 2)


class Population:
    def __init__(self):
        self.size = 120
        self.number_of_steps = 12000
        self.individuals = self.create_first_generation()
        self.mutation_chance = 0.1

    def create_first_generation(self):
        first_generation = []
        for _ in range(self.size):
            strategy = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(self.number_of_steps)]
            first_generation.append(Individual(strategy))
        return first_generation

    @staticmethod
    def crossover(parent_1, parent_2):
        child_strategy = []
        for s1, s2 in zip(parent_1.strategy, parent_2.strategy):
            if random.uniform(0, 1) > 0.5:
                child_strategy.append(s1)
            else:
                child_strategy.append(s2)
        return child_strategy

    def mutate(self, strategy):
        for i, _ in enumerate(strategy):
            if random.uniform(0, 1) < self.mutation_chance:
                strategy[i] = [random.uniform(-1, 1), random.uniform(-1, 1)]
        return strategy

    def select_parents(self, target):
        best_parents = sorted(self.individuals, key=lambda x: x.distance(target.x, target.y))
        return best_parents[:10]

    def create_next_generation(self, target):
        potential_parents = self.select_parents(target)
        next_generation = []

        for _ in range(self.size):
            parent_1 = random.choice(potential_parents)
            parent_2 = random.choice(potential_parents)
            child_strategy = self.crossover(parent_1, parent_2)
            child_strategy = self.mutate(child_strategy)
            next_generation.append(Individual(child_strategy))

        self.individuals = next_generation


def random_target_value():
    x = random.randint(100, WIDTH-50)
    y = random.randint(100, HEIGHT-50)
    return Unit(x, y)


class Environment:
    def __init__(self):
        self.population = Population()
        self.target = random_target_value()
        self.clock = pygame.time.Clock()

    def simulate_generation(self):
        for _ in range(self.population.number_of_steps):
            self.clock.tick()
            display.fill((0, 0, 0))
            self.target.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            for individual in self.population.individuals:
                individual.make_step()
                individual.draw()

            pygame.display.flip()

        self.population.create_next_generation(self.target)



