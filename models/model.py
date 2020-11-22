from odoo import api, fields, models


class GG_commande(models.Model):
    _name = 'gg_commande'
    _description = 'gg_commande'
    name = fields.Char(string='Name')

    ids_gg_operation = fields.Many2many('gg_operation', string='gg_operation')
    ids_gg_lin_commande = fields.One2many(
        'gg_lin_commande', 'id_gg_commande', string='ids_gg_lin_commande')
    ids_gg_lin_com2 = fields.One2many(
        'gg_lin_com2', 'id_gg_commande', string='ids_gg_lin_com2')

    id_gg_partner = fields.Many2one('gg_partner', string='gg_partner')
    in_data = fields.Char(string='in_data')
    totale = fields.Float(string='totale')

    @api.onchange("ids_gg_operation", "ids_gg_lin_commande","ids_gg_lin_com2")
    def bt1(self):
        data = {}
        sperimeter = 0
        sarea = 0
        for rec in self.ids_gg_lin_commande:
            sarea += rec.longueur*rec.hauteur*rec.Qte
            sperimeter += (2*(rec.longueur+rec.hauteur))*rec.Qte
        data["area"] = sarea
        data["perimeter"] = sperimeter
        data["fix"] = 1
        self.in_data = str(data)
        print(self.in_data)
        # functio nculc all
        stotale = 0
        for rec in self.ids_gg_operation:
            stotale += rec.fun_calc(data)[0]
        for rec in self.ids_gg_lin_com2:
            stotale += rec.qent*rec.unti
        self.totale = stotale


class GG_partner(models.Model):
    _name = "gg_partner"
    _inherits = {'res.partner': 'partner_id'}


class GG_lin_commande(models.Model):
    _name = 'gg_lin_commande'
    _description = 'gg_lin_commande'
    id_gg_commande = fields.Many2one('gg_commande', string='gg_commande')
    longueur = fields.Float(string='longueur')
    hauteur = fields.Float(string='hauteur')
    Qte = fields.Float(string='Qté', default=1)


class GG_lin_com2(models.Model):
    _name = 'gg_lin_com2'
    _description = 'gg_lin_com2'
    id_gg_commande = fields.Many2one('gg_commande', string='gg_commande')
    qent = fields.Float(string='qent')
    unti = fields.Float(string='unti')


class GG_facteur(models.Model):
    _name = 'gg_facteur'
    _description = 'gg_facteur'

    name = fields.Char(string='Name')


class GG_operation(models.Model):
    _name = 'gg_operation'
    _description = 'gg_operation'
    name = fields.Char(string='Name')
    code = fields.Char(string='code operation')
    qent = fields.Float(string='qent', default=1)
    key_data = fields.Selection([
        ('perimeter', 'perimeter'),
        ('area', 'area'),
        ('fix', 'fix'),
    ], string='ddd')

    _sql_constraints = [
        ('unique_code', 'unique (code)', 'code value must be unique!')]

    @api.one
    def fun_calc(self, val):
        print(val)
        print(self.key_data)
        print(val[self.key_data])
        q = self.qent*val[self.key_data]
        return q
