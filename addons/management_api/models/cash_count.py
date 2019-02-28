from flectra import models, fields, api

class CashCount(models.Model):
    _name = 'cash.count'

    pecahan_100 =   fields.Integer(String="Pecahan 100 rb")
    pecahan_50  =   fields.Integer(String="Pecahan 50 rb")
    pecahan_20  =   fields.Integer(String="Pecahan 20 rb")
    pecahan_10  =   fields.Integer(String="Pecahan 10 rb")
    pecahan_5   =   fields.Integer(String="Pecahan 5 rb")
    pecahan_2   =   fields.Integer(String="Pecahan 2 rb")
    pecahan_1   =   fields.Integer(String="Pecahan 1 rb")
    koin        =   fields.Integer(String="Total Koin")
    total_cash  =   fields.Integer(String="Total Cash")
    saldo_aplikasi  =   fields.Integer(String="Saldo Aplikasi")
    selisih  =   fields.Integer(String="Selisih")
    keterangan  =   fields.Text(String="Keterangan")
    date        =   fields.Date(String="Tanggal")