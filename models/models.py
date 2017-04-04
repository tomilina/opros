# -*- coding: utf-8 -*-

from openerp import models, fields, api

class record(models.Model):
    _name = 'opros.record'

    age = fields.Integer('Возраст')
    # country = fields.Many2one('opros.country',string='Страна')
    country = fields.Char(string='Страна')
    # region = fields.Many2one('opros.region',string='Регион')
    region = fields.Char(string='Регион')
    sex = fields.Selection([('male','мужской'),
                            ('female','женский')],'Пол')
    social_net_ids = fields.Many2many(comodel_name="opros.social_net",
                                relation='opros_social_net_rel',
                                column1='id',
                                column2='att_id',
                                string="Какими соц.сетями пользуетесь чаще")

    name = fields.Many2one('opros.university_name', string='Название университета')
    remoteip = fields.Char('IP-адрес пользователя')
    headers = fields.Char('Заголовок запроса')
    headers_from = fields.Char('Заголовок запроса FROM')
    email = fields.Char('email')

class social_net(models.Model):
    _name = 'opros.social_net'

    name = fields.Char('Название социальной сети')

class university_name(models.Model):
    _name = 'opros.university_name'

    name = fields.Char('Название университета')

class country(models.Model):
    _name = 'opros.country'

    country_id = fields.Integer('id страны')
    name = fields.Char('Название страны')
    region_ids = fields.One2many('opros.region','country_id', 'Регионы')

    # def get_regions(self):
    #     self.region_ids = self.env['opros.region'].sudo().search([('country', '=', self.country_id)]),on_change='get_regions'

class region(models.Model):
    _name = 'opros.region'

    # country_id = fields.Many2one('opros.country')#id страны
    country_id = fields.Integer('id страны')
    region_id = fields.Integer('id региона')
    name = fields.Char('Название региона')


