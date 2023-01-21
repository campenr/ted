from ted import Buffer


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
    for i in added_content:
        buffer.add_char(i)
    assert str(buffer) == content + added_content


def test_buffer_with_content_added_at_the_start_outputs_expected():
    content = 'this is test content\n'
    buffer = Buffer(content)
    added_content = 'added content\n'
    for i in added_content:
        buffer.add_char(i)
    assert str(buffer) == added_content + content
