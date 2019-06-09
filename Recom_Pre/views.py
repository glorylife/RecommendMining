from django.http import HttpResponse, HttpResponseRedirect
from .Prediction.perp_data import *
from .Prediction.load_model import *
from .Prediction.recommend import *
from .Prediction.predict_all import *
from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.transform import factor_cmap


# Create your views here.


def home(request):
    return render(request, 'Recom_Pre/index.html', {})


def about(request):
    return HttpResponse('<h1>about page</h1>')


def role(request):
    return render(request, 'Recom_Pre/roleSelect.html', {})


def wrong(request):
    return render(request, 'Recom_Pre/except.html', context={})


def student(request):
    try:
        if request.method == 'POST':
            if request.POST['sid']:

                text1 = request.POST['sid']
                text = findID(text1)
                user_id = findID(text1)
                answerb = find_eclass(text)
                class_detail = get_class_name(answerb)
                year = find_year(text)
                df_tag = total_tag(answerb)
                select = percent_logQuiz(user_id)
                logquiz_select = add_tag_logquiz(select[0], select[1])
                df = create_data(logquiz_select, df_tag, user_id)
                answer = predict(df[0], df[1], df[2], df[3], df[4], df[5], df[6], df[7])
                log_read = select_logRead(year, user_id)
                read_data = select_ReadData(year)
                quiz_select = select[1]
                data_recommend = prep_recommend(quiz_select)
                log_quiz = logquiz_select
                print(log_quiz)

                # plot
                quiz = list(log_quiz.quiz_id)
                practice_id = []
                quiz_id = []
                point_quiz = []
                point_index = []
                num = 0
                for i in quiz:
                    id = i
                    for a in quiz_select.quiz_id:
                        check = a
                        if id == check:
                            select = quiz_select.quiz_title[quiz_select.quiz_id == id]
                            select_id = select.index.values
                            select = list(quiz_select.quiz_title[select_id])
                            if 'Quiz' in select[0]:
                                quiz_id.append(select[0])
                                point_index.append(num)
                                num += 1
                            elif 'Project' in select[0]:
                                point_index.append(num)
                                num += 1
                                pass
                            else:
                                practice_id.append(select[0])
                                num += 1


                point_practice_check = list(log_quiz.percent_score)
                point_practice = []
                for i in point_index:
                    quiz_point = point_practice_check[i]
                    point_quiz.append(quiz_point)

                for i in range(len(point_practice_check)):
                    check = i
                    if check not in point_index:
                        practice = point_practice_check[check]
                        point_practice.append(practice)

                read = get_read(text, year)


                chapter = list(read.title_chapter)
                percent_read = list(read.percent_read)



                source_practice = ColumnDataSource(dict(practice_id=practice_id, point_practice=point_practice))
                source_quiz = ColumnDataSource(dict(quiz_id=quiz_id, point_quiz=point_quiz))
                source_read = ColumnDataSource(dict(chapter=chapter, percent_read=percent_read))

                ## hbar-p2
                p2 = figure(plot_width=1000, plot_height=300, y_range=practice_id, x_range=(0, 100))
                p2.hbar(y='practice_id', right='point_practice', height=0.5, alpha=0.7, source=source_practice)
                hoverp2 = HoverTool(tooltips=[('percent of score', '@point_practice')])
                p2.add_tools(hoverp2)
                script, div = components(p2)

                p3 = figure(plot_width=1000, plot_height=300, y_range=quiz_id, x_range=(0, 100))
                p3.hbar(y='quiz_id', right='point_quiz', height=0.5, alpha=0.7, source=source_quiz)
                hoverp3 = HoverTool(tooltips=[('percent of score', '@point_quiz')])
                p3.add_tools(hoverp3)
                script2, div2 = components(p3)

                p4 = figure(plot_width=1000, plot_height=300, y_range=chapter, x_range=(0, 100))
                p4.hbar(y='chapter', right='percent_read', height=0.5, alpha=0.7, source=source_read)
                hoverp4 = HoverTool(tooltips=[('percent of read', '@percent_read')])
                p4.add_tools(hoverp4)
                script3, div3 = components(p4)



                if answer == 'A' or answer == 'B':
                    # print('point', df[1], df[2], df[3])
                    recommend = check_classAB([df[1], df[2], df[3]])
                    list_enhance = enhance(recommend[1], data_recommend[0], data_recommend[1], data_recommend[2],
                                           logquiz_select)
                    list_optional = optional(recommend[2], data_recommend[0], data_recommend[1], data_recommend[2],
                                             logquiz_select)
                    recom_enhance = recommend_enhance(list_enhance[0], list_enhance[1], quiz_select, read_data,
                                                      log_read)
                    recom_op = recommend_optional(list_optional[0], list_optional[1], quiz_select, read_data)
                    info = get_userInfo(text1)

                    return render(request, 'Recom_Pre/StudentPredict.html', context={'text': text,
                                                                                     'user_id': user_id,
                                                                                     'answer': answer,
                                                                                     'eclass': class_detail,
                                                                                     'year': year,
                                                                                     'sid': info[0],
                                                                                     'fullname': info[1],
                                                                                     'enhance': recommend[1],
                                                                                     'enhance_read_all': recom_enhance[
                                                                                         0],
                                                                                     'enhance_read_topic':
                                                                                         recom_enhance[1],
                                                                                     'en_forget': recom_enhance[2],
                                                                                     'en_practice': recom_enhance[3],
                                                                                     'optional': recommend[2],
                                                                                     'optional_read_all': recom_op[0],
                                                                                     'optional_do': recom_op[1],
                                                                                     'op_forget': recom_op[2],
                                                                                     'script': script,
                                                                                     'div': div,
                                                                                     'script2': script2,
                                                                                     'div2': div2,
                                                                                     'script3': script3,
                                                                                     'div3': div3,
                                                                                     })
                elif answer == 'C':
                    # print('point', df[1], df[2], df[3])
                    recommend = check_classC([df[1], df[2], df[3]])
                    list_improve = improve(recommend[0], data_recommend[0], data_recommend[1], data_recommend[2],
                                           logquiz_select)
                    list_enhance = enhance(recommend[1], data_recommend[0], data_recommend[1], data_recommend[2],
                                           logquiz_select)
                    recom_improve = recommend_improve(list_improve[0], list_improve[1], quiz_select, read_data)

                    recom_enhance = recommend_enhance(list_enhance[0], list_enhance[1], quiz_select, read_data,
                                                      log_read)

                    info = get_userInfo(text1)

                    return render(request, 'Recom_Pre/StudentPredict.html', context={'text': text,
                                                                                     'user_id': user_id,
                                                                                     'answer': answer,
                                                                                     'eclass': class_detail,
                                                                                     'year': year,
                                                                                     'sid': info[0],
                                                                                     'fullname': info[1],
                                                                                     'improve': recommend[0],
                                                                                     'improve_read_all': recom_improve[
                                                                                         0],
                                                                                     'improve_do': recom_improve[1],
                                                                                     'im_forget': recom_improve[2],
                                                                                     'enhance': recommend[1],
                                                                                     'enhance_read_all': recom_enhance[
                                                                                         0],
                                                                                     'enhance_read_topic':
                                                                                         recom_enhance[1],
                                                                                     'en_forget': recom_enhance[2],
                                                                                     'en_practice': recom_enhance[3],
                                                                                     'script': script,
                                                                                     'div': div,
                                                                                     'script2': script2,
                                                                                     'div2': div2,
                                                                                     'script3': script3,
                                                                                     'div3': div3,
                                                                                     })



            else:
                return render(request, 'Recom_Pre/StudentPredict.html', {})
        else:
            return render(request, 'Recom_Pre/StudentPredict.html', {})
    except Exception as e:
        print(e)
        return HttpResponseRedirect('ssa/', {'error': e})


def select_group(request):
    # if request.method == 'POST':
    # select = request.POST['year_select']
    # user_warning = predict_all(select)
    # info = warning_info(user_warning)
    # return render(request, 'Recom_Pre/test.html', context={'info': info})
    # else:
    class_select = show_class()
    return render(request, 'Recom_Pre/select_group.html', context={'class': class_select})


def select_IT(request):
    try:
        if request.method == 'POST':
            text1 = request.POST['user_select']
            text = findID(text1)
            user_id = findID(text1)
            answerb = find_eclass(text)
            class_detail = get_class_name(answerb)
            year = find_year(text)
            df_tag = total_tag(answerb)
            select = percent_logQuiz(user_id)
            logquiz_select = add_tag_logquiz(select[0], select[1])
            df = create_data(logquiz_select, df_tag, user_id)
            answer = predict(df[0], df[1], df[2], df[3], df[4], df[5], df[6], df[7])
            log_read = select_logRead(year, user_id)
            read_data = select_ReadData(year)
            quiz_select = select[1]
            data_recommend = prep_recommend(quiz_select)

            recommend = check_classC([df[1], df[2], df[3]])
            list_improve = improve(recommend[0], data_recommend[0], data_recommend[1], data_recommend[2],
                                   logquiz_select)
            list_enhance = enhance(recommend[1], data_recommend[0], data_recommend[1], data_recommend[2],
                                   logquiz_select)
            recom_improve = recommend_improve(list_improve[0], list_improve[1], quiz_select, read_data)

            recom_enhance = recommend_enhance(list_enhance[0], list_enhance[1], quiz_select, read_data, log_read)

            info = get_userInfo(text1)

            log_quiz = logquiz_select
            read = get_read(text, year)

            chapter = list(read.title_chapter)
            percent_read = list(read.percent_read)

            # plot
            quiz = list(log_quiz.quiz_id)
            practice_id = []
            quiz_id = []
            point_quiz = []
            point_index = []
            num = 0
            for i in quiz:
                id = i
                for a in quiz_select.quiz_id:
                    check = a
                    if id == check:
                        select = quiz_select.quiz_title[quiz_select.quiz_id == id]
                        select_id = select.index.values
                        select = list(quiz_select.quiz_title[select_id])
                        if 'Quiz' in select[0]:
                            quiz_id.append(select[0])
                            point_index.append(num)
                            num += 1
                        elif 'Project' in select[0]:
                            point_index.append(num)
                            num += 1
                            pass
                        else:
                            practice_id.append(select[0])
                            num += 1

            point_practice_check = list(log_quiz.percent_score)
            point_practice = []
            for i in point_index:
                quiz_point = point_practice_check[i]
                point_quiz.append(quiz_point)

            for i in range(len(point_practice_check)):
                check = i
                if check not in point_index:
                    practice = point_practice_check[check]
                    point_practice.append(practice)

            source_practice = ColumnDataSource(dict(practice_id=practice_id, point_practice=point_practice))
            source_quiz = ColumnDataSource(dict(quiz_id=quiz_id, point_quiz=point_quiz))
            source_read = ColumnDataSource(dict(chapter=chapter, percent_read=percent_read))

            ## hbar-p2
            p2 = figure(plot_width=1000, plot_height=300, y_range=practice_id, x_range=(0, 100))
            p2.hbar(y='practice_id', right='point_practice', height=0.5, alpha=0.7, source=source_practice)
            hoverp2 = HoverTool(tooltips=[('percent of score', '@point_practice')])
            p2.add_tools(hoverp2)
            script, div = components(p2)

            p3 = figure(plot_width=1000, plot_height=300, y_range=quiz_id, x_range=(0, 100))
            p3.hbar(y='quiz_id', right='point_quiz', height=0.5, alpha=0.7, source=source_quiz)
            hoverp3 = HoverTool(tooltips=[('percent of score', '@point_quiz')])
            p3.add_tools(hoverp3)
            script2, div2 = components(p3)

            p4 = figure(plot_width=1000, plot_height=300, y_range=chapter, x_range=(0, 100))
            p4.hbar(y='chapter', right='percent_read', height=0.5, alpha=0.7, source=source_read)
            hoverp4 = HoverTool(tooltips=[('percent of read', '@percent_read')])
            p4.add_tools(hoverp4)
            script3, div3 = components(p4)

            return render(request, 'Recom_Pre/teacher_select.html', context={'text': text,
                                                                             'user_id': user_id,
                                                                             'answer': answer,
                                                                             'eclass': class_detail,
                                                                             'year': year,
                                                                             'sid': info[0],
                                                                             'fullname': info[1],
                                                                             'improve': recommend[0],
                                                                             'improve_read_all': recom_improve[0],
                                                                             'improve_do': recom_improve[1],
                                                                             'im_forget': recom_improve[2],
                                                                             'enhance': recommend[1],
                                                                             'enhance_read_all': recom_enhance[0],
                                                                             'enhance_read_topic': recom_enhance[1],
                                                                             'en_forget': recom_enhance[2],
                                                                             'en_practice': recom_enhance[3],
                                                                             'script': script,
                                                                             'div': div,
                                                                             'script2': script2,
                                                                             'div2': div2,
                                                                             'script3': script3,
                                                                             'div3': div3

                                                                             })
        else:
            user_warning = predict_all(2561, 'Database System Concepts')
            class_name = 'เทคโนโลยีสารสนเทศ'
            info = warning_info(user_warning)
            return render(request, 'Recom_Pre/test.html', context={'info': info, 'class_name': class_name})

    except Exception as e:
        return HttpResponseRedirect('ssa/', {'error': e})


def select_DSBA(request):
    try:
        if request.method == 'POST':
            text1 = request.POST['user_select']
            text = findID(text1)
            user_id = findID(text1)
            answerb = find_eclass(text)
            class_detail = get_class_name(answerb)
            year = find_year(text)
            df_tag = total_tag(answerb)
            select = percent_logQuiz(user_id)
            logquiz_select = add_tag_logquiz(select[0], select[1])
            df = create_data(logquiz_select, df_tag, user_id)
            answer = predict(df[0], df[1], df[2], df[3], df[4], df[5], df[6], df[7])
            log_read = select_logRead(year, user_id)
            read_data = select_ReadData(year)
            quiz_select = select[1]
            data_recommend = prep_recommend(quiz_select)
            recommend = check_classC([df[1], df[2], df[3]])
            list_improve = improve(recommend[0], data_recommend[0], data_recommend[1], data_recommend[2],
                                   logquiz_select)
            list_enhance = enhance(recommend[1], data_recommend[0], data_recommend[1], data_recommend[2],
                                   logquiz_select)
            recom_improve = recommend_improve(list_improve[0], list_improve[1], quiz_select, read_data)

            recom_enhance = recommend_enhance(list_enhance[0], list_enhance[1], quiz_select, read_data, log_read)

            info = get_userInfo(text1)

            log_quiz = logquiz_select

            read = get_read(text, year)

            chapter = list(read.title_chapter)
            percent_read = list(read.percent_read)

            # plot
            quiz = list(log_quiz.quiz_id)
            practice_id = []
            quiz_id = []
            point_quiz = []
            point_index = []
            num = 0
            for i in quiz:
                id = i
                for a in quiz_select.quiz_id:
                    check = a
                    if id == check:
                        select = quiz_select.quiz_title[quiz_select.quiz_id == id]
                        select_id = select.index.values
                        select = list(quiz_select.quiz_title[select_id])
                        if 'Quiz' in select[0]:
                            quiz_id.append(select[0])
                            point_index.append(num)
                            num += 1
                        elif 'Project' in select[0]:
                            point_index.append(num)
                            num += 1
                            pass
                        else:
                            practice_id.append(select[0])
                            num += 1

            point_practice_check = list(log_quiz.percent_score)
            point_practice = []
            for i in point_index:
                quiz_point = point_practice_check[i]
                point_quiz.append(quiz_point)

            for i in range(len(point_practice_check)):
                check = i
                if check not in point_index:
                    practice = point_practice_check[check]
                    point_practice.append(practice)

            source_practice = ColumnDataSource(dict(practice_id=practice_id, point_practice=point_practice))
            source_quiz = ColumnDataSource(dict(quiz_id=quiz_id, point_quiz=point_quiz))
            source_read = ColumnDataSource(dict(chapter=chapter, percent_read=percent_read))

            ## hbar-p2
            p2 = figure(plot_width=1000, plot_height=300, y_range=practice_id, x_range=(0, 100))
            p2.hbar(y='practice_id', right='point_practice', height=0.5, alpha=0.7, source=source_practice)
            hoverp2 = HoverTool(tooltips=[('percent of score', '@point_practice')])
            p2.add_tools(hoverp2)
            script, div = components(p2)

            p3 = figure(plot_width=1000, plot_height=300, y_range=quiz_id, x_range=(0, 100))
            p3.hbar(y='quiz_id', right='point_quiz', height=0.5, alpha=0.7, source=source_quiz)
            hoverp3 = HoverTool(tooltips=[('percent of score', '@point_quiz')])
            p3.add_tools(hoverp3)
            script2, div2 = components(p3)

            p4 = figure(plot_width=1000, plot_height=300, y_range=chapter, x_range=(0, 100))
            p4.hbar(y='chapter', right='percent_read', height=0.5, alpha=0.7, source=source_read)
            hoverp4 = HoverTool(tooltips=[('percent of read', '@percent_read')])
            p4.add_tools(hoverp4)
            script3, div3 = components(p4)

            return render(request, 'Recom_Pre/teacher_select.html', context={'text': text,
                                                                             'user_id': user_id,
                                                                             'answer': answer,
                                                                             'eclass': class_detail,
                                                                             'year': year,
                                                                             'sid': info[0],
                                                                             'fullname': info[1],
                                                                             'improve': recommend[0],
                                                                             'improve_read_all': recom_improve[0],
                                                                             'improve_do': recom_improve[1],
                                                                             'im_forget': recom_improve[2],
                                                                             'enhance': recommend[1],
                                                                             'enhance_read_all': recom_enhance[0],
                                                                             'enhance_read_topic': recom_enhance[1],
                                                                             'en_forget': recom_enhance[2],
                                                                             'en_practice': recom_enhance[3],
                                                                             'script': script,
                                                                             'div': div,
                                                                             'script2': script2,
                                                                             'div2': div2,
                                                                             'script3': script3,
                                                                             'div3': div3
                                                                             })
        else:
            user_warning = predict_all(2561, 'Database System Concepts (DSBA)')
            class_name = 'วิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ'
            info = warning_info(user_warning)
            return render(request, 'Recom_Pre/test.html', context={'info': info,
                                                                   'class_name': class_name})
    except Exception as e:
        return HttpResponseRedirect('ssa/', {'error': e})


def select_warn(request):
    try:
        if request.method == 'POST':
            text1 = request.POST['user_select']
            text = findID(text1)
            user_id = findID(text1)
            answerb = find_eclass(text)
            class_detail = get_class_name(answerb)
            year = find_year(text)
            df_tag = total_tag(answerb)
            select = percent_logQuiz(user_id)
            logquiz_select = add_tag_logquiz(select[0], select[1])
            df = create_data(logquiz_select, df_tag, user_id)
            answer = predict(df[0], df[1], df[2], df[3], df[4], df[5], df[6], df[7])
            log_read = select_logRead(year, user_id)
            read_data = select_ReadData(year)
            quiz_select = select[1]
            data_recommend = prep_recommend(quiz_select)

            recommend = check_classC([df[1], df[2], df[3]])
            list_improve = improve(recommend[0], data_recommend[0], data_recommend[1], data_recommend[2],
                                   logquiz_select)
            list_enhance = enhance(recommend[1], data_recommend[0], data_recommend[1], data_recommend[2],
                                   logquiz_select)
            recom_improve = recommend_improve(list_improve[0], list_improve[1], quiz_select, read_data)

            recom_enhance = recommend_enhance(list_enhance[0], list_enhance[1], quiz_select, read_data, log_read)

            info = get_userInfo(text1)
            return render(request, 'Recom_Pre/StudentPredict.html', context={'text': text,
                                                                             'user_id': user_id,
                                                                             'answer': answer,
                                                                             'eclass': class_detail,
                                                                             'year': year,
                                                                             'sid': info[0],
                                                                             'fullname': info[1],
                                                                             'improve': recommend[0],
                                                                             'improve_read_all': recom_improve[0],
                                                                             'improve_do': recom_improve[1],
                                                                             'im_forget': recom_improve[2],
                                                                             'enhance': recommend[1],
                                                                             'enhance_read_all': recom_enhance[0],
                                                                             'enhance_read_topic': recom_enhance[1],
                                                                             'en_forget': recom_enhance[2],
                                                                             'en_practice': recom_enhance[3],
                                                                             })
    except Exception as e:
        return HttpResponseRedirect('ssa/', {'error': e})
