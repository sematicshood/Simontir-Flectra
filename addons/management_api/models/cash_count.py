from flectra import models, fields, api

class CashCount(models.Model):
    _name = 'cash.count'

    pecahan_100 =   fields.Integer(string="Pecahan 100 rb")
    pecahan_50  =   fields.Integer(string="Pecahan 50 rb")
    pecahan_20  =   fields.Integer(string="Pecahan 20 rb")
    pecahan_10  =   fields.Integer(string="Pecahan 10 rb")
    pecahan_5   =   fields.Integer(string="Pecahan 5 rb")
    pecahan_2   =   fields.Integer(string="Pecahan 2 rb")
    pecahan_1   =   fields.Integer(string="Pecahan 1 rb")
    koin        =   fields.Integer(string="Total Koin")
    total_cash  =   fields.Integer(string="Total Cash")
    saldo_aplikasi  =   fields.Integer(string="Saldo Aplikasi")
    selisih  =   fields.Integer(string="Selisih")
    keterangan  =   fields.Text(string="Keterangan")
    date        =   fields.Date(string="Tanggal")