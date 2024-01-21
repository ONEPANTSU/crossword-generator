from copy import copy
from utils import *
from word import WordNode

words = (
    "геология, почва, рельеф, порода, грабен, фации, осадконакопление, залежь, трещиноватость, слой, ресурсы, "
    "геофизика, месторождения, стратиграфия, плита, разлом, разрез, сейсмогенез, очаг, бурение, скважины, нефть, "
    "добыча, муфт, труба, проектирование, пористость, поляризация, нефтеотдача, нефтебаза, исследования, запасы, "
    "газификация, газопереработка, геотектоника, геодинамика, щит, газ, недра, прочность, жесткость, привод, "
    "компрессор, газопровод, геомеханика, трещины, разломы, давление, напряжение, геоэкология, ископаемые, узлы, "
    "сырье, архей, импакты, протерозой, сейсмичность, геотермия, нефтепереработка, обводненность, вязкость, "
    "флюид, грунт, водоснабжение"
)
# words = (
#     "altitude, horizon, sample, subsoil, direction, uplift, reset, canyon, flexura, wing, elevator, shafts, "
#     "cementing, expander, cover, chisel, slaughter, rotator, shank, bream, transportation, tracking, recycling, "
#     "watering, zoning, profile, trap, cluster, debit , pump, diameter, valve, rod, depth, bunkering, gushing, "
#     "debitmeter, ventilation, tank, ashcontent, upstream, esters, filtrate, blowout, slaughter, gutter, "
#     "ignition, catalyst, volcanoes, fuel, formation, anthropogenesis, torch, winch, gauge, viscoelastic, "
#     "diffusion, ditch, valve, core, solution, trunk, hygrometer"
# )
if words is None:
    words = input()
words = words.split(", ")

words_by_len = group_words_by_length(words)
# for k, v in words_by_len.items():
#     print(k, v)


words_count = 0
iteration = 0

best_matrix = dict()
best_score = 0

while words_count < 50 and iteration < 10:
    words_count = 0
    words_by_len = group_words_by_length(words)
    iteration += 1
    print(iteration)
    used_points = dict()
    matrix = []
    axis = WordNode(get_axis_word(words_by_len))
    used_points.update({
        point: axis.word[i]
        for i, point in enumerate(axis.points)
    })

    axis_iter = 0
    while (axis.left is None or axis.right is None) and axis_iter < 2:
        axis_iter += 1
        cross_char_index = get_cross_char(axis)
        axis.cross_char_left_index = cross_char_index
        axis.cross_char_right_index = len(axis.word) - cross_char_index - 1

        left_word, right_word, cross_pos = find_words(
            axis.left_cross_char(), axis.right_cross_char(), words_by_len, "v"
        )
        if left_word is not None and right_word is not None:
            left = WordNode(
                left_word,
                right=axis,
                cross_char_right_index=cross_pos,
                start_point=Point(
                    axis.points[cross_char_index].x,
                    axis.points[cross_char_index].y - len(left_word) + 1 + cross_pos
                ),
                direction="v"
            )
            right = WordNode(
                right_word,
                left=axis,
                cross_char_left_index=cross_pos,
                start_point=Point(
                    axis.points[len(axis) - cross_char_index - 1].x,
                    axis.points[len(axis) - cross_char_index - 1].y - len(right_word) + 1 + cross_pos
                ),
                direction="v"
            )
            used_points.update({
                point: left.word[i]
                for i, point in enumerate(left.points)
            })
            used_points.update({
                point: right.word[i]
                for i, point in enumerate(right.points)
            })
            axis.left = left
            axis.right = right
            words_count += 2
    if axis.left is None or axis.right is None:
        continue
    for _ in range(30):
        cross_chars = list(range(0, len(left.word)))
        cross_chars.remove(left.cross_char_right_index)
        random.shuffle(cross_chars)
        for cross_char_index in cross_chars:
            left.cross_char_left_index = cross_char_index
            right.cross_char_right_index = cross_char_index \
                if right.direction == "v" \
                else len(right.word) - cross_char_index - 1
            direction = "h" if left.direction == "v" else "v"
            left_word, right_word, cross_pos = find_words(
                left.left_cross_char(), right.right_cross_char(), words_by_len, direction
            )
            if left_word is not None and right_word is not None:
                if left.direction == "h":
                    lefter = WordNode(
                        left_word,
                        right=left,
                        cross_char_right_index=cross_pos,
                        start_point=Point(
                            left.points[left.cross_char_left_index].x,
                            left.points[left.cross_char_left_index].y - len(left_word) + 1 + cross_pos
                        ),
                        direction="v"
                    )
                    righter = WordNode(
                        right_word,
                        left=axis,
                        cross_char_left_index=cross_pos,
                        start_point=Point(
                            right.points[right.cross_char_right_index].x,
                            right.points[right.cross_char_right_index].y - len(right_word) + 1 + cross_pos
                        ),
                        direction="v"
                    )
                else:
                    lefter = WordNode(
                        left_word,
                        right=left,
                        cross_char_right_index=cross_pos,
                        start_point=Point(
                            left.points[left.cross_char_left_index].x - len(left_word) + 1 + cross_pos,
                            left.points[left.cross_char_left_index].y
                        ),
                        direction="h"
                    )
                    righter = WordNode(
                        right_word,
                        left=axis,
                        cross_char_left_index=cross_pos,
                        start_point=Point(
                            right.points[right.cross_char_right_index].x - cross_pos,
                            right.points[right.cross_char_right_index].y
                        ),
                        direction="h"
                    )

                left_points = lefter.points[:]
                left_points.remove(left.points[left.cross_char_left_index])
                for point in left_points:
                    if point in used_points:
                        continue
                right_points = righter.points[:]
                right_points.remove(right.points[right.cross_char_right_index])
                if (any([right_points[i] in used_points
                         for i in range(len(right_points))])
                        or any([right_points[i] in left_points
                                for i in range(len(right_points))])):
                    continue
                del left_points
                del right_points

                used_points.update({
                    point: lefter.word[i]
                    for i, point in enumerate(lefter.points)
                })
                used_points.update({
                    point: righter.word[i]
                    for i, point in enumerate(righter.points)
                })
                left.left = lefter
                right.right = righter
                words_count += 2
                left = lefter
                right = righter
                break

    if best_score < words_count:
        best_score = words_count
        best_matrix = copy(used_points)

    print(best_score)
    matrix = get_matrix(best_matrix)
    for row in matrix:
        print("".join(row))
