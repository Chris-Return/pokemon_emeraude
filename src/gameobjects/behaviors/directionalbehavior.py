import random

class DirectionalBehavior():
    @staticmethod
    def update(deltatime, game_object_behavior):
        if(game_object_behavior.allow_directional_change and game_object_behavior.get_parent().get_input_active()):
            game_object_behavior.deltatime_accumulator_direction += deltatime
            if(game_object_behavior.deltatime_accumulator_direction > game_object_behavior.random_deltatime_accumulator_direction):
                game_object_behavior.get_parent().set_direction(random.randint(0,3))
                game_object_behavior.deltatime_accumulator_direction = 0
                game_object_behavior.random_deltatime_accumulator_direction = random.randint(500, 4000)