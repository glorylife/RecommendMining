import pandas as pd
from .perp_data import *
from .load_model import *

pd.options.mode.chained_assignment = None
df_user = pd.read_csv('Recom_Pre/data/userEclass.csv')
df_logquiz60 = pd.read_csv('Recom_Pre/data/log_quiz60.csv')
df_logquiz61 = pd.read_csv('Recom_Pre/data/log_quiz61.csv')
df_tagChap = pd.read_csv('Recom_Pre/data/total_tagChap.csv')
df_userinfo = pd.read_csv('Recom_Pre/data/users_data.csv')
df_class_detail = pd.read_csv('Recom_Pre/data/e_class_detail.csv')
df_class = pd.read_csv('Recom_Pre/data/class_totalsec.csv')

def show_class():
    class_select = list(df_class_detail.name.unique())
    # print(year)
    return class_select

def find_class_id(x):
    class_name = x
    year = max(list(df_class_detail.year.unique()))
    df_class_present = df_class_detail[df_class_detail.year == year]
    class_select = df_class_present[df_class_present.name == class_name]
    class_id = max(list(class_select.id))
    return class_id

def get_year(x):
    year = x
    if year == 2560:
        user = list(df_logquiz60.user_id.unique())
        return user
    else:
        user = list(df_logquiz61.user_id.unique())
        return user


def percent_logQuiz_user(x, y, z):
    id_user = x
    df_quiz = make_dataFrame_quiz()
    class_select = y
    # print(class_select)
    year = z
    # print(year)
    ##create log_quiz
    if year == 2560:
        # print('in year 2560')
        logquizall = df_logquiz60
    else:
        # print('in year 2561')
        logquizall = df_logquiz61

    logquizall['percent_score'] = 0

    ##Select user_logQuiz
    logquiz_select = logquizall[logquizall.user_id == id_user]

    index_s = logquiz_select.index.values

    df_quiz_select = df_quiz[df_quiz.e_class_id == class_select]

    index_quiz = df_quiz_select.index.values
    ##calulate percent of execise (user)
    for i in index_s:
        log_select = i
        for m in index_quiz:
            quiz_select = m
            if df_quiz_select.quiz_id[quiz_select] == logquiz_select.quiz_id[log_select]:
                if df_quiz_select.Full_score[quiz_select] != 0 and logquiz_select.high_score[log_select] > 0:
                    get_score = logquiz_select.high_score[log_select]
                    full_score = df_quiz_select.Full_score[quiz_select]
                    if get_score > full_score:
                        get_score = full_score
                    percent = (get_score / full_score)
                    percent = percent * 100
                    logquiz_select.percent_score[log_select] = percent
                    break

    return logquiz_select, df_quiz_select


def total_tag_user(x):
    ##get total class of user class
    class_select = x
    df_tag = df_tagChap[df_tagChap.e_class_id == class_select]
    # print(df_tag)
    df_tag['Total_tags'] = 0

    ## calculate real total tag in class and drop pervious total
    index_tag = df_tag.index.values
    index_tag = index_tag.tolist()
    for i in index_tag:
        total = df_tag.total[i]
        e_class_id_select = class_select
        index_class = 0
        for n in df_class.e_class_id:
            e_class_id_check = n
            if e_class_id_select == e_class_id_check:
                sec = df_class.total_sec[index_class]
                df_tag.Total_tags[i] = int(total / sec)
                break
            else:
                index_class += 1
    df_tag = df_tag.drop('total', axis=1)
    return df_tag


def create_data_user(x, y, z, a):
    logquiz_select = x
    df_tag = y
    select = z
    year = a
    ## create dataframe to use in predict process
    dict_select = {'user': [select], 'Practice_introduction': [0], 'Practice_conceptualDesign': [0],
                   'Practice_logicalDesign': [0]}
    df_select = pd.DataFrame(dict_select)

    # create Dataframe total execise in chapter to use in midterm
    dict_midterm = {'theory': [0], 'conceptual': [0], 'mapping': [0]}
    dict_record = {'user': [select], 's_theory': [0], 's_conceptual': [0], 's_mapping': [0]}
    df_record_f = pd.DataFrame(dict_record)
    df_tagMid_f = pd.DataFrame(dict_midterm)
    df_record = df_record_f
    df_tagMid = df_tagMid_f
    theory = 0
    conceptual = 0
    mapping = 0
    index_tag = df_tag.index.values
    index_tagA = index_tag.tolist()
    for i in index_tagA:
        if 'theory' in df_tag.tags[i]:
            theory += df_tag.Total_tags[i]
        elif ('er-concept' in df_tag.tags[i]) or ('er-model' in df_tag.tags[i]) or ('eer-model' in df_tag.tags[i]) or (
                'eer-concept' in df_tag.tags[i]):
            conceptual += df_tag.Total_tags[i]
        elif 'mapping' in df_tag.tags[i]:
            mapping += df_tag.Total_tags[i]
    df_tagMid.theory = theory
    df_tagMid.conceptual = conceptual
    df_tagMid.mapping = mapping
    theory = 0
    conceptual = 0
    mapping = 0
    list_indexSelect = logquiz_select.index.values
    list_indexSelect = list_indexSelect.tolist()
    for j in list_indexSelect:
        if 'theory' in logquiz_select.tags_chap_mid[j]:
            theory += logquiz_select.percent_score[j]
        elif 'conceptual' in logquiz_select.tags_chap_mid[j]:
            conceptual += logquiz_select.percent_score[j]
        elif 'mapping' in logquiz_select.tags_chap_mid[j]:
            mapping += logquiz_select.percent_score[j]
    df_record.s_theory[0] = int(theory / df_tagMid.theory[0])
    df_record.s_conceptual[0] = int(conceptual / df_tagMid.conceptual[0])
    df_record.s_mapping[0] = int(mapping / df_tagMid.mapping[0])
    indexs = 0

    df_select.Practice_introduction[0] = df_record.s_theory[0]
    df_select.Practice_conceptualDesign[0] = df_record.s_conceptual[0]
    df_select.Practice_logicalDesign[0] = df_record.s_mapping[0]

    ## find user's studies year and perpare read_data

    if year == 2560:
        df_chapter = pd.read_csv('Recom_Pre/data/total_title60.csv')
        df_totalread = pd.read_csv('Recom_Pre/data/total_read60.csv')
    else:
        df_chapter = pd.read_csv('Recom_Pre/data/total_title61.csv')
        df_totalread = pd.read_csv('Recom_Pre/data/total_read61.csv')

    read_select = df_totalread[df_totalread.user_id == select]

    df_select['read_introduction'] = 0
    df_select['read_er'] = 0
    df_select['read_eer'] = 0
    df_select['read_logical'] = 0

    index_read = read_select.index.values

    if year == 2560:
        for i in index_read:
            read = read_select.title_chapter[i]
            if ('Introduction to Database System' in read) or ('Database System Concepts and Architecture' in read) or (
                    'Relational Data Model' in read):
                df_select.read_introduction[0] += read_select.total_read[i]
            elif 'Database Design using ER Model' in read:
                df_select.read_er[0] += read_select.total_read[i]
            elif 'Database Design using EER Model' in read:
                df_select.read_eer[0] += read_select.total_read[i]
            elif 'Logical Design: Data Model Mapping' in read:
                df_select.read_logical[0] += read_select.total_read[i]

        max_read = 0
        max_read += int(df_chapter.totalTitle[df_chapter.chapterTitle == '1. Introduction to Database System'])
        max_read += int(
            df_chapter.totalTitle[df_chapter.chapterTitle == '2. Database System Concepts and Architecture'])
        max_read += int(df_chapter.totalTitle[df_chapter.chapterTitle == '5. Relational Data Model'])
        percent_r = int((df_select.read_introduction[0] / max_read) * 100)
        df_select.read_introduction[0] = percent_r

        max_read = df_chapter.totalTitle[df_chapter.chapterTitle == '3. Database Design using ER Model']
        percent_r = int((df_select.read_er[0] / max_read) * 100)
        df_select.read_er[0] = percent_r

        max_read = df_chapter.totalTitle[df_chapter.chapterTitle == '4. Database Design using EER Model']
        percent_r = int((df_select.read_eer[0] / max_read) * 100)
        df_select.read_eer[0] = percent_r

        max_read = df_chapter.totalTitle[df_chapter.chapterTitle == '6. Logical Design: Data Model Mapping']
        percent_r = int((df_select.read_logical[0] / max_read) * 100)
        df_select.read_logical[0] = percent_r

    else:
        for i in index_read:
            read = read_select.title_chapter[i]
            if 'Introduction to Database System' in read or 'Relational Data Model' in read:
                df_select.read_introduction[0] += read_select.total_read[i]
            elif 'Database Design using ER Model' in read:
                df_select.read_er[0] += read_select.total_read[i]
            elif 'Logical Design: Data Model Mapping' in read:
                df_select.read_logical[0] += read_select.total_read[i]
            elif 'Database Design using EER Model' in read:
                df_select.read_eer[0] += read_select.total_read[i]
        max_read = 0
        max_read += int(df_chapter.totalTitle[0])
        max_read += int(df_chapter.totalTitle[1])
        percent_r = int((df_select.read_introduction[0] / max_read) * 100)
        df_select.read_introduction[0] = percent_r

        max_read = df_chapter.totalTitle[df_chapter.chapterTitle == '3. Database Design using ER Model']
        percent_r = int((df_select.read_er[0] / max_read) * 100)
        df_select.read_er[0] = percent_r

        max_read = df_chapter.totalTitle[df_chapter.chapterTitle == '5. Database Design using EER Model']
        percent_r = int((df_select.read_eer[0] / max_read) * 100)
        df_select.read_eer[0] = percent_r

        max_read = df_chapter.totalTitle[df_chapter.chapterTitle == '4. Logical Design: Data Model Mapping']
        percent_r = int((df_select.read_logical[0] / max_read) * 100)
        df_select.read_logical[0] = percent_r

    df = df_select

    user = df.user[0]
    pra_intro = df.Practice_introduction[0]
    pra_con = df.Practice_conceptualDesign[0]
    pra_log = df.Practice_logicalDesign[0]
    read_intro = df.read_introduction[0]
    read_er = df.read_er[0]
    read_eer = df.read_eer[0]
    read_log = df.read_logical[0]

    return user, pra_intro, pra_con, pra_log, read_intro, read_er, read_eer, read_log


def predict_all(x,y):
    year = int(x)
    user = get_year(year)
    class_select = find_class_id(y)
    user_class_select = []
    df_check = df_user[df_user.year == year]
    df_check = df_check[df_check.e_class_id == class_select]
    check = list(df_check.user_id.unique())
    for i in user:
        if i in check:
            user_class_select.append(i)
    warning_user = []
    print(len(user_class_select))
    dict_select = {'user': [], 'Practice_introduction': [], 'Practice_conceptualDesign': [],
                   'Practice_logicalDesign': []}
    df_year = pd.DataFrame(dict_select)
    df_year['read_introduction'] = []
    df_year['read_er'] = []
    df_year['read_eer'] = []
    df_year['read_logical'] = []
    for i in user_class_select:
        user_id = i
        df_select = df_user[df_user.year == year]
        # print(df_select)
        user_class = df_select[df_select.user_id == user_id]
        user_class = int(user_class.e_class_id.unique())
        # print(user_class)
        df_tag = total_tag_user(user_class)
        select = percent_logQuiz_user(user_id, user_class, year)
        logquiz_select = add_tag_logquiz(select[0], select[1])
        df = create_data_user(logquiz_select, df_tag, user_id, year)
        answer = predict(df[0], df[1], df[2], df[3], df[4], df[5], df[6], df[7])
        if str(answer) == 'C':
            warning_user.append(user_id)
    print(warning_user)
    return warning_user
    # print(warning_user)


def warning_info(x):
    warning_user = x
    sid = []
    name = []
    dic_warn = []
    for i in warning_user:
        user_id = i
        df_user = df_userinfo[df_userinfo.id == user_id]
        index = df_user.index.values
        index = index.tolist()
        index = max(index)
        user_sid = str(df_userinfo.username[index])
        sid.append(user_sid)
        user_name = str(df_userinfo.firstname[index]) + " " + str(
            df_userinfo.lastname[index])
        name.append(user_name)
        dic = {'student' : user_sid,'stu_name': user_name, 'id': i }
        dic_warn.append(dic)
    print(dic_warn)
    return dic_warn
