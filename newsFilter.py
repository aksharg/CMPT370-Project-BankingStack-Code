from newsapi import NewsApiClient
import json
import globals
from os import path

newsapi = NewsApiClient(api_key='7cf0bdea56174d2a8523d6728d01fa38')

def displayNewsFilter(topic):
    """

    This function will grab the key words or the title of the news
    and print out a list of news titles.

    arg:
        :param topic: The key words or the title of the news user wish to
                      search

    return:
        :return: None
    """
    list = []
    if len(topic) != 0:  # check whether the data is not
        data = newsapi.get_everything(q = topic, language='en', sort_by='popularity' ,page_size=20)

        articles = data['articles']

        for x,y in enumerate(articles):
            list.append(f'{x+1} {y["title"]}')

        return list

    else:

        return -1

def addNewsFilter(topic,num):
    """

    This function will help to grab the news of whatever the user enter
    and save it as a .json file in the current directory. It will first
    print out a list of titles and then grab the index of the news
    user desire to save from the user, and save that specific news into
    .json file.

    arg:
        :param topic: the key words or the title of the news user wish to
                      search.
        :param num: the index number of the 20 news that have been shown
                    to the user.

    return:
        :return: None
    """

    new_dic = {}
    i = 1
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    if len(topic) != 0:  # check whether the data is not
        data = newsapi.get_everything(q = topic, language='en', sort_by='popularity' ,page_size=20)


        articles = data['articles']



        # num = input("\nPlease input the number of the article you which to add: ")

        for key, value in articles[int(num)-1].items():
            new_dic[key]=value

        if path.exists(user_dir+"news.json"):
            with open(user_dir+'news.json') as f:
                data = json.load(f)
                list = data['data']
                for item in list:
                    if item['news'] == new_dic:
                        return 0
                    elif item['key'] == i:
                        i += 1
        else:
            with open(user_dir+'news.json', 'w') as f:
                json.dump({'data': []}, f)

        data_dict = {'key': i, 'news': new_dic}

        with open(user_dir+'news.json') as fp:
            data = json.load(fp)
            temp = data['data']
            temp.append(data_dict)

        with open(user_dir+'news.json', 'w') as fp:
            json.dump(data, fp, indent=3)


    else:

        return -1

def editNewsFilter(news_key, topic, num):
    """

    This function will grab the special key given to the news filter,
    and then replace the specific news with the content of the newly
    found news.

    arg:
        :param news_key: a special key given by the system to let the user
                         accessing to specific news.
        :param topic: the key words or the title of the news user wish to
                      search.
        :param num: the index number of the 20 news that have been shown
                    to the user.

    return:
        :return: None
    """

    new_dic = {}
    i = 1
    counter = 0
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    if len(topic) != 0 :  # check whether the data is not
        if path.exists(user_dir+"news.json"):
            data = newsapi.get_everything(q=topic, language='en', sort_by='popularity', page_size=20)


            articles = data['articles']



            # num = input("\nPlease input the number of the article you which to change to: ")

            for key, value in articles[int(num) - 1].items():
                new_dic[key] = value

            with open(user_dir+'news.json') as f:
                data = json.load(f)
                list = data['data']
                for item in list:
                    if item['key'] == news_key:
                        item['news'] = new_dic
                        counter += 1

                if counter == 0:

                    return -1

            with open(user_dir+'news.json', 'w') as fp:
                json.dump(data, fp, indent=3)
        else:

            return -1

    else:

        return -1
