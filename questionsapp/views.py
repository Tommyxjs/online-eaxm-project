from django.http import QueryDict
from django.shortcuts import render

# Create your views here.
from django import http
from django.views import View
from fuzzywuzzy import fuzz
from django.shortcuts import render
# Create your views here.
import happybase
import json
import re


# 1 列表视图
class QuestionInfoView(View):
    def get(self, request):
        """获取所有学生信息"""
        # 1 ，查询
        connection = happybase.Connection('47.100.92.57')
        qesTable = connection.table('questionstable')

        # 2 ，转Json
        j = eval(request.GET.get('page')) - 1  # 获取当前页数，并将页数值-1
        qesList = []
        for key, value in qesTable.scan():
            qes_dict = {
                "institution": key.decode().split("$")[0],
                "questionsId": key.decode().split("$")[1],
                "category": value[b'Paper_info:Category'].decode(),
                "question": value[b'Paper_info:Question'].decode(),
                "standardanswer": value[b'Paper_info:StandardAnswer'].decode(),
                "score": value[b'Paper_info:Score'].decode(),
                "level": value[b'Paper_info:Level'].decode(),
            }
            qesList.append(qes_dict)
        keyword = request.GET.get('input')
        if keyword != '':
            temp = []
            for i in qesList:
                if fuzz.token_sort_ratio(keyword, i["score"]) == 100 or re.search(keyword, i["institution"]) != None or re.search(keyword, i["question"]) != None:
                    temp.append(i)
            total = len(temp)
            returnList = {'data': [], 'total': total}
            if j * 10 + 10 <= total:
                for i in range(j * 10, j * 10 + 10):
                    returnList['data'].append(temp[i])
            else:
                for i in range(j * 10, total):
                    returnList['data'].append(temp[i])
        else:
            total = len(qesList)
            returnList = {'data': [], 'total': total}
            if j * 10 + 10 <= total:
                for i in range(j * 10, j * 10 + 10):
                    returnList['data'].append(qesList[i])
            else:
                for i in range(j * 10, total):
                    returnList['data'].append(qesList[i])


        # 3 ，返回响应
        return http.JsonResponse(returnList, safe=False)

    def post(self, request):
        """创建学生对象"""
        # 1，获取参数
        dict_data = json.loads(request.body.decode())
        print(dict_data)
        if 'multipleSelection' in dict_data:
            new_data = dict_data['multipleSelection']
        else:
            new_data = dict_data
        print(new_data)
        for i in new_data:
            print(i)
            institution = i.get("institution")
            questionsId = i.get("questionsId")
            category = i.get("category")
            question = i.get("question")
            standardanswer = i.get("standardanswer")
            score = i.get("score")
            level = i.get("level")
            print(institution)
            # 2，校验参数(暂时省略)
            # 3，数据入库
            connection = happybase.Connection('47.100.92.57')
            qesTable = connection.table('questionstable')
            qesData = {'Paper_info:Category': category, 'Paper_info:Question': question,
                       'Paper_info:StandardAnswer': standardanswer, 'Paper_info:Score': score, 'Paper_info:Level': level}
            rowKey = institution + '$' + str(questionsId)
            qesTable.put(row=rowKey, data=qesData)
            # 4，返回响应
            info = dict(qesTable.row(rowKey))
            qes_dict = {
                "institution": rowKey.split("$")[0],
                "questionsId": rowKey.split("$")[1],
                "category": info[b'Paper_info:Category'].decode(),
                "question": info[b'Paper_info:Question'].decode(),
                "standardanswer": info[b'Paper_info:StandardAnswer'].decode(),
                "score": info[b'Paper_info:Score'].decode(),
                "level": info[b'Paper_info:Level'].decode(),
            }
        return http.JsonResponse(qes_dict, safe=False)

    def delete(self, request):
        deleteQuestionsId = request.GET.getlist("deleteQuestionsId")
        deleteInstitution = request.GET.getlist("deleteInstitution")
        #print(request)
        #print(request.body)
        #data = request.body.decode('utf-8')
        #print("data", data)

        #print(QueryDict(request.body).get("deleteQuestionsId"))
        #print(QueryDict(request.body).get("deleteInstitution"))

        #deleteQuestionsId = request.GET.get('deleteQuestionsId')
        #deleteInstitution = request.GET.get('deleteInstitution')

        print(deleteQuestionsId)
        print(deleteInstitution)
        #multipleSelection = request.GET.get('multipleSelection')


        for index in range(len(deleteQuestionsId)):
            # 1,获取数据
            # #rk = (request.GET.get('institution')) + '$' + (request.GET.get('questionsId'))
            rk = deleteInstitution[index] + '$' + deleteQuestionsId[index]
            #print(deleteInstitution[index])
            #print(index)
            #print(deleteQuestionsId[index])

            # 2 删除数据
            connection = happybase.Connection('47.100.92.57')
            stuTable = connection.table('questionstable')
            stuTable.delete(rk)
        # 3 返回响应
        return http.HttpResponse(status=204)
