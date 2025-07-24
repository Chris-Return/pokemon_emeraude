import random

class MoveBehavior():
    @staticmethod
    def update(deltatime, game_object_behavior):
        if(game_object_behavior.allow_movement and game_object_behavior.get_parent().get_input_active()):
            game_object_behavior.deltatime_accumulator_movement += deltatime
            if(game_object_behavior.deltatime_accumulator_movement > game_object_behavior.random_deltatime_accumulator_movement):
                direction = random.randint(0,3)
                if(game_object_behavior.get_movement_out_of_scope(direction)):
                    game_object_behavior.get_parent().move_to([direction])

                game_object_behavior.deltatime_accumulator_movement = 0
                game_object_behavior.random_deltatime_accumulator_movement = random.randint(2000, 10000)