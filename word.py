from coords import Point


class WordNode:
    def __init__(
            self,
            word,
            right=None,
            left=None,
            cross_char_left_index=None,
            cross_char_right_index=None,
            start_point: Point = Point(0, 0),
            direction: str = "h"
    ):
        self.word = word
        self.cross_char_left_index = None if cross_char_left_index is None \
            else len(word) - cross_char_left_index - 1 \
            if direction == "h" \
            else cross_char_left_index
        self.cross_char_right_index = cross_char_right_index
        self.right: WordNode = right
        self.left: WordNode = left
        self.direction = direction
        if direction == "h":
            end_point = Point(
                start_point.x + len(word) - 1,
                start_point.y
            )
        else:
            end_point = Point(
                start_point.x,
                start_point.y + len(word) - 1
            )
        self.points: list[Point] = list(
            Point(x, y)
            for x in range(start_point.x, end_point.x + 1)
            for y in range(start_point.y, end_point.y + 1)
        )

    def __str__(self):
        return self.word

    def left_cross_char(self):
        return self.word[self.cross_char_left_index]

    def right_cross_char(self):
        return self.word[self.cross_char_right_index]

    def __len__(self):
        return len(self.word)

    def __getitem__(self, item):
        return self.word[item]

    def get_left(self):
        if self.left is None:
            return str([self.cross_char_left_index]) + self.word + str([self.cross_char_right_index])
        return (self.left.get_left() +
                " " +
                str([self.cross_char_left_index]) +
                self.word +
                str([self.cross_char_right_index]))

    def get_right(self):
        if self.right is None:
            return str([self.cross_char_left_index]) + self.word + str([self.cross_char_right_index])
        return (str([self.cross_char_left_index]) +
                self.word +
                str([self.cross_char_right_index]) +
                " " +
                self.right.get_right())
