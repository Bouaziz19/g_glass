from odoo import api, fields, models
from odoo.tools import safe_eval


class GG_commande(models.Model):
    _name = 'gg_commande'
    _description = 'gg_commande'
    name = fields.Char(string='Name')
    field_name = fields.Many2many('comodel_name', string='')
    ids__operation = fields.Many2many('gg_operation', string='gg_operation')
    ids__lin_commande = fields.One2many( 'gg_lin_commande', 'id_gg_commande', string='ids__lin_commande')
    ids__lin_com2 = fields.One2many('gg_lin_com2', 'id_gg_commande', string='ids__lin_com2')
    @api.one
    def pri(self):
        return self.env.ref('g_glass.action_report_gg_commande5').report_action(self)
    @api.one
    def get_sale_order_data(self):
        self.calc()
        ll=[];
        
        for rec in  self.ids__lin_commande:
            da=[]
            da.append("commande verre")
            da.append(rec.longueur)
            da.append(rec.largeur)
            da.append(rec.Qte)
            da.append(rec.prix_p)
            da.append(rec.total_m)
            ll.append(da)
        for rec in  self.ids__lin_com2:
            da=[]
            print(rec)
            print(rec.id_gg_produit)
            
            
            if str(rec.id_gg_produit) == "gg_produit()":
                
                da.append(rec.name)
            else:
                da.append(rec.id_gg_produit.name)
            da.append("-- -- --")
            da.append("-- -- --")
            da.append(rec.qent)
            da.append(rec.unti)
            da.append(rec.qent*rec.unti)
            ll.append(da)
            print(ll)
        return ll
    id_gg_partner = fields.Many2one('gg_partner', string='Client')
    in_data = fields.Char(string='in_data')
    totale = fields.Float(string='totale')
    d_chi=fields.Float(string='d_chi')
    prix_p=fields.Float(string='prix_p')
    
    # prix_p = fields.Float(compute='_c_prix_p', store=True)
    # @api.depends('totale','')
    # def _c_prix_p(self):
    #     self.prix_p=10
    #     pass
    def valid(self):
        for rec in self.ids__lin_com2:
            rec.id_gg_produit.qent_stk-=rec.qent

        data = {}
        sperimeter = 0
        sarea = 0
        for rec in self.ids__lin_commande:
            r_area= rec.longueur*rec.largeur*rec.Qte
            r_peri = (2*(rec.longueur+rec.largeur))*rec.Qte
            r_data = {}
            r_data["area"] = r_area
            r_data["perimeter"] = r_peri
            r_data["fix"] = 1
            for rec2 in rec.ids__operation:
                rec2.fun_calc(r_data,1)[0]
            sperimeter += r_peri
            sarea +=r_area
            
        data["area"] = sarea
        data["perimeter"] = sperimeter
        data["fix"] = 1
        self.in_data = str(data)
        # functio nculc all
        
        for rec in self.ids__operation:
            rec.fun_calc(data,1)[0]

    # @api.onchange("ids__operation", "ids__lin_commande","ids__lin_com2")
    # def bt1(self):
    #     stotale = 0
    #     data = {}
        
    #     sperimeter = 0
    #     sarea = 0
    #     for rec in self.ids__lin_commande:
    #         r_area= rec.longueur*rec.largeur*rec.Qte
    #         r_peri = (2*(rec.longueur+rec.largeur))*rec.Qte
    #         r_data = {}
    #         r_data["area"] = r_area
    #         r_data["perimeter"] = r_peri
    #         r_data["fix"] = 1
    #         for rec2 in rec.ids__operation:
    #             stotale += rec2.fun_calc(r_data)[0]
            
    #         sperimeter += r_peri
    #         sarea +=r_area
            
    #     data["area"] = sarea
    #     data["perimeter"] = sperimeter
    #     data["fix"] = 1
    #     self.in_data = str(data)
    #     # functio nculc all
        
    #     for rec in self.ids__operation:
    #         stotale += rec.fun_calc(data)[0]
    #     for rec in self.ids__lin_com2:
    #         stotale += rec.qent*rec.unti
    #     self.totale = stotale
    

    # @api.onchange("calc")
    def calc(self):
        
        
        stotale = 0
        data = {}
        
        sperimeter = 0
        sarea = 0
        sfix=0
        for rec in self.ids__lin_commande:
            r_area= rec.longueur*rec.largeur*rec.Qte
            r_peri = (2*(rec.longueur+rec.largeur))*rec.Qte
            sperimeter += r_peri
            sarea +=r_area
            sfix +=1
 
        data["area"] = sarea
        data["perimeter"] = sperimeter
        data["fix"] = sfix
        self.in_data = str(data)
        # av calc d_chi
        for rec in self.ids__operation:
            stotale += rec.fun_calc(data)[0]
        data["area"] = sarea+(((sarea*100)/(100-self.d_chi))*((self.d_chi/100)))
        # apri calc d_chi
        # functio nculc all
        lis=[self.id_vv1.id,self.id_vv2.id,self.id_vv3.id,self.id_vv4.id,self.id_vv5.id]
        ob1 = self.env['gg_2v'].search([('id_vv', '=', self.id_vv1.id)])
        for ob in lis:
            ob1 = self.env['gg_2v'].search([('id_vv', '=', ob)])
            for rec in ob1.ids__operation:
                stotale += rec.fun_calc(data)[0]
        
        self.prix_p=stotale/sarea
        for rec in self.ids__lin_com2:
            stotale += rec.qent*rec.unti
        self.totale = stotale
        
    

    #  vv
    id_vv1 = fields.Many2one('gg_pro_glass', string='pro_glass')
    id_vv2 = fields.Many2one('gg_pro_glass', string='pro_glass')
    id_vv3 = fields.Many2one('gg_pro_glass', string='pro_glass')
    id_vv4 = fields.Many2one('gg_pro_glass', string='pro_glass')
    id_vv5 = fields.Many2one('gg_pro_glass', string='pro_glass')

    state = fields.Selection([
        ('et1', 'et1'),
        ('et2', 'et2'),
        ('et3', 'et3'),
        ('et4', 'et4'),],
        string='Status', default='et1')
    code_2v = fields.Char(string='code_2v')
    

class GG_partner(models.Model):
    _name = "gg_partner"
    _inherits = {'res.partner': 'partner_id'}

class GG_lin_commande(models.Model):
    _name = 'gg_lin_commande'
    _description = 'gg_lin_commande'
    name = fields.Char(string='Name')
    id_gg_commande = fields.Many2one('gg_commande', string='gg_commande')
    longueur = fields.Float(string='Largeur',digits=(10, 4))
    largeur = fields.Float(string='Hauteur',digits=(10, 4))
    prix_p=fields.Float(related='id_gg_commande.prix_p', store=False, string='Prix Unitaire', readonly=True,digits=(10, 4))
    Qte = fields.Float(string='Qté', default=1,digits=(10, 4))
    ids__operation = fields.Many2many('gg_operation', string='gg_operation')
    # total_m = fields.Float(string='Montant HT')
    
    total_m = fields.Float(compute='_c_total_m',string='Montant HT',digits=(10, 4))
    @api.one
    @api.depends('longueur','largeur','prix_p','Qte')
    def _c_total_m(self):
        self.total_m=self.longueur*self.largeur*self.prix_p*self.Qte
        # self.total_m=10
        

class GG_lin_com2(models.Model):
    _name = 'gg_lin_com2'
    _description = 'gg_lin_com2'
    name = fields.Char(string='Name')
    id_gg_produit = fields.Many2one('gg_produit', string='produit')
    id_gg_commande = fields.Many2one('gg_commande', string='gg_commande')
    qent = fields.Float(string='qent')
    unti = fields.Float(string='prix unti')

    @api.onchange("id_gg_produit")
    def bt1(self):
        self.unti=self.id_gg_produit.prix_unti
        pass
class GG_produit(models.Model):
    _name = 'gg_produit'
    _description = 'gg_produit'
    name=fields.Char(string="code d'article")
    code=fields.Char(string='article')
    prix_unti=fields.Float(string='prix unti')
    qent_stk=fields.Float(string='Qté stock ')
    unit_mes=fields.Char(string='unité de mesure')
    prix_G=fields.Float(string='prix_G')
    
    

class GG_pro_glass(models.Model):
    _name = 'gg_pro_glass'
    _description = 'gg_pro_glass'
    name  =  fields.Char(string="code d'article")
    QteBoite  =  fields.Char(string="QteBoite")
    DesignationA  =  fields.Char(string="DesignationA")
    PrixaA  =  fields.Float(string='PrixaA')
    PvDA  =  fields.Float(string='PvDA')
    PvGA  =  fields.Float(string='PvGA')
    PvFA  =  fields.Float(string='PvFA')
    QteA  =  fields.Float(string='QteA')
    lon  =  fields.Float(string='longueur')
    lar  =  fields.Float(string='largeur')
    Feuille  =  fields.Float(string='Feuille')
    ReferenceA  =  fields.Char(string="ReferenceA")
    p_type = fields.Selection([
        ('gla', 'glass'),
        ('Int', 'intercal'),

        ],
        string='p_type', default='gla')
class GG_facteur(models.Model):
    _name = 'gg_facteur'
    _description = 'gg_facteur'

    name = fields.Char(string='Name')
    id_gg_produit = fields.Many2one('gg_produit', string='produit')
    state = fields.Selection([
        ('et', 'entrée en stock '),
        ('so', ' sortie de stoc'),],
        string='Status', default='et')
    qent=fields.Float(string='Qté  ')
    @api.one
    def fun_calc(self):
        if(self.state=='et'):
            self.id_gg_produit.qent_stk+=self.qent
        else:
            self.id_gg_produit.qent_stk-=self.qent

class GG_operation(models.Model):
    _name = 'gg_operation'
    _description = 'gg_operation'
    name = fields.Char(string='Name')
    code = fields.Char(string='code operation')
    qent = fields.Float(string='prix unit', default=0,digits=(10, 4))
    PrixaA  =  fields.Float(string='PrixaA')
    PvDA  =  fields.Float(string='PvDA')
    id_gg_produit = fields.Many2one('gg_produit', string='produit')
    op_type  = fields.Selection([
        ('t1', 't1'),
        ('t2', 't2'),
        ],
        string='op_type', default='t1')
    key_data = fields.Selection([
        ('perimeter', 'perimeter'),
        ('area', 'area'),
        ('fix', 'fix'),
    ], string='key')

    _sql_constraints = [
        ('unique_code', 'unique (code)', 'code value must be unique!')]

    @api.one
    def fun_calc(self, val,d=0):
        if d==0:
            q = self.qent*val[self.key_data]
        else:
            self.id_gg_produit.qent_stk-=val[self.key_data]
            q = 0
        
        return q

#   vitrine
class GG_vit_para(models.Model):
    _name = 'gg_vit_para'
    _description = 'gg_vit_para'
    name = fields.Char(string='Name')

class GG_vit_typ(models.Model):
    _name = 'gg_vit_typ'
    _description = 'gg_vit_typ'
    name = fields.Char(string='Name')
    plan_vit = fields.Binary(string='plan_vit')
    ids_vit_para  = fields.Many2many('gg_vit_para', string='ids_vit_para')
    func = fields.Text(string='function')

class GG_lin_vit(models.Model):
    _name = 'gg_lin_vit'
    _description = 'gg_lin_vit'
    id_vit_para  = fields.Many2one('gg_vit_para', string='gg_vit_para')
    value = fields.Float(string='value')
    id_vit   = fields.Many2one('gg_vit', string='id_vit')

class GG_vit(models.Model):
    _name = 'gg_vit'
    _description = 'gg_vit'
    _inherits = {'gg_commande': 'gg_commande_id'}

    id_vit_typ   = fields.Many2one('gg_vit_typ', string='id_vit_typ')
    plan_vit = fields.Binary(related='id_vit_typ.plan_vit', store=False, string='plan_vit', readonly=True)
    ids_lin_vit  = fields.One2many('gg_lin_vit','id_vit', string='ids_lin_vit')

    state = fields.Selection([
        ('st', 'sel_typ'),
        ('av', 'add val'),
        ('gc', 'gen_commande'),],
        string='Status', default='st')
    @api.one
    def st_st(self):
        self.state="st"
    @api.one
    def st_gc(self):
        self.state="gc"
    @api.one
    def st_av(self):
        self.state="av"

    def fun_ex(self,parameter_list):
        #pre fix
        s_pri_f="""
            global out
            out=[]
            def add_p(lo=0,la=0,q=0):
                if (lo > la):
                    bef={"longueur":lo,"largeur":la,"Qte":q}
                else :
                    bef={"longueur":la,"largeur":lo,"Qte":q}
                global out
                out.append(bef)"""
        s_pri_f=s_pri_f.replace("            ", "")
        cr=self.id_vit_typ.func
        #inp
        inp={}
        for rec in self.ids_lin_vit:
            num=rec.id_vit_para.name
            val=rec.value
            inp[num]=val
        
        #si fix
        s_si_f="""
            for val in out:
                self.ids__lin_commande = [(0,0,val)]
                print("fff")
                """
        s_si_f=s_si_f.replace("            ", "")
        s_ex=s_pri_f+"\n"+cr+"\n"+s_si_f
       
        self.state="gc"
        excod= compile(s_ex, '<string>', 'exec')
        exec(excod)

    # add parametre type vitr
    def aptvt(self,parameter_list):
        self.state="av"
        
        for rec in self.id_vit_typ.ids_vit_para:
             # id_vit_para
             val={"value":1,"id_vit_para":rec}
             self.ids_lin_vit =[(0,0,val)]

class GG_2v(models.Model):
    _name = 'gg_2v'
    _description = 'gg_2v'
    name=fields.Char(string="code")
    active = fields.Boolean('Active', default=True)
    #  vv
    id_vv = fields.Many2one('gg_pro_glass', string='pro_glass')
   
    ids__operation = fields.Many2many('gg_operation', string='gg_operation')
  
    @api.onchange("id_vv")
    def bt1(self):
        self.name= " / "+str(self.id_vv.name)
