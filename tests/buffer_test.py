import pytest

from ted import Buffer, Piece

#########
# Buffer #
#########


def test_empty_original_no_initial_piece_entry():
    buffer = Buffer()
    assert buffer._piece_table == []


def test_non_empty_original_matching_initial_piece_entry():
    content = 'this is test content\n'
    buffer = Buffer(content)
    assert buffer._piece_table == [
        Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
    ]


def test_get_correct_piece_for_index_simple_case():
    content = 'this is test content\n'
    buffer = Buffer(content)
    assert buffer._get_indexes(5) == (0, 5)


def test_get_correct_piece_for_index():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, len(content))

    assert buffer._get_indexes(len(content) + 2) == (1, 2)


def test_split_piece():
    content = 'this is test content\n'
    buffer = Buffer(content)
    split_index = 5
    pieces = buffer._split_piece(buffer._piece_table[0], split_index)
    assert pieces == [
        Piece(start=0, length=split_index, source=Buffer.ORIGINAL),
        Piece(start=split_index, length=len(content) - split_index, source=Buffer.ORIGINAL),
    ]


def test_non_empty_with_content_added_at_end():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, len(content))

    assert buffer._piece_table == [
        Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
        Piece(start=0, length=len(added_content), source=Buffer.ADD),
        Piece(start=21, length=0, source=Buffer.ORIGINAL),  # TODO: remove pieces with zero length?
    ]


def test_non_empty_with_content_added_at_start():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, 0)

    assert buffer._piece_table == [
        Piece(start=0, length=len(added_content), source=Buffer.ADD),
        Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
    ]


def test_non_empty_with_content_added_in_middle_of_original():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    insertion_pos = 8
    buffer.insert(added_content, insertion_pos)

    assert buffer._piece_table == [
        Piece(source='_original', start=0, length=insertion_pos),
        Piece(source='_add', start=0, length=len(added_content)),
        Piece(source='_original', start=insertion_pos, length=len(content) - 8),
    ]


def test_non_empty_with_content_added_in_middle_of_added():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    insertion_pos_1 = 8
    buffer.insert(added_content, insertion_pos_1)

    added_content_2 = 'more things\n'
    insertion_pos_2 = 10
    buffer.insert(added_content_2, insertion_pos_2)

    assert buffer._piece_table == [
        Piece(source='_original', start=0, length=insertion_pos_1),
        Piece(source='_add', start=0, length=insertion_pos_2 - insertion_pos_1),
        Piece(source='_add', start=len(added_content), length=len(added_content_2)),
        Piece(source='_add', start=insertion_pos_2 - insertion_pos_1, length=len(added_content) - (insertion_pos_2 - insertion_pos_1)),
        Piece(source='_original', start=insertion_pos_1, length=len(content) - insertion_pos_1),
    ]


def test_non_empty_with_content_added_at_end_of_added():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    insertion_pos_1 = 8
    buffer.insert(added_content, insertion_pos_1)

    added_content_2 = 'more things\n'
    insertion_pos_2 = insertion_pos_1 + len(added_content)
    buffer.insert(added_content_2, insertion_pos_2)

    assert buffer._piece_table == [
        Piece(source='_original', start=0, length=insertion_pos_1),
        Piece(source='_add', start=0, length=len(added_content) + len(added_content_2)),
        Piece(source='_original', start=insertion_pos_1, length=len(content) - 8),
    ]


########
# File #
########

def test_get_buffer_location_from_file_position():
    content = 'this is\nmultiline\ntest content'
    buffer = Buffer(content)
    line_pos, char_pos = 1, 2
    assert buffer.get_char_index(line_pos, char_pos) == 9


def test_get_buffer_location_from_file_position_2():
    content = 'this is\nmultiline\ntest content'
    buffer = Buffer(content)
    line_pos, char_pos = 0, 2
    assert buffer.get_char_index(line_pos, char_pos) == 2


def test_get_buffer_location_from_file_position_2():
    content = 'this is\nmultiline\ntest content'
    buffer = Buffer(content)
    line_pos, char_pos = 2, 2
    assert buffer.get_char_index(line_pos, char_pos) == 18


def test_get_buffer_location_from_file_position_2():
    content = 'this is all on one line'
    buffer = Buffer(content)
    line_pos, char_pos = 0, 2
    assert buffer.get_char_index(line_pos, char_pos) == 2


##########
# Output #
##########

def test_new_empty_buffer_equals_empty_string():
    buffer = Buffer()
    assert str(buffer) == ''


def test_new_non_empty_buffer_equals_original_content():
    content = 'this is test content\n'
    buffer = Buffer(content)
    assert str(buffer) == content


def test_buffer_with_content_added_at_the_end_outputs_expected():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, len(content))

    assert str(buffer) == 'this is test content\nadded content\n'


def test_buffer_with_content_added_at_the_start_outputs_expected():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, 0)

    assert str(buffer) == 'added content\nthis is test content\n'


def test_buffer_with_content_added_in_the_middle_of_original_outputs_expected():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, 8)

    assert str(buffer) == 'this is added content\ntest content\n'


def test_buffer_with_content_added_in_the_middle_of_added_outputs_expected():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    insertion_pos = 8
    buffer.insert(added_content, insertion_pos)

    added_content_2 = 'more things\n'
    # added_content_2 = '1'
    insertion_pos = 10
    buffer.insert(added_content_2, insertion_pos)

    assert str(buffer) == 'this is admore things\nded content\ntest content\n'


def test_buffer_with_content_added_at_end_of_added_outputs_expected():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    insertion_pos = 8
    buffer.insert(added_content, insertion_pos)

    added_content_2 = 'more things\n'
    insertion_pos_2 = insertion_pos + len(added_content)
    buffer.insert(added_content_2, insertion_pos_2)

    assert str(buffer) == 'this is added content\nmore things\ntest content\n'
