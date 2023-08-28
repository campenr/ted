from ted import File, Buffer, FilePosition


class TestInit:
    def test_origin_init(self):
        buffer = Buffer('')
        file = File(buffer, FilePosition.origin())

        assert file.char_pos == 0
        assert file.line_pos == 0


class TestHorizontalMovement:
    def test_move_right_from_start(self):
        content = 'this is test content'
        buffer = Buffer(content)
        file = File(buffer, FilePosition.origin())

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

    def test_move_right_multi_line(self):
        content = 'this is test content\nthat takes up two lines'
        buffer = Buffer(content)
        first_line = content.splitlines()[0]
        file = File(buffer, FilePosition(x=len(first_line), y=0))

        file.move_right()

        assert file.char_pos == len(first_line)
        assert file.line_pos == 0

    def test_left_at_start_of_line(self):
        content = 'this is test content'
        buffer = Buffer(content)
        file = File(buffer, FilePosition.origin())

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
        file = File(buffer, FilePosition.origin())

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

    def test_move_down_onto_shorter_line(self):
        content = 'this is test content\nshort line'
        buffer = Buffer(content)
        first_line, second_line = content.splitlines()
        file = File(buffer, FilePosition(x=len(first_line), y=0))

        file.move_down()

        assert file.char_pos == len(second_line)
        assert file.line_pos == 1

    def test_move_up_from_the_start(self):
        content = 'this is test content\nthat takes up two lines'
        buffer = Buffer(content)
        file = File(buffer, FilePosition.origin())

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


class TestBufferIntegration:
    def test_get_char_from_buffer_single_line(self):
        content = 'this is test content'
        buffer = Buffer(content)

        file = File(buffer, FilePosition(x=3, y=0))

        assert file.get_char() == 's'

    def test_get_char_from_buffer_multi_line(self):
        content = 'this is test content\nthat takes up two lines'
        buffer = Buffer(content)

        file = File(buffer, FilePosition(x=3, y=1))

        assert file.get_char() == 't'

    def test_insert_into_buffer_no_content(self):
        buffer = Buffer('')

        file = File(buffer, FilePosition.origin())

        file.write_char('a')

        assert str(buffer) == 'a'
        assert file._position == FilePosition(x=1, y=0)

    def test_insert_into_buffer_from_file_position_single_line(self):
        content = 'this is test content'
        buffer = Buffer(content)

        file = File(buffer, FilePosition(x=3, y=0))

        file.write_char('a')

        assert str(buffer) == 'thias is test content'
        assert file._position == FilePosition(x=4, y=0)

    def test_insert_into_buffer_from_file_position_multi_line(self):
        content = 'this is test content\nthat takes up two lines'
        buffer = Buffer(content)

        file = File(buffer, FilePosition(x=3, y=1))

        file.write_char('a')

        assert str(file._buffer) == 'this is test content\nthaat takes up two lines'
        assert file._position == FilePosition(x=4, y=1)

    def test_insert_new_line_no_content(self):
        buffer = Buffer('')

        file = File(buffer, FilePosition.origin())

        file.write_char('\n')

        assert str(file._buffer) == '\n'
        assert file._position == FilePosition(x=0, y=1)

    def test_insert_new_line_single_line(self):
        buffer = Buffer('this is test content')

        file = File(buffer, FilePosition.origin())

        file.write_char('\n')

        assert str(file._buffer) == '\nthis is test content'
        assert file._position == FilePosition(x=0, y=1)
