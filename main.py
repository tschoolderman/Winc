# Do not modify these lines
__winc_id__ = '71dd124b4a6e4d268f5973db521394ee'
__human_name__ = 'strings'

# Add your code after this line
scorer_one = 'Ruud Gullit'
scorer_two = 'Marco van Basten'

goal_0 = 32
goal_1 = 54

scorers = (f'{scorer_one} {goal_0}, {scorer_two} {goal_1}')

report = (f'{scorer_one} scored in the {goal_0}nd minute\n{scorer_two} scored in the {goal_1}th minute')

player = 'Ronald Koeman'
first_name = player[:6]
last_name = player[7:]
last_name_len = len(last_name)
name_short = player[0] + '. ' + last_name

chant_0 = (first_name + '! ') * len(first_name)
chant = chant_0[:-1]
good_chant = chant != ' '