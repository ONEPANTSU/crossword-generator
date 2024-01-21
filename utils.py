import random

from coords import Point
from word import WordNode




def get_matrix(used_points):
    min_x, min_y = min(used_points.keys(), key=lambda p: p.x).x, min(used_points.keys(), key=lambda p: p.y).y
    max_x, max_y = max(used_points.keys(), key=lambda p: p.x).x, max(used_points.keys(), key=lambda p: p.y).y
    matrix = [
        [used_points[Point(x, y)]
         if Point(x, y) in used_points
         else " "
         for x in range(min_x, max_x + 1)
         ]
        for y in range(min_y, max_y + 1)
    ]
    return matrix


def group_words_by_length(words):
    words_by_len = {}
    for word in words:
        if len(word) not in words_by_len:
            words_by_len[len(word)] = list()
        words_by_len[len(word)].append(word)
    return words_by_len


def get_cross_char(word: WordNode) -> tuple[int, str]:
    cross_char_index = None
    while (not cross_char_index or
           cross_char_index == word.cross_char_left_index or
           cross_char_index == word.cross_char_right_index):
        cross_char_index = random.randint(0, len(word) // 2 - 1)
    return cross_char_index


def get_random_length(word_list):
    return word_list[
        random.randint(0, len(word_list) - 1)
    ]


def get_axis_word(words_dict: dict[int, list[str]]):
    odd_lengths = [key for key, val in words_dict.items() if len(val) % 2 != 0]
    if len(odd_lengths) == 0:
        axis_len = get_random_length(list(words_dict.keys()))
    else:
        axis_len = get_random_length(odd_lengths)
    if len(words_dict[axis_len]) == 1:
        axis_word = words_dict[axis_len][0]
    else:
        axis_word = words_dict[axis_len][
            random.randint(0, len(words_dict[axis_len]) - 1)
        ]
    words_dict[axis_len].remove(axis_word)
    return axis_word


def find_words(char_left, char_right, words_dict: dict[int, list[str]], direction="h"):
    for length in words_dict:
        words: list[str] = words_dict[length]
        for i in range(len(words) - 1):
            for j in range(i + 1, len(words)):
                for pos in range(0, length):
                    if direction == "h":
                        if words[i][length - pos - 1] == char_left and words[j][pos] == char_right:
                            right = words.pop(j)
                            left = words.pop(i)
                            return left, right, pos
                    else:
                        if words[i][length - pos - 1] == char_left and words[j][length - pos - 1] == char_right:
                            right = words.pop(j)
                            left = words.pop(i)
                            return left, right, pos
    return None, None, None


def create_nodes(
        left_node: WordNode,
        right_node: WordNode,
        words_by_len: dict[int, list[str]],
        used_points: dict[Point, str]
):
    cross_chars = list(range(0, len(left_node)))
    cross_chars.remove(left_node.cross_char_right_index)
    random.shuffle(cross_chars)
    for cross_char_index in cross_chars:
        left_node.cross_char_left_index = cross_char_index
        right_node.cross_char_right_index = cross_char_index \
            if right_node.direction == "v"\
            else len(right_node) - cross_char_index - 1

        left_word, right_word, cross_pos = find_words(
            left_node.left_cross_char(), right_node.right_cross_char(), words_by_len
        )
        if left_word is not None and right_word is not None:
            if left_node.direction == "h":
                lefter_start_point = Point(
                    left_node.points[cross_char_index].x,
                    left_node.points[cross_char_index].y - len(left_word) + cross_pos
                )
                righter_start_point = Point(
                    right_node.points[cross_char_index].x,
                    right_node.points[cross_char_index].y - len(right_node) + cross_pos
                )
            else:
                lefter_start_point = Point(
                    left_node.points[cross_char_index].x - len(left_word) + cross_pos,
                    left_node.points[cross_char_index].y
                )
                righter_start_point = Point(
                    right_node.points[cross_char_index].x + len(right_node) - cross_pos,
                    right_node.points[cross_char_index].y
                )
            lefter = WordNode(
                left_word,
                right=left_node,
                cross_char_right_index=cross_pos,
                start_point=Point(
                    left_node.points[cross_char_index].x,
                )
            )
            righter = WordNode(right_word, left=right_node, cross_char_left_index=cross_pos)


            left_node.cross_char_left_index = cross_char_index
            right_node.cross_char_right_index = cross_char_index
            left_node.left = lefter
            right_node.right = righter
            return lefter, righter
    return WordNode("", right=left_node), WordNode("", left=right_node)
