import pandas as pd
import mysql.connector
from mysql.connector import Error
import math

pd.options.mode.chained_assignment = None

df_user = pd.read_csv('Recom_Pre/data/users_data.csv')
df_logquiz60 = pd.read_csv('Recom_Pre/data/log_quiz60.csv')
df_logquiz61 = pd.read_csv('Recom_Pre/data/log_quiz61.csv')
df_tagChap = pd.read_csv('Recom_Pre/data/total_tagChap.csv')
df_class = pd.read_csv('Recom_Pre/data/class_totalsec.csv')
df_class_cat = pd.read_csv('Recom_Pre/data/userEclass.csv')
df_predict = pd.read_csv('Recom_Pre/data/predict.csv')
df_eclass_detail = pd.read_csv('Recom_Pre/data/e_class_detail.csv')


def findID(x):
    sid = str(x)
    if 'it' not in str(sid):
        sid = 'it' + str(sid)
    for i in df_user.username:
        check = i
        if sid == check:
            select = df_user[df_user.username == check]
            user_indexSelect = int(select.index.values)
            id_stu = select.id[user_indexSelect]
            return id_stu


def select_data(user):
    user_id = user
    for i in df_predict.user:
        check = i
        if user_id == check:
            select = df_predict[df_predict.user == check]
            index = select.index.values
            index = index.tolist()
            index = max(index)
            d1 = select.user[index]
            d2 = select.Practice_introduction[index]
            d3 = select.Practice_conceptualDesign[index]
            d4 = select.Practice_logicalDesign[index]
            d5 = select.read_introduction[index]
            d6 = select.read_er[index]
            d7 = select.read_eer[index]
            d8 = select.read_logical[index]
            return d1, d2, d3, d4, d5, d6, d7, d8


def find_eclass(x):
    select_user = x
    index = []
    # print('user', select_user)
    # print(df_class_cat.user_id.unique)
    for i in df_class_cat.user_id:
        check = i
        if select_user == check:
            select = df_class_cat[df_class_cat.user_id == check]
            index = select.index.values
            index = index.tolist()
            break
    if len(index):
        num = 0
        for ing in index:
            check2 = ing
            if check2 > num:
                num = check2
                eclass_user = select.e_class_id[num]
        return eclass_user
    else:
        num = '333'
        return num


def get_class_name(x):
    e_class_id = x
    for i in df_eclass_detail.id:
        check = i
        if e_class_id == check:
            select = df_eclass_detail.name[df_eclass_detail.id == check]
            index = int(select.index.values)
            eclass = df_eclass_detail.name[index]
            return eclass

def find_year(x):
    select_user = x
    df = df_class_cat[df_class_cat.user_id == select_user]
    index = df.index.values
    index = index.tolist()
    index = max(index)
    year = df.year[index]
    print('index', index)
    print('columns', df.columns)
    return year


def db_connect():
    conn = mysql.connector.connect(
        host='dblearning.it.kmitl.ac.th',
        database='admin_sql',
        user='data_analysis',
        password='LFJp0a44L8YQzmrK!')
    return conn


def query_toCSV_DBL(x):
    conn = db_connect()
    query = x
    result = pd.read_sql_query(query, conn)
    # db_connect().close()
    return result


def make_dataFrame_quiz():
    que_quiz = 'select DISTINCT q1.*, q2.Full_score from (SELECT admin_sql.quiz.id as \'quiz_id\', ' \
               'admin_sql.quiz.title as \'quiz_title\', admin_sql.quiz.type as \'Type\', admin_sql.quiz.pass_score, ' \
               'admin_sql.section.e_class_id FROM admin_sql.quiz join admin_sql.quiz_section on admin_sql.quiz.id = ' \
               'admin_sql.quiz_section.quiz_id join admin_sql.section on admin_sql.quiz_section.section_id = ' \
               'admin_sql.section.id where admin_sql.quiz.id in (SELECT admin_sql.quiz_section.quiz_id FROM ' \
               'admin_sql.quiz_section where admin_sql.quiz_section.section_id in (SELECT admin_sql.section.id FROM ' \
               'admin_sql.section where admin_sql.section.e_class_id in (SELECT admin_sql.e_class.id FROM ' \
               'admin_sql.e_class where admin_sql.e_class.name like \'%Database System Concepts%\' and ' \
               'admin_sql.e_class.deleted_at is null and admin_sql.e_class.year > 2559) and ' \
               'admin_sql.section.deleted_at is null) and admin_sql.quiz_section.deleted_at is null)) as q1 join (' \
               'SELECT admin_sql.quiz_question.quiz_id, sum(admin_sql.quiz_question.score) as \'Full_score\' FROM ' \
               'admin_sql.quiz_question where admin_sql.quiz_question.deleted_at is null group by quiz_id) as q2 on ' \
               'q1.quiz_id = q2.quiz_id; '
    que_tagquiz = 'SELECT admin_sql.tagged.taggable_id, admin_sql.tags.slug FROM admin_sql.tagged join admin_sql.tags ' \
                  'on admin_sql.tagged.tag_id = admin_sql.tags.id where admin_sql.tagged.taggable_type like ' \
                  '\'%Quiz%\'; '

    df_quiz = query_toCSV_DBL(que_quiz)
    df_tag_quiz = query_toCSV_DBL(que_tagquiz)

    ##clean pass score in dataframe quiz_data
    index_p = 0
    for i in df_quiz['pass_score']:
        if pd.isna(df_quiz['pass_score'][index_p]):
            df_quiz['pass_score'][index_p] = math.ceil(df_quiz['Full_score'][index_p] / 2)
        index_p += 1

    ##add tag to dataframe quiz_data
    df_quiz['tags'] = ""
    index_i = 0
    for i in df_quiz.quiz_id:
        quiz_id = i
        index_t = 0
        for t in df_tag_quiz.taggable_id:
            tagged_id = t
            if quiz_id == tagged_id:
                tag = df_tag_quiz.slug[index_t]
                if len(df_quiz.tags[index_i]) == 0:
                    df_quiz.tags[index_i] = tag
                else:
                    df_quiz.tags[index_i] = df_quiz.tags[index_i] + ", " + tag
            index_t += 1
        index_i += 1

    df_quiz.to_csv('Recom_pre/data/quiz.csv')
    return df_quiz


def percent_logQuiz(x):
    id_user = x
    df_quiz = make_dataFrame_quiz()
    class_select = find_eclass(id_user)
    # print(class_select)
    year = find_year(id_user)
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


def add_tag_logquiz(x, y):
    ##get specific tag to use
    logquiz_select = x
    logquiz_select['tags_chap_mid'] = ''
    quiz_select = y
    index_tags = quiz_select.index.values
    index_tags = index_tags.tolist()
    index_s = logquiz_select.index.values
    index_s = index_s.tolist()
    for i in index_s:
        quiz_id = logquiz_select.quiz_id[i]
        for n in index_tags:
            select_quiz = quiz_select.quiz_id[n]
            if quiz_id == select_quiz:
                tags = quiz_select.tags[n]
                list_tags = tags.split(', ')
                for tag in list_tags:
                    if 'theory' in tag:
                        logquiz_select.tags_chap_mid[i] = 'theory'
                    elif ('er-concept' in tag) or ('er-model' in tag) or ('eer-model' in tag) or ('eer-concept' in tag):
                        logquiz_select.tags_chap_mid[i] = 'conceptual'
                    elif 'mapping' in tag:
                        logquiz_select.tags_chap_mid[i] = 'mapping'
                break
    # return logquiz_select
    ## drop not use data
    for i in index_s:
        if len(logquiz_select.tags_chap_mid[i]) == 0:
            logquiz_select = logquiz_select.drop([i])
    return logquiz_select


def total_tag(x):
    ##get total class of user class
    class_select = x
    df_tag = df_tagChap[df_tagChap.e_class_id == class_select]
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


def create_data(x, y, z):
    logquiz_select = x
    df_tag = y
    select = z
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
    df = df_class_cat[df_class_cat.user_id == select]
    year = int(max(df.year))

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


def get_userInfo(user):
    user_select = str(user)
    if 'it' not in user_select:
        user_select = 'it' + str(user_select)
    df_user_select = df_user[df_user.username == user_select]
    user_indexSelect = df_user_select.index.values
    user_indexSelect = user_indexSelect.tolist()
    index = max(user_indexSelect)
    SID = str(df_user_select.username[index])
    name = str(df_user_select.firstname[index]) + " " + str(df_user_select.lastname[index])
    return SID, name

def get_read(id, year):
    if year == 2560:
        df_chapter = pd.read_csv('Recom_Pre/data/total_title60.csv')
        df_totalread = pd.read_csv('Recom_Pre/data/total_read60.csv')
    else:
        df_chapter = pd.read_csv('Recom_Pre/data/total_title61.csv')
        df_totalread = pd.read_csv('Recom_Pre/data/total_read61.csv')

    read_select = df_totalread[df_totalread.user_id == id]
    read_select['percent_read'] = 0

    index = read_select.index.values
    for i in index:
        user_read = read_select.total_read[i]
        for topic in df_chapter.chapterTitle:
            topic_check = topic
            if  read_select.title_chapter[i] == topic_check:
                percent = int((user_read/df_chapter.totalTitle[df_chapter.chapterTitle == topic_check])*100)
                read_select.percent_read[i] = percent
    print(read_select)
    return read_select

