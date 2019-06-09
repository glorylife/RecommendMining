import pandas as pd

df_userEclass = pd.read_csv('Recom_Pre/data/userEclass.csv')
df_logquiz60 = pd.read_csv('Recom_Pre/data/log_quiz60_use.csv')
df_logquiz61 = pd.read_csv('Recom_Pre/data/log_quiz61_use.csv')
df_logread60 = pd.read_csv('Recom_Pre/data/log_read60.csv')
df_logread61 = pd.read_csv('Recom_Pre/data/log_read61.csv')
df_quiz = pd.read_csv('Recom_Pre/data/quiz.csv')
df_read60 = pd.read_csv('Recom_Pre/data/topic_chapter60.csv')
df_read61 = pd.read_csv('Recom_Pre/data/topic_chapter61.csv')


def check_classC(x_test):
    list_data = x_test
    # print(list_data)
    parameter = ['Introduction', 'ConceptualDesign', 'LogicalDesign']
    enhance = []
    improve = []
    optional = []
    index = 0
    for i in list_data:
        if i >= 50 and i < 80:
            enhance.append(parameter[index])
        elif i < 50:
            improve.append(parameter[index])
        index += 1
    return improve, enhance, optional


def check_classAB(X_test):
    list_data = X_test
    # print(list_data)
    parameter = ['Introduction', 'ConceptualDesign', 'LogicalDesign']
    enhance = []
    improve = []
    optional = []
    index = 0
    for i in list_data:
        if i >= 50 and i < 80:
            # print('Enhance Knowledge about', parameter[index], 'catagory')
            enhance.append(parameter[index])
            # print('enhance:', parameter[index])
        elif i >= 80:
            # print('Optional Enhance Knowledge about', parameter[index], 'catagory')
            optional.append(parameter[index])
            # print('optional:', parameter[index])
        else:
            enhance.append(parameter[index])
        index += 1
    return improve, enhance, optional


def select_logRead(year, user):
    if year == 2560:
        df_logread = df_logread60[df_logread60.user_id == user]
    elif year == 2561:
        df_logread = df_logread61[df_logread61.user_id == user]
    return df_logread


def select_ReadData(x):
    if x == 2560:
        df_read = df_read60
    elif x == 2561:
        df_read = df_read61
    return df_read


def prep_recommend(x):
    df_quiz_class_select = x
    indexSelect = df_quiz_class_select.index.values
    introduction = []
    conceptual = []
    logical = []
    for i in indexSelect:
        if pd.isna(df_quiz_class_select.tags[i]):
            df_quiz_class_select = df_quiz_class_select.drop([i])
        elif df_quiz_class_select.Type[i] == 'quiz':
            df_quiz_class_select = df_quiz_class_select.drop([i])
        elif 'project' in df_quiz_class_select.tags[i]:
            df_quiz_class_select = df_quiz_class_select.drop([i])
        else:
            list_tag = df_quiz_class_select.tags[i].split(', ')
            drop = 1
            if 'theory' in list_tag:
                drop = 0
                introduction.append(df_quiz_class_select.quiz_id[i])
            if 'er-concept' in list_tag or 'er-model' in list_tag or 'eer-concept' in list_tag or 'eer-model' in list_tag:
                drop = 0
                conceptual.append(df_quiz_class_select.quiz_id[i])
            if 'mapping' in list_tag:
                drop = 0
                logical.append(df_quiz_class_select.quiz_id[i])
            if drop == 1:
                df_quiz_class_select = df_quiz_class_select.drop([i])
    return introduction, conceptual, logical


def improve(x, y, z, a, b):
    list_improve = x
    introduction = y
    conceptual = z
    logical = a
    log_quiz = b
    quiz_do = list(log_quiz.quiz_id)
    improve_read = []
    improve_do = []
    if 'Introduction' in list_improve:
        for i in introduction:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score < 50:
                    improve_read.append(check_practice)
            else:
                improve_do.append(check_practice)
    if 'ConceptualDesign' in list_improve:
        for i in conceptual:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score < 50:
                    improve_read.append(check_practice)
            else:
                improve_do.append(check_practice)
    if 'LogicalDesign' in list_improve:
        for i in logical:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score < 50:
                    improve_read.append(check_practice)
            else:
                improve_do.append(check_practice)
    return improve_read, improve_do


def enhance(x, y, z, a, b):
    list_enhance = x
    introduction = y
    conceptual = z
    logical = a
    log_quiz = b
    quiz_do = list(log_quiz.quiz_id)
    enhance_read = []
    enhance_do = []
    if 'Introduction' in list_enhance:
        for i in introduction:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score > 50 and p_score <= 80:
                    enhance_read.append(check_practice)
            else:
                enhance_do.append(check_practice)
    if 'ConceptualDesign' in list_enhance:
        for i in conceptual:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score > 50 and p_score <= 80:
                    enhance_read.append(check_practice)
            else:
                enhance_do.append(check_practice)
    if 'LogicalDesign' in list_enhance:
        for i in logical:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score > 50 and p_score <= 80:
                    enhance_read.append(check_practice)
            else:
                enhance_do.append(check_practice)
    return enhance_read, enhance_do


def optional(x, y, z, a, b):
    list_optional = x
    introduction = y
    conceptual = z
    logical = a
    log_quiz = b
    quiz_do = list(log_quiz.quiz_id)
    optional_read = []
    optional_do = []
    if 'Introduction' in list_optional:
        for i in introduction:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score <= 80:
                    optional_read.append(check_practice)
            else:
                optional_do.append(check_practice)
    if 'ConceptualDesign' in list_optional:
        for i in conceptual:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score <= 80:
                    optional_read.append(check_practice)
            else:
                optional_do.append(check_practice)
    if 'LogicalDesign' in list_optional:
        for i in logical:
            check_practice = i
            if check_practice in quiz_do:
                p_score = int(log_quiz.percent_score[log_quiz.quiz_id == check_practice])
                if p_score <= 80:
                    optional_read.append(check_practice)
            else:
                optional_do.append(check_practice)
    return optional_read, optional_do


def insert_chapter(df_quiz):
    df_quiz_class_select = df_quiz
    df_quiz_class_select['Chapter'] = ''
    indexSelect = df_quiz_class_select.index.values
    for i in indexSelect:
        test = df_quiz_class_select.tags[i]
        list_test = test.split(', ')
        for tag in list_test:
            if tag == 'chapter1' or tag == 'chapter-1':
                df_quiz_class_select.Chapter[i] = 1
            elif tag == 'chapter2' or tag == 'chapter-2':
                df_quiz_class_select.Chapter[i] = 2
            elif tag == 'chapter3' or tag == 'chapter-3':
                df_quiz_class_select.Chapter[i] = 3
            elif tag == 'chapter4' or tag == 'chapter-4':
                df_quiz_class_select.Chapter[i] = 4
            elif tag == 'chapter5' or tag == 'chapter-5':
                df_quiz_class_select.Chapter[i] = 5
            elif tag == 'chapter6' or tag == 'chapter-6':
                df_quiz_class_select.Chapter[i] = 6
    return df_quiz_class_select


def recommend_improve(read, do, df_quiz, read_data):
    recom_read = read
    recom_do = do
    improve_read_all = []
    improve_do = []
    don_forget = []
    df_quiz_class_select = insert_chapter(df_quiz)
    Chapter = list(read_data.chapterTitle.unique())
    for i in recom_read:
        df = df_quiz_class_select[df_quiz_class_select.quiz_id == i]
        indexSelect = int(df.index.values)
        chap = str(df.Chapter[indexSelect])
        chapter_read = ''
        for c in Chapter:
            Chapter_check = c
            if chap in Chapter_check:
                chapter_read = Chapter_check
                break
        quiz = df_quiz_class_select[df_quiz_class_select.quiz_id == i]
        quiz_indexSelect = int(quiz.index.values)
        quiz_selectchap = str(quiz.quiz_title[quiz_indexSelect])
        if quiz_selectchap not in improve_do:
            improve_do.append(quiz_selectchap)
        if chapter_read not in improve_read_all:
            improve_read_all.append(chapter_read)
        # print(' -'*50)
    for i in recom_do:
        quiz = df_quiz_class_select[df_quiz_class_select.quiz_id == i]
        quiz_indexSelect = int(quiz.index.values)
        quiz_selectchap = str(quiz.quiz_title[quiz_indexSelect])
        if quiz_selectchap not in don_forget:
            don_forget.append(quiz_selectchap)
    return improve_read_all, improve_do, don_forget


def recommend_enhance(read, do, df_quiz, read_data, log_read):
    recom_read = read
    recom_do = do
    enhance_read_all = []
    enhance_read_topic = []
    don_forget = []
    practice = []
    df_quiz_class_select = insert_chapter(df_quiz)
    Chapter = list(read_data.chapterTitle.unique())
    for i in recom_read:
        df = df_quiz_class_select[df_quiz_class_select.quiz_id == i]
        indexSelect = int(df.index.values)
        chap = str(df.Chapter[indexSelect])
        for c in Chapter:
            Chapter_check = c
            if chap in Chapter_check:
                chapter_read = Chapter_check
                log_read_select = list(log_read.title_topic[log_read.title_chapter == chapter_read])
                read_data_select = list(read_data.topicTitle[read_data.chapterTitle == chapter_read])
                unread = []
                for un in read_data_select:
                    if un not in log_read_select:
                        unread.append(un)
                quiz = df_quiz_class_select[df_quiz_class_select.quiz_id == i]
                quiz_indexSelect = int(quiz.index.values)
                quiz_selectchap = str(quiz.quiz_title[quiz_indexSelect])
                # print('For Enhance Practice:', quiz_selectchap, 'score.')
                if quiz_selectchap not in practice:
                    practice.append(quiz_selectchap)

                if len(unread) > 0:
                    # print('You can enhance knowledge by read or see video in', chapter_read, 'topic:')
                    for topic in unread:
                        # print('-', topic)
                        if chapter_read + ' | ' + topic not in enhance_read_topic:
                            enhance_read_topic.append(chapter_read + ' | ' + topic)
                elif len(unread) == 0 and chapter_read not in enhance_read_all:
                    # print('You can enhance knowledge by read all topic in chapter', chapter_read, 'again.')
                    enhance_read_all.append(chapter_read)

    for i in recom_do:
        quiz = df_quiz[df_quiz.quiz_id == i]
        quiz_indexSelect = int(quiz.index.values)
        quiz_selectchap = str(quiz.quiz_title[quiz_indexSelect])
        # print('You have not done Practice:', quiz_selectchap)
        if quiz_selectchap not in practice and quiz_selectchap not in don_forget:
            don_forget.append(quiz_selectchap)
        # print('Do not forget to do it for enhance your knowledge.')
        # print(' -' * 50)
    return enhance_read_all, enhance_read_topic, don_forget, practice


def recommend_optional(read, do, df_quiz, read_data):
    recom_read = read
    recom_do = do
    optional_read_all = []
    optional_do = []
    don_forget = []
    df_quiz_class_select = insert_chapter(df_quiz)
    Chapter = list(read_data.chapterTitle.unique())
    for i in recom_read:
        df = df_quiz_class_select[df_quiz_class_select.quiz_id == i]
        indexSelect = int(df.index.values)
        chap = str(df.Chapter[indexSelect])
        chapter_read = ''
        for c in Chapter:
            Chapter_check = c
            if chap in Chapter_check:
                chapter_read = Chapter_check
                break
        quiz = df_quiz_class_select[df_quiz_class_select.quiz_id == i]
        quiz_indexSelect = int(quiz.index.values)
        quiz_selectchap = str(quiz.quiz_title[quiz_indexSelect])
        if quiz_selectchap not in optional_do:
            optional_do.append(quiz_selectchap)
        # print('Optional for Enhance Practice:', quiz_selectchap, 'score.')
        # print('You can read all topic in', chapter_read, 'and do this practice again.')
        if chapter_read not in optional_read_all:
            optional_read_all.append(chapter_read)
        # print('This is optional recommend for you')
        # print(' -' * 50)
    for i in recom_do:
        quiz = df_quiz_class_select[df_quiz_class_select.quiz_id == i]
        quiz_indexSelect = int(quiz.index.values)
        quiz_selectchap = str(quiz.quiz_title[quiz_indexSelect])
        if quiz_selectchap not in don_forget:
            don_forget.append(quiz_selectchap)
        # print('You have not done Practice:', quiz_selectchap)
        # print('Do not forget to do it for enhance your knowledge.')
        # print(' -' * 50)
    return optional_read_all, optional_do, don_forget
