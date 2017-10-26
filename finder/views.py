from django.shortcuts import render

from django.http import HttpResponse
import pandas as pd
import io
import collections
import xlsxwriter
from . import finder

# Create your views here.
def home(request):
    if request.method == 'POST':
######## receive input from frontend BEGIN   ########
        api_hunter = request.POST['api_hunter']
        api_anymail = request.POST['api_anymail']
        api_rocketreach = request.POST['api_rocketreach']
        file = request.FILES['my_input']
        ls = pd.read_excel(file)
######## receive input from frontend END   ########

        columns = [
            ('email',''),
            ('first name',''),
            ('last name',''),
            ('found by',''),
        ]
        person_emails = []
        for index, row in ls.iterrows():
            first_name = row['first name']
            last_name = row['last name']
            company_name = row['company name']
            url = row['url']
            email = ""
            found_by = ""
            if api_hunter:
                email = finder.hunter(first_name,last_name,company_name,url,api_hunter)
                if email:
                    found_by = 'Hunter'
            if api_anymail and len(email) == 0:
                email = finder.anymail(first_name,last_name,company_name,url,api_anymail)
                if email:
                    found_by = 'AnyMail'
            if api_rocketreach and len(email) == 0:
                email = finder.rocketreach(first_name,last_name,company_name,api_rocketreach)
                if email:
                    found_by = 'Rocket Reach'
            person_email = collections.OrderedDict(columns)
            person_email['email'] = email
            person_email['first name'] = first_name
            person_email['last name'] = last_name
            person_email['found by'] = found_by
            person_emails.append(person_email)

######## generate output BEGIN ########
        filename = "output.xlsx"
        excel_file = io.BytesIO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter',options={'remove_timezone': True})

        result = pd.DataFrame(person_emails)

        result.to_excel(xlwriter, sheet_name=filename)
        xlwriter.save()
        xlwriter.close()
        excel_file.seek(0)
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(excel_file.read(),content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=output.xlsx'
        return response
    return render(request,'home.html')
