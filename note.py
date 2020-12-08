import json
import os
import datetime
import globals

def createNote(title, note_content):
    """
    This function will create a new Note. If a new note have
    been created while note.json are already created, it will
    append the new note into the note.json instead.

    Args:
        :param title: The title of the note
        :param month: the current month
        :param date: the current date
        :param year: the current year
        :param note_content: what the user wish to write

    Return:
        :return: None
    """
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    global new_directory, new_direc, new_d
    current_time = datetime.datetime.now()

    if None not in (title, note_content):  # check whether the data is not
        i = 1

        # cwd = os.getcwd()
        # while True:
        #     if os.path.isdir(cwd + '\\programData'):
        #         new_directory = os.path.join(cwd + '\\programData')

        #         if os.path.isdir(new_directory + '\\userID'):
        #             new_direc = os.path.join(new_directory + '\\userID')

        #             if os.path.isdir(new_direc + '\\notes'):
        #                 new_d = os.path.join(new_direc + '\\notes')
        #                 break

        #             else:
        #                 new_d = os.path.join(new_direc + '\\notes')
        #                 os.mkdir(new_d)
        #                 continue
        #         else:
        #             new_direc = os.path.join(new_directory + '\\userID')
        #             os.mkdir(new_direc)
        #             continue
        #     else:
        #         new_directory = os.path.join(cwd+'\\programData')
        #         os.mkdir(new_directory)
        #         continue

        if os.path.exists(user_dir+"note.json"):
            with open(user_dir+'note.json') as f:
                data = json.load(f)

                if data != {'notes': []}:
                    list = data['notes']
                    for item in list:
                        if item['key'] == i:
                            i += 1
        else:
            with open(user_dir+'note.json', 'w') as f:
                json.dump({'notes': []}, f)

        note = {"title": title, "content": note_content,
                "month": int(current_time.month), "date": int(current_time.day),
                "year": int(current_time.year)}

        noteId = {"key": i, "note": note}

        with open(user_dir+'note.json') as fp:
            data = json.load(fp)
            temp = data["notes"]
            temp.append(noteId)
        with open(user_dir+'note.json', 'w') as fp:
            json.dump(data, fp, indent=3)

        
    else:
        
        return -1


def editNote(note_key, dict):
    """
    This function will update the exist note in note.json
    file by searching the given note_key and change the
    data inside to the newly given dictionary.

    args:
        :param note_key: the given id for the note.
        :param dict: a dictionary of the new data

    return:
        :return: None
    """
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    if None not in (note_key, dict):

        counter = 0

        current_time = datetime.datetime.now()

        dict['month'] = current_time.month
        dict['date'] = current_time.day
        dict['year'] = current_time.year


        if os.path.exists(user_dir + "note.json"):
            with open(user_dir + 'note.json') as f:
                data = json.load(f)
                list = data['notes']
                for item in list:
                    if item['key'] == note_key:
                        item['note'] = dict
                        counter += 1

                if counter == 0:
                                
                    return -1

            with open(user_dir + 'note.json', 'w') as fp:
                json.dump(data, fp, indent=3)
        else:
                        
            return -1



def deleteNote(note_key):
    """
    This function will be removing a note by searching
    the given note_key in the note.json file.

    arg:
        :param note_key: the given id for the note.

    return:
        :return: None
    """
    counter = 0
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    cwd = os.getcwd()


    if os.path.exists(user_dir + "note.json"):
        with open(user_dir + 'note.json') as f:
            data = json.load(f)
            list = data['notes']
            for item in list:
                if item['key'] == note_key:
                    data['notes'].remove(item)
                    counter += 1

            if counter == 0:
                            
                return -1

        with open(user_dir + 'note.json', 'w') as fp:
            json.dump(data, fp, indent=3)

    else:
                    
        return -1


def printNotes():
    """
    This function will only printing out the notes that saved in the .json file.

    return:
        :return: None

    """
    cwd = os.getcwd()
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]

    if os.path.exists(user_dir + "note.json"):
        with open(user_dir + 'note.json') as f:
            data = json.load(f)
            list = data['notes']
            new_dic = {}
            result = []
            for item in list:
                note = item['note']

                new_dic={'key' : item['key'], 'title' : note['title']}
                            
                result.append(new_dic)

            return result

    else:
                    
        return -1
