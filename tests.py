import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_valid_choice():
    question = Question(title="q1")
    question.add_choice("a", is_correct=True)
    assert len(question.choices) == 1
    assert question.choices[0].text == "a"
    assert question.choices[0].is_correct

def test_add_choice_with_empty_text():
    question = Question(title="q1")
    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice("")    

def test_add_choice_with_long_text():
    question = Question(title="q1")
    long_text = "a" * 101
    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice(long_text)

def test_remove_choice_by_id():
    question = Question(title="q1")
    choice = question.add_choice("a")
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0

def test_remove_choice_with_invalid_id():
    question = Question(title="q1")
    question.add_choice("a")
    with pytest.raises(Exception, match="Invalid choice id"):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title="q1")
    question.add_choice("a")
    question.add_choice("b")
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_select_valid_choices():
    question = Question(title="q1", max_selections=2)
    choice1 = question.add_choice("a", is_correct=True)
    question.add_choice("b", is_correct=False)
    selected = question.select_choices([choice1.id])
    assert selected == [choice1.id]

def test_select_more_than_max_selections():
    question = Question(title="q1", max_selections=1)
    choice1 = question.add_choice("a", is_correct=True)
    question.add_choice("b", is_correct=False)
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        question.select_choices([choice1.id, 2])


def test_set_correct_choices():
    question = Question(title="q1")
    choice1 = question.add_choice("a")
    choice2 = question.add_choice("b")
    question.set_correct_choices([choice1.id])
    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct

def test_generate_unique_choice_ids():
    question = Question(title="q1")
    question.add_choice("a")
    question.add_choice("b")
    assert question.choices[0].id != question.choices[1].id
