import pytest

from ted import Buffer

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
        Buffer.Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
    ]


def test_non_empty_with_content_added_at_end():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, len(content))

    assert buffer._pieces == [
        Buffer.Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
        Buffer.Piece(start=0, length=len(added_content), source=Buffer.ADD),
    ]


def test_non_empty_with_content_added_at_start():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, 0)

    assert buffer._pieces == [
        Buffer.Piece(start=0, length=len(added_content), source=Buffer.ADD),
        Buffer.Piece(start=0, length=len(content), source=Buffer.ORIGINAL),
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

    assert str(buffer) == f'{content}{added_content}'


def test_buffer_with_content_added_at_the_start_outputs_expected():
    content = 'this is test content\n'
    buffer = Buffer(content)

    added_content = 'added content\n'
    buffer.insert(added_content, 0)

    assert str(buffer) == f'{added_content}{content}'
