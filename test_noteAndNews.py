import json
import os
import pytest

import note
import newsFilter

cwd = os.getcwd()
note_directory = os.path.join(cwd + '\\programData\\userId\\notes')

def test_createNote():
    """
    This function is a unit test of the createNote function.
    return:
        :return: the result after running the createNote function.
    """
    title = "abc"
    note_content = "Testing"

    note.createNote(title, note_content)

    if os.path.exists(note_directory + "\\note.json"):
        result = json.load(open(note_directory + '\\note.json'))
        return result
    else:
        return -1


def test_editNote():
    """
    This function is a unit test of the editNote function.

    return:
        :return: the result after running the editNote function.
    """
    title = "changed"
    note_content = "changed"
    note_key = 1

    update_dict = {'title': title, 'content': note_content}
    note.editNote(note_key, update_dict)

    if os.path.exists(note_directory + "\\note.json"):
        result = json.load(open(note_directory + '\\note.json'))
        return result
    else:
        return -1


def test_deleteNote():
    """
    This function is a unit test of the deleteNote function.

    return:
        :return: the result after running the deleteNote function.
    """
    note_key = 2

    note.deleteNote(note_key)

    if os.path.exists(note_directory + "\\note.json"):
        result = json.load(open(note_directory + '\\note.json'))
        return result
    else:
        return -1


def test_addNewsFilter():
    """
    This function is a unit test of the addNewsFilter function.

    return:
        :return: None
    """
    topic = 'Canada Stocks Market'
    newsFilter.addNewsFilter(topic)


def test_editNewsFilter():
    """
    This function is a unit test of the editNewsFilter function.

    return:
        :return: None
    """

    news_key = 1
    topic = 'US Stocks Market'
    newsFilter.editNewsFilter(news_key, topic)


# ###################################################
# # creating a new note.
result1 = test_createNote()
assert result1 is not None

# # # To test adding the second note, please keeps the code below uncomment.
assert os.path.exists(note_directory + "\\note.json")

with open(note_directory + '\\note.json') as f:
    data1 = json.load(f)
    list1 = data1['notes']

back_up_note1_data = data1


# ###################################################
# # creating another new note.
result2 = test_createNote()
assert result2 is not None

# # # To test adding the second note, please keeps the code below uncomment.
with open(note_directory + '\\note.json') as f:
    data2 = json.load(f)
    list2 = data2['notes']

back_up_note2_data = data2

assert len(list2) == 2
assert os.path.exists(note_directory + "\\note.json")
assert back_up_note2_data != back_up_note1_data


# ###################################################
# # creating another new note.
result3 = test_createNote()
assert result3 is not None

# To test adding the second note, please keeps the code below uncomment.
with open(note_directory + '\\note.json') as f:
    data3 = json.load(f)
    list3 = data3['notes']

back_up_note3_data = data3

assert len(list3) == 3
assert os.path.exists(note_directory + "\\note.json")
assert back_up_note3_data != back_up_note2_data


###################################################
# edit an existing note.
update1 = test_editNote()
assert update1 is not None

# To test removing function, please keeps the code below uncomment.
with open(note_directory + '\\note.json') as f:
    update_data = json.load(f)
    update_list = update_data['notes']

back_up_updated_data = update_data

assert os.path.exists(note_directory + "\\note.json")
assert len(update_list) == 3
#to testh remove please comment out the line below
assert back_up_updated_data != back_up_note3_data


###################################################
# delete an existing note.
remove1 = test_deleteNote()
assert remove1 is not None

with open(note_directory + '\\note.json') as f:
    remove_data = json.load(f)
    remove_list = remove_data['notes']

back_up_remove_data = remove_data

assert os.path.exists(note_directory + "\\note.json")
assert len(remove_list) == 2
assert back_up_remove_data != back_up_updated_data


###################################################
# add a new news filter.
#
test_addNewsFilter()
with open('news.json') as f:
    data = json.load(f)
    list = data['data']
assert os.path.exists("news.json")
assert data is not None
assert len(list) != 0 and len(list) == 1
back_up_data = data
#
# ####################################################
# # # edit an already existing news filter.
#
test_editNewsFilter()
with open('news.json') as f:
    d = json.load(f)
    l = data['data']
assert os.path.exists("news.json")
assert d is not None
assert len(l) != 0 and len(l) == 1
assert back_up_data != d
