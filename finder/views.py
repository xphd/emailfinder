from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import io
import collections
import xlsxwriter
from . import finder
import time

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
            ('first name',''),
            ('last name',''),
            ('company name',''),
            ('domain',''),
            ('Hunter email',''),
            ('Hunter score',0),
            ('Anymail email',''),
            ('RocketReach email',''),]
        person_emails = []
        for index, row in ls.iterrows():
            first_name = row['first name']
            last_name = row['last name']
            company_name = row['company name']
            domain = row['domain']
            hunter_email = ""
            hunter_score = -2
            anymail_email = ""
            rocketreach_email = ""
            person_email = collections.OrderedDict(columns)
            if api_hunter:
                hunter_email,hunter_score = finder.hunter(first_name,last_name,company_name,api_hunter)
            person_email['Hunter email'] = hunter_email
            person_email['Hunter score'] = hunter_score

            if api_anymail and hunter_score < 75:
                anymail_email = finder.anymail(first_name,last_name,company_name,domain,api_anymail)
            person_email['Anymail email'] = anymail_email

            if api_rocketreach and hunter_score < 75 and len(anymail_email)==0:
                rocketreach_email = finder.rocketreach(first_name,last_name,company_name,api_rocketreach)
            person_email['RocketReach email'] = rocketreach_email

            person_email['first name'] = first_name
            person_email['last name'] = last_name
            person_email['company name'] = company_name
            person_email['domain'] = domain
            person_emails.append(person_email)
            time.sleep(0.86)

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
