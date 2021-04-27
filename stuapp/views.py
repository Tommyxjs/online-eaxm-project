from django import http
from django.views import View
from django.shortcuts import render
from fuzzywuzzy import fuzz
# Create your views here.
import happybase
import json
import re



# 1 列表视图
class StuInfoView(View):
    def get(self, request):
        """获取所有学生信息"""
        # 1 ，查询
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        # 2 ，转Json
        j = eval(request.GET.get('page')) - 1 #获取当前页数，并将页数值-1
        stuList = []
        for key, value in stuTable.scan():
            stu_dict = {
                "institution": key.decode().split("$")[0],
                "stuId": key.decode().split("$")[1],
                "cidNum": value[b'CID:cidNumber'].decode(),
                "stuName": value[b'Student_info:StuName'].decode(),
                "phone": value[b'Student_info:Phone'].decode()
            }
            stuList.append(stu_dict)
        keyword = request.GET.get('input')
        if keyword != '':
            temp = []
            for i in stuList:
                if fuzz.token_sort_ratio(keyword, i["stuName"]) == 100 or fuzz.token_sort_ratio(keyword, i["institution"]) == 100 or re.search(keyword, i["stuId"]) != None:
                    temp.append(i)
            total=len(temp)
            returnList={'data':[],'total':total}
            if j * 10 + 10 <= total:
                for i in range(j * 10, j * 10 + 10):
                    returnList['data'].append(temp[i])
            else:
                for i in range(j * 10, total):
                    returnList['data'].append(temp[i])
        else:
            total = len(stuList)
            returnList={'data':[],'total':total}
            if j*10+10<=total:
                for i in range(j*10,j*10+10):
                    returnList['data'].append(stuList[i])
            else:
                for i in range(j * 10, total):
                    returnList['data'].append(stuList[i])

        # 3 ，返回响应
        return http.JsonResponse(returnList, safe=False)

        

    def post(self, request):
        """创建学生对象"""
        # 1，获取参数
        dict_data = json.loads(request.body.decode())
        institution = dict_data.get("institution")
        stuId = dict_data.get("stuId")
        cidNum = dict_data.get("cidNum")
        stuName = dict_data.get("stuName")
        phone = dict_data.get("phone")

        # 2，校验参数(暂时省略)
        # 3，数据入库
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        stuData = {'Student_info:StuName': stuName, 'Student_info:Phone': phone, 'CID:cidNumber': cidNum}
        rowKey = institution + '$' + stuId
        stuTable.put(row=rowKey, data=stuData)
        # 4，返回响应
        info = dict(stuTable.row(rowKey))
        stu_dict = {
            "institution": rowKey.split("$")[0],
            "stuId": rowKey.split("$")[1],
            "cidNum": info[b'CID:cidNumber'].decode(),
            "stuName": info[b'Student_info:StuName'].decode(),
            "phone": info[b'Student_info:Phone'].decode()
        }
        return http.JsonResponse(stu_dict, safe=False)

    def delete(self, request):
        deleteStuId = request.GET.getlist("deleteStuId")
        deleteInstitution = request.GET.getlist("deleteInstitution")
        print(request)

        for index in range(len(deleteStuId)):
            # 1,获取数据
            rk = deleteInstitution[index] + '$' + deleteStuId[index]
            # 2 删除数据
            connection = happybase.Connection('47.100.92.57')
            stuTable = connection.table('stuTable')
            stuTable.delete(rk)

        # 3 返回响应
        return http.HttpResponse(status=204)

    def put(self, request):
        # 1, 获取参数,对象
        dict_data = json.loads(request.body.decode())
        cidNum = dict_data.get("cidNum")
        stuName = dict_data.get("stuName")
        phone = dict_data.get("phone")
        stuId = dict_data.get("stuId")
        institution = dict_data.get("institution")
        rk = institution + '$' + stuId
        print(rk)
        # 2, 校验参数（省略）
        # 3，数据入库
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        print(stuTable.row(rk))
        info = dict(stuTable.row(rk))
        if info:
            stuData = {'Student_info:StuName': stuName, 'Student_info:Phone': phone, 'CID:cidNumber': cidNum}
            stuTable.put(row=rk, data=stuData)
        # 4，返回响应
        info = dict(stuTable.row(rk))

        stu_dict = {
            "institution": rk.split("$")[0],
            "stuId": rk.split("$")[1],
            "cidNum": info[b'CID:cidNumber'].decode(),
            "stuName": info[b'Student_info:StuName'].decode(),
            "phone": info[b'Student_info:Phone'].decode()
        }
        return http.JsonResponse(stu_dict, safe=False)

class StuDLUTInfoView(View):
    def get(self, request):
        """获取所有学生信息"""
        # 1 ，查询
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        # 2 ，转Json
        j = eval(request.GET.get('page')) - 1  # 获取当前页数，并将页数值-1
        stuList = []
        for key, value in stuTable.scan():
            stu_dict = {
                "institution": key.decode().split("$")[0],
                "stuId": key.decode().split("$")[1],
                "cidNum": value[b'CID:cidNumber'].decode(),
                "stuName": value[b'Student_info:StuName'].decode(),
                "phone": value[b'Student_info:Phone'].decode()
            }
            if stu_dict["institution"]=="dlut":
                stuList.append(stu_dict)
        keyword = request.GET.get('input')
        if keyword != '':
            temp = []
            for i in stuList:
                if fuzz.token_sort_ratio(keyword, i["stuName"]) == 100 or fuzz.token_sort_ratio(keyword, i[
                    "institution"]) == 100 or re.search(keyword, i["stuId"]) != None:
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
            total = len(stuList)
            returnList = {'data': [], 'total': total}
            if j * 10 + 10 <= total:
                for i in range(j * 10, j * 10 + 10):
                    returnList['data'].append(stuList[i])
            else:
                for i in range(j * 10, total):
                    returnList['data'].append(stuList[i])

        # 3 ，返回响应
        return http.JsonResponse(returnList, safe=False)

    def post(self, request):
        """创建学生对象"""
        # 1，获取参数
        dict_data = json.loads(request.body.decode())
        institution = dict_data.get("institution")
        stuId = dict_data.get("stuId")
        cidNum = dict_data.get("cidNum")
        stuName = dict_data.get("stuName")
        phone = dict_data.get("phone")

        # 2，校验参数(暂时省略)
        # 3，数据入库
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        stuData = {'Student_info:StuName': stuName, 'Student_info:Phone': phone, 'CID:cidNumber': cidNum}
        rowKey = institution + '$' + stuId
        stuTable.put(row=rowKey, data=stuData)
        # 4，返回响应
        info = dict(stuTable.row(rowKey))
        stu_dict = {
            "institution": rowKey.split("$")[0],
            "stuId": rowKey.split("$")[1],
            "cidNum": info[b'CID:cidNumber'].decode(),
            "stuName": info[b'Student_info:StuName'].decode(),
            "phone": info[b'Student_info:Phone'].decode()
        }
        return http.JsonResponse(stu_dict, safe=False)

    def delete(self, request):
        deleteStuId = request.GET.getlist("deleteStuId")
        deleteInstitution = request.GET.getlist("deleteInstitution")
        print(request)

        for index in range(len(deleteStuId)):
            # 1,获取数据
            rk = deleteInstitution[index] + '$' + deleteStuId[index]
            # 2 删除数据
            connection = happybase.Connection('47.100.92.57')
            stuTable = connection.table('stuTable')
            stuTable.delete(rk)

        # 3 返回响应
        return http.HttpResponse(status=204)

    def put(self, request):
        # 1, 获取参数,对象
        dict_data = json.loads(request.body.decode())
        cidNum = dict_data.get("cidNum")
        stuName = dict_data.get("stuName")
        phone = dict_data.get("phone")
        stuId = dict_data.get("stuId")
        institution = dict_data.get("institution")
        rk = institution + '$' + stuId
        print(rk)
        # 2, 校验参数（省略）
        # 3，数据入库
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        print(stuTable.row(rk))
        info = dict(stuTable.row(rk))
        if info:
            stuData = {'Student_info:StuName': stuName, 'Student_info:Phone': phone, 'CID:cidNumber': cidNum}
            stuTable.put(row=rk, data=stuData)
        # 4，返回响应
        info = dict(stuTable.row(rk))

        stu_dict = {
            "institution": rk.split("$")[0],
            "stuId": rk.split("$")[1],
            "cidNum": info[b'CID:cidNumber'].decode(),
            "stuName": info[b'Student_info:StuName'].decode(),
            "phone": info[b'Student_info:Phone'].decode()
        }
        return http.JsonResponse(stu_dict, safe=False)

# 2 详情视图
class StuInfoDetailView(View):
    def get(self, request, institution, stuId):
        # 1 通过pk获取对象
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        rk = institution + '$' + stuId
        info = dict(stuTable.row(rk))
        # 2 转Json
        stu_dict = {
            "institution": rk.split("$")[0],
            "stuId": rk.split("$")[1],
            "cidNum": info[b'CID:cidNumber'].decode(),
            "stuName": info[b'Student_info:StuName'].decode(),
            "phone": info[b'Student_info:Phone'].decode()
        }
        # 3 返回响应
        return http.JsonResponse(stu_dict, safe=False)

    def put(self, request, institution, stuId):
        # 1, 获取参数,对象
        dict_data =  demjson.decode(request.body)
        cidNum = dict_data.get("cidNum")
        stuName = dict_data.get("stuName")
        phone = dict_data.get("phone")
        rk = institution + '$' + stuId
        # 2, 校验参数（省略）
        # 3，数据入库
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        info = dict(stuTable.row(rk))
        if info:
            stuData = {'Student_info:StuName': stuName, 'Student_info:Phone': phone, 'CID:cidNumber': cidNum}
            stuTable.put(row=rk, data=stuData)
        # 4，返回响应
        info = dict(stuTable.row(rk))
        stu_dict = {
            "institution": rk.split("$")[0],
            "stuId": rk.split("$")[1],
            "cidNum": info[b'CID:cidNumber'].decode(),
            "stuName": info[b'Student_info:StuName'].decode(),
            "phone": info[b'Student_info:Phone'].decode()
        }
        return http.JsonResponse(stu_dict, safe=False)

    def delete(self, request, institution, stuId):
        # 1,获取数据
        rk = institution + '$' + stuId
        # 2 删除数据
        connection = happybase.Connection('47.100.92.57')
        stuTable = connection.table('stuTable')
        stuTable.delete(rk)
        # 3 返回响应
        return http.HttpResponse(status=204)


# 2 数据处理视图
class PhotoHandleView(View):
    def post(self, request):
        """创建学生对象"""
        # 1，获取参数
        print(request.body.decode())
        dict_data = json.loads(request.body.decode())
        institution = dict_data.get("Institution")
        stuId = dict_data.get("Stuid")
        cidNum = dict_data.get("cidNum")
        cidPhoto = dict_data.get("cidPhoto")
        rk = institution + '$' + stuId

        # 2，校验参数(暂时省略)
        # 3，数据入库
        connection = happybase.Connection('47.94.147.71')
        stuTable = connection.table('stuTable')
        info = dict(stuTable.row(rk))
        if info:
             stuData = {'CID:cidNumber': cidNum, 'CID:cidPhoto': cidPhoto}
             result = stuTable.put(row=rk, data=stuData)
        # 4，返回响应
        # info = dict(stuTable.row(rowKey))
        # stu_dict = {
        #     "institution": rowKey.split("$")[0],
        #     "stuId": rowKey.split("$")[1],
        #     "cidNum": info[b'CID:cidNumber'].decode(),
        #     "stuName": info[b'Student_info:StuName'].decode(),
        #     "phone": info[b'Student_info:Phone'].decode()
        # }
        return http.JsonResponse(result, safe=False)
