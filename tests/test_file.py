from ted import File, Buffer, FilePosition


class TestHorizontalMovement:
    def test_move_right_from_start(self):
        content = 'this is test content'
        buffer = Buffer(content)
        file = File(buffer, FilePosition(x=0, y=0))

        file.move_right()

        assert file.char_pos == 1
        assert file.line_pos == 0

    def test_move_right_from_end(self):
        content = 'this is test content'
        buffer = Buffer(content)
        file = File(buffer, FilePosition(x=len(content), y=0))

        file.move_right()

        assert file.char_pos == len(content)
        assert file.line_pos == 0

    def test_left_at_start_of_line(self):
        content = 'this is test content'
        buffer = Buffer(content)
        file = File(buffer, FilePosition(x=0, y=0))

        file.move_left()

        assert file.char_pos == 0
        assert file.line_pos == 0

    def test_left_at_end_of_line(self):
        content = 'this is test content'
        buffer = Buffer(content)
        file = File(buffer, FilePosition(x=len(content), y=0))

        file.move_left()

        assert file.char_pos == len(content) - 1
        assert file.line_pos == 0


class TestVerticalMovement:
    def test_move_down_from_the_start(self):
        content = 'this is test content\nthat takes up two lines'
        buffer = Buffer(content)
        file = File(buffer, FilePosition(x=0, y=0))

        file.move_down()

        assert file.char_pos == 0
        assert file.line_pos == 1

    def test_move_down_from_the_end(self):
        content = 'this is test content\nthat takes up two lines'
        buffer = Buffer(content)
        file = File(buffer, FilePosition(x=0, y=1))

        file.move_down()

        assert file.char_pos == 0
        assert file.line_pos == 1

    def test_move_up_from_the_start(self):
        content = 'this is test content\nthat takes up two lines'
        buffer = Buffer(content)
        file = File(buffer, FilePosition(x=0, y=0))

        file.move_up()

        assert file.char_pos == 0
        assert file.line_pos == 0

    def test_move_up_from_the_end(self):
        content = 'this is test content\nthat takes up two lines'
        buffer = Buffer(content)
        file = File(buffer, FilePosition(x=0, y=1))

        file.move_up()

        assert file.char_pos == 0
        assert file.line_pos == 0
