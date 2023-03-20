import pytest

from ted import Buffer, Piece

#########
# Buffer #
#########


def test_empty_original_no_initial_piece_entry():
    buffer = Buffer()
    assert buffer._pieces == []


def test_non_empty_original_matching_initial_piece_entry():
    content = 'this is test content\n'
    buffer = Buffer(content)
    assert buffer._pieces == [
        Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
    ]


def test_get_correct_piece_for_index_simple_case():
    content = 'this is test content\n'
    buffer = Buffer(content)
    assert buffer._find_piece(5) == 0


def test_get_correct_piece_for_index():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, len(content))

    index = buffer._find_piece(len(content) + 2)
    assert index == 1


def test_split_piece():
    content = 'this is test content\n'
    buffer = Buffer(content)
    pieces = buffer._split_piece(buffer._pieces[0], 5)
    assert pieces == [
        Piece(start=0, length=5, source=Buffer.ORIGINAL),
        Piece(start=5, length=len(content), source=Buffer.ORIGINAL),
    ]


def test_non_empty_with_content_added_at_end():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, len(content))

    assert buffer._pieces == [
        Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
        Piece(start=0, length=len(added_content), source=Buffer.ADD),
    ]


def test_non_empty_with_content_added_at_start():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, 0)

    assert buffer._pieces == [
        Piece(start=0, length=len(added_content), source=Buffer.ADD),
        Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
    ]


def test_non_empty_with_content_added_in_middle():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, 8)

    assert buffer._pieces == [
        Piece(source='_original', start=0, length=8),
        Piece(source='_add', start=0, length=14),
        Piece(source='_original', start=8, length=21),
    ]


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


def test_buffer_with_content_added_in_the_middle_outputs_expected():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, 8)

    assert str(buffer) == 'this is added content\ntest content\n'
