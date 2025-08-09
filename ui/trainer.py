from ai.config import Config, configs
from ai.agent import *
from ui.colors import *
import ui.console as console

POPULATION_SIZE = 10
NUM_GENERATIONS = 50
NUM_GAMES_PER_PAIR = 5
TOP_K = POPULATION_SIZE // 3
MUTATIONS_PER_ELITE = 3
ai_agent = AdaptiveBeamAgent

class Individual:
    def __init__(self, id, player, generation, score=0):
        self.id = id
        self.player = player
        self.score = score
        self.generation = generation

    def __repr__(self):
        return f"ID: {self.id} Score: {self.score} Gen: {self.generation}"

def initialize_population(n = POPULATION_SIZE):
    return [Individual(id, initialize_agent(), 0) for id in range(n)]

def initialize_agent():
    return ai_agent(DARK_PIECE, Config.random_config(), 2)

def train_config():
    population = initialize_population()
    for generation in range(NUM_GENERATIONS):
        print("GENERATION:", generation)
        population = play_tournament(population, generation)
        best_performers = get_best_performers(population, TOP_K)
        
        mutated = best_performers[TOP_K // 2:] 
        for ind in mutated:
            ind.player.config = mutate_performers(ind.player.config)

        population = best_performers + [Individual(id, initialize_agent(), generation + 1) for id in range(POPULATION_SIZE - TOP_K)]
        for idx, ind in enumerate(population): 
            ind.score = 0
            ind.id = idx

        print(population)
        for ind in population:
            print(ind.id, ind.player.config)
            
    print(population)
    for ind in population:
        print(ind.id, ind.player.config)

def play_tournament(population, generation):
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            light_player = population[i].player
            dark_player = population[j].player

            light_player.color = LIGHT_PIECE
            dark_player.color = DARK_PIECE
            players = [dark_player, light_player]
            
            print(f"LOG: Pair {population[i].id} against {population[j].id} Gen: {generation}")

            light = 0
            dark = 0
            for game in range(NUM_GAMES_PER_PAIR):
                print(f"LOG: Game {game + 1}")
                info = console.simulate_game(players)

                if info is None: continue

                print(info.winner)
                if info.winner == light_player: 
                    population[i].score += 1
                    light += 1
                else: 
                    population[j].score += 1
                    dark += 1
    
    population = sorted(population, key=lambda x: x.score, reverse=True)
    return population

def get_best_performers(population, k):
    return population[:k]

def mutate_performers(config, factor=0.1):
    def jitter(val): return val + random.uniform(-factor, factor)

    return Config(
        blocked_point_score=jitter(config.blocked_point_score),
        connected_blocks_factor=jitter(config.connected_blocks_factor),
        blots_factor=jitter(config.blots_factor),
        blots_factor_passed=jitter(config.blots_factor_passed),
        blots_threshold=max(0, config.blots_threshold + random.choice([-1, 0, 1])),
        run_or_block_factor=jitter(config.run_or_block_factor),
    )

train_config()