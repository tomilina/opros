# -*- coding: utf-8 -*-
from openerp import http,api, models, fields, exceptions
import requests
import os
import json
import smtplib
import random
import hashlib

class Opros(http.Controller):

    @http.route('/opros', type='http', auth="public", website=True)
    def person_opros(self, theme='default',
                     vote=False,
                     ip=False,
                     age=False,
                     country=False,
                     region=False,
                     sex=False,
                     social_net_ids=False,
                     name=False,
                     email=None,
                     soc_nets_ids=[],
                     grecaptcha=None,**kw):

        url = "https://www.google.com/recaptcha/api/siteverify"
        grecaptcha_response=[]
        for k in kw:
            if 'g-recaptcha-response' in k:
                grecaptcha_response=kw[k]
        # 'secret': '6Lc_QwsUAAAAACR6d8un-pK-BPWmGh9NnILGbufq', localhost
        # 'secret': '6LcH5gsUAAAAAAKGzvupw5MslyNg4dJteFEDYcH0',
        params = {
            'secret': http.request.env['ir.config_parameter'].sudo().search([('key','=','recapcha_secret')]).value,
            'response': grecaptcha_response
        }
        # 'response': "g-recaptcha-response",# 'remoteip': '91.216.164.4'
        response=requests.post(url,data=params)
        data = json.loads(response.text)
        result = data["success"]

        data_sitekey = http.request.env['ir.config_parameter'].sudo().search([('key','=','recapcha_data_sitekey')]).value

        email_result = None
        message_email = ''
        secret_code = ''

        # messages
        message_age = ''
        message_country = ''
        message_region = ''
        message_name =''

        soc_nets_ids = []
        for k in kw:
            if 'social_net_ids' in k:
                soc_nets_ids.append(int(kw[k]))  # извлекаем из хеш-массива нужные id

        university_names = http.request.env['opros.university_name'].sudo().search([])
        social_nets = http.request.env['opros.social_net'].sudo().search([])
        countries = http.request.env['opros.country'].sudo().search([])
        regions = http.request.env['opros.region'].sudo().search([])
        message_captcha=''
        # ЕСЛИ НЕ ПРОШЛИ КАПЧУ - возвращаем на ту же страничку, сохраняя уже введенные данные
        if vote!=False and not result:
            message_captcha='Пройдите проверку !!!'
            return http.request.render('opros.person_opros', {
                'age': age,
                'country': country,
                'region': region,
                'sex': sex,
                'social_net_ids': social_net_ids,
                'name': name,
                'email': email,
                'university_names': university_names,
                'social_nets': social_nets,
                'countries': countries,
                'regions': regions,
                # 'response': response.text,
                # 'grecaptcha_response': grecaptcha_response,
                'soc_nets_ids': soc_nets_ids,
                # 'result': result,
                'message_captcha': message_captcha,
                # 'handler': handler,
                'email_result': email_result,
                'message_email': message_email,
                'data_sitekey': data_sitekey,
                #'ip': ip,
                # 'secret_code': secret_code
            })

        # ЕСЛИ ПРОШЛИ КАПЧУ - отправляем письмо с кодом и пересылаем на новую страничку, где нужно ввести этот код
        elif vote!=False and result:
            # Отправка кода на почту
            FROM = 'noreply@sibsau.ru'
            TO = str(email)#'nastomila@gmail.com'
            SUBJECT = 'SibSAU Secret Code'

            secret_salt = http.request.env['ir.config_parameter'].sudo().search([('key','=','secret_salt')]).value

            secret_code=str(random.randrange(100000,999999,1))
            TEXT = secret_code#'Hello! Recieved?'
            secret_code = hashlib.md5(secret_salt + TO + str(secret_code)).hexdigest()#хешируем код
            # Prepare actual message
            # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, TO, SUBJECT, TEXT)

            # ЕСЛИ ПИСЬМО ОТПРАВИЛОСЬ НА ПОЧТУ
            try:
                # server = smtplib.SMTP("smtp.gmail.com", 587)
                server = smtplib.SMTP("mail.sibsau.ru", 25)
                server.ehlo()
                # server.starttls()
                # server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                server.close()
                # email_result='successfully sent the mail'
                headers = http.request.httprequest.headers
                return http.request.render('opros.opros_code', {
                    'age': age,
                    'country': country,
                    'region': region,
                    'sex': sex,
                    'soc_nets_ids': soc_nets_ids,
                    'name': name,
                    'email': email,
                    'secret_code': secret_code,
                    'email_result': email_result,
                    'ip': (headers),
                })
            # ЕСЛИ НЕ ОТПРАВИЛОСЬ
            except:
                # email_result="failed to send mail"
                message_email='Невозможно отправить письмо! Проверьте введенное значение или используйте другой email.'

                return http.request.render('opros.person_opros', {
                    'age': age,
                    'country': country,
                    'region': region,
                    'sex': sex,
                    'social_net_ids': social_net_ids,
                    'name': name,
                    'email': email,
                    'university_names': university_names,
                    'social_nets': social_nets,
                    'countries': countries,
                    'regions': regions,
                    # 'response': response.text,
                    # 'grecaptcha_response': grecaptcha_response,
                    'soc_nets_ids': soc_nets_ids,
                    # 'result': result,
                    'message_captcha': message_captcha,
                    # 'handler': handler,
                    # 'email_result': email_result,
                    'message_email': message_email,
                    'data_sitekey': data_sitekey,
                    #'ip': ip,
                })

        elif vote != False and not age:
            message_age = 'Укажите ваш возраст!'
            return http.request.render('opros.person_opros', {
                'age': age,
                'country': country,
                'region': region,
                'sex': sex,
                'social_net_ids': social_net_ids,
                'name': name,
                'email': email,
                'university_names': university_names,
                'social_nets': social_nets,
                'countries': countries,
                'regions': regions,
                'soc_nets_ids': soc_nets_ids,
                'message_captcha': message_captcha,
                'email_result': email_result,
                'message_email': message_email,
                'data_sitekey': data_sitekey,
                #'ip': ip,
                #messages
                'message_age': message_age,
                'message_country': message_country,
                'message_region': message_region,
                'message_name': message_name
            })
        elif vote != False and not country:
            message_country = 'Укажите вашу страну!'
            return http.request.render('opros.person_opros', {
                'age': age,
                'country': country,
                'region': region,
                'sex': sex,
                'social_net_ids': social_net_ids,
                'name': name,
                'email': email,
                'university_names': university_names,
                'social_nets': social_nets,
                'countries': countries,
                'regions': regions,
                'soc_nets_ids': soc_nets_ids,
                'message_captcha': message_captcha,
                'email_result': email_result,
                'message_email': message_email,
                'data_sitekey': data_sitekey,
                #'ip': ip,
                #messages
                'message_age': message_age,
                'message_country': message_country,
                'message_region': message_region,
                'message_name': message_name
            })
        elif vote != False and not region:
            message_region = 'Укажите ваш регион!'
            return http.request.render('opros.person_opros', {
                'age': age,
                'country': country,
                'region': region,
                'sex': sex,
                'social_net_ids': social_net_ids,
                'name': name,
                'email': email,
                'university_names': university_names,
                'social_nets': social_nets,
                'countries': countries,
                'regions': regions,
                'soc_nets_ids': soc_nets_ids,
                'message_captcha': message_captcha,
                'email_result': email_result,
                'message_email': message_email,
                'data_sitekey': data_sitekey,
                #'ip': ip,
                #messages
                'message_age': message_age,
                'message_country': message_country,
                'message_region': message_region,
                'message_name': message_name
            })
        elif vote != False and not name:
            message_name = 'Выберете название!'
            return http.request.render('opros.person_opros', {
                'age': age,
                'country': country,
                'region': region,
                'sex': sex,
                'social_net_ids': social_net_ids,
                'name': name,
                'email': email,
                'university_names': university_names,
                'social_nets': social_nets,
                'countries': countries,
                'regions': regions,
                'soc_nets_ids': soc_nets_ids,
                'message_captcha': message_captcha,
                'email_result': email_result,
                'message_email': message_email,
                'data_sitekey': data_sitekey,
                #'ip': ip,
                #messages
                'message_age': message_age,
                'message_country': message_country,
                'message_region': message_region,
                'message_name': message_name
            })

        # ПРИ ЗАГРУЗКЕ
        else: return http.request.render('opros.person_opros', {
                'age': age,
                'country': country,
                'region': region,
                'sex': sex,
                'social_net_ids': social_net_ids,
                'name': name,
                'email': email,
                'university_names': university_names,
                'social_nets': social_nets,
                'kw': kw,
                'countries': countries,
                'regions': regions,
                'response': response.text,
                'grecaptcha_response': grecaptcha_response,
                'social_net_ids': social_net_ids,
                'soc_nets_ids': soc_nets_ids,
                'result': result,
                'message_captcha': message_captcha,
                #'ip': ip,
                # 'handler': handler,
                # 'email_result': email_result,
                # 'secret_code': secret_code
                'data_sitekey': data_sitekey,
            })

    @http.route('/opros/code', type='http', auth="public", website=True)
    def opros_code(self, theme='default',
                     accept=False,
                     ip=False,
                     age=False,
                     country=False,
                     region=False,
                     sex=False,
                     soc_nets_ids=[],
                     name=False,
                     email='',
                     user_code='',
                     secret_code='',
                     **kw):
        show_chart = http.request.env['ir.config_parameter'].sudo().search([('key','=','show_chart')]).value
        secret_salt = http.request.env['ir.config_parameter'].sudo().search([('key','=','secret_salt')]).value
        user_code_hash=hashlib.md5(secret_salt + email +str(user_code)).hexdigest()
        # trial = 2#количество попыток
        trial=0
        # chart_array = []
        chart_array = ''
        if user_code_hash==str(secret_code) and accept!=False:
            res_record = http.request.env['opros.record']
            if not res_record.search([('email','=',email)]):#если еще нет записи с таким email
                headers = http.request.httprequest.headers
                headers_from = ip
                ip = headers.get('X-Forward-For', http.request.httprequest.remote_addr)
                record_id = res_record.sudo().create({
                    'age': age,
                    'country': country,
                    'region': region,
                    'sex': sex,
                    'name': name,
                    'email': email,
                    'remoteip': ip,
                    'headers': str(headers),
                    'headers_from': headers_from,
                })
                if soc_nets_ids:
                    record_id.social_net_ids= [int(x) for x in (soc_nets_ids.strip('[]')).split(',')]
                trial = 1#успех
                if str(show_chart)=="True":
                    chart_array=chart_array+'['+"'University name'"+','+"'Number of people voted'"+']'+','
                    records = http.request.env['opros.record']
                    university_names = http.request.env['opros.university_name'].sudo().search([])

                    for name in university_names:
                        chart_array=chart_array+'['+"'"+(name.name)+"'"+','+str(records.sudo().search([('name','=',name.id)],count=True))+']'+','
                    chart_array=chart_array[0:-1]#удаляем последнюю запятушку
                    chart_array='['+chart_array+']'#добавляем внешние скобки
            else: #если
                trial = 3#такая почта уже была
        if accept!=False and user_code_hash!=str(secret_code):
            trial=2
        return http.request.render('opros.opros_code',{
            'ip' : ip,
            'age' : age,
            'country' : country,
            'region' : region,
            'sex' : sex,
            'name' : name,
            'soc_nets_ids' : soc_nets_ids,
            'user_code' : user_code,
            'secret_code' : secret_code,
            'trial':trial,
            'chart_array': chart_array,
            'show_chart': show_chart
            # 'university_names':university_names,

        })

    @http.route('/opros/20162017_62534762534765', type='http', auth="public", website=True)
    def opros_code_show(self, theme='default'):
        chart_array = ''
        chart_array = chart_array + '[' + "'University name'" + ',' + "'Number of people voted'" + ']' + ','
        records = http.request.env['opros.record']
        university_names = http.request.env['opros.university_name'].sudo().search([])

        for name in university_names:
            chart_array = chart_array + '[' + "'" + (name.name) + "'" + ',' + str(
                records.sudo().search([('name', '=', name.id)], count=True)) + ']' + ','
        chart_array = chart_array[0:-1]  # удаляем последнюю запятушку
        chart_array = '[' + chart_array + ']'  # добавляем внешние скобки
        return http.request.render('opros.20162017_62534762534765', {
            'chart_array': chart_array
        })

    @http.route(["/ajax/region"], auth="public", type='json', website=True, methods=['POST'])
    def region(self, param, **kw):
        res = http.request.env['opros.region'].sudo().search([('country_id', '=', int(param))])
        values = []
        for x in res:
            v = {}
            v["name"] = x.name
            v["id"] = x.region_id
            values.append(v)
        return values


