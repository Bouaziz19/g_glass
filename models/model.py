from odoo import api, fields, models
from odoo.tools import safe_eval


class GG_commande(models.Model):
    _name = 'gg_commande'
    _description = 'gg_commande'
    name = fields.Char(string='Name')
    num=fields.Char(string='commande N :',compute='_compute_num')
    sequence = fields.Integer('sequence', help="Sequence for the handle.",default=10)
    @api.one
    def _compute_num(self):
        self.num='CN_'+str(self.id)
    state = fields.Selection([
            ('0',"Brouillon"),
            ('1', "En cours"),
            ('2', "Terminé"),
            ],
        string='Status', default='0')
    ids__operation = fields.Many2many('gg_operation', string='gg_operation')
    ids__lin_commande = fields.One2many( 'gg_lin_commande', 'id_gg_commande', string='ids__lin_commande')
    ids__lin_com2 = fields.One2many('gg_lin_com2', 'id_gg_commande', string='ids__lin_com2')
    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(GG_commande, self).fields_get(allfields, attributes)
        fields_to_hide = ['write_uid','create_uid','create_date', 'write_date','ids__operation',
                        'ids__lin_commande','ids__lin_com2','in_data','totale','d_chi','prix_p','id_vv1',
                        'id_vv2','id_vv3','id_vv4','id_vv5','code_2v']
        
        for field in fields_to_hide:
            res[field]['selectable'] = False  # disable field visible in filter
            res[field]['sortable'] = False  # disable field visible in grouping
        return res
    @api.one
    def def_kit(self):
        ll=[1,29]
        for val in ll:
            self.ids__lin_com2=[(0,0,{"id_gg_produit":val} )]
        
        pass
    @api.one
    def pri(self):
        return self.env.ref('g_glass.action_report_gg_commande5').report_action(self)
    @api.one
    def to_st_0(self):
        self.state="0"
    @api.one
    def to_st_1(self):
        self.state="1"
    @api.one
    def to_st_2(self):
        self.st_1()
        self.state="2"
    @api.one
    def st_1(self):
        self.calc()
        id_created = self.env['gg_facteur'].create({'name': self.name})
  
        for rec in self.ids__lin_com2:
            id_created.ids__lin_com3=[(0,0,{"id_gg_produit":rec.id_gg_produit.id,"qent":rec.qent,"depot_out":"depot_4"} )]
            # rec.id_gg_produit.qent_stk-=rec.qent

    
        
        
    
    @api.one
    def get_sale_order_data2(self):
        da=[]
        for rec in  self.ids__operation:
            da.append(rec.name)

        return da

    @api.onchange('id_gg_client')
    def _onchange_id_gg_client(self):
        try:
            if self.id_gg_client:
                self.name =self.id_gg_client.name
        except :
            pass
        
    @api.one
    def get_sale_order_data(self):
        
        ll=[];
        
        for rec in  self.ids__lin_commande:
            da=[]
            da.append("C - V")
            da.append(rec.longueur)
            da.append(rec.largeur)
            da.append(rec.Qte)
            da.append(rec.prix_p)
            da.append(rec.total_m)
            ll.append(da)
        for rec in  self.ids__lin_com2:
            da=[]

            
            
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
        return ll
    id_gg_client = fields.Many2one('gg_client', string='Client')
    in_data = fields.Char(string='in_data')
    totale = fields.Float(string='totale',digits=(10, 2))
    

    versement = fields.Float(string='Versement',digits=(10, 2))
    
    d_chi=fields.Float(string='d_chi',digits=(10, 1))
    prix_p=fields.Float(string='prix_p',digits=(10, 2))
    
    # prix_p = fields.Float(compute='_c_prix_p', store=True)
    # @api.depends('totale','')
    # def _c_prix_p(self):
    #     self.prix_p=10
    #     pass
    
    
    def valid(self):
        pass

    # *****************************************
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
        # ob1 = self.env['gg_2v'].search([('id_vv', '=', self.id_vv1.id)])
        for ob in lis:
            
            ob1 = self.env['gg_2v'].search([('id_vv', '=', ob)])
            try:
                for rec in ob1.ids__operation:
                    
                    stotale += rec.fun_calc(data)[0]
            except :
                    pass
        try:
            self.prix_p=stotale/sarea
        except :
            pass
        
        for rec in self.ids__lin_com2:
            stotale += rec.qent*rec.unti
        self.totale = stotale
        


    #  vv
    id_vv1 = fields.Many2one('gg_pro_glass', string='pro_glass')
    id_vv2 = fields.Many2one('gg_pro_glass', string='pro_glass')
    id_vv3 = fields.Many2one('gg_pro_glass', string='pro_glass')
    id_vv4 = fields.Many2one('gg_pro_glass', string='pro_glass')
    id_vv5 = fields.Many2one('gg_pro_glass', string='pro_glass')


    code_2v = fields.Char(string='code_2v')

class GG_lin_commande(models.Model):
    _name = 'gg_lin_commande'
    _description = 'gg_lin_commande'
    name = fields.Char(string='Name')
    id_gg_commande = fields.Many2one('gg_commande', string='gg_commande')
    longueur = fields.Float(string='Largeur',digits=(10, 2))
    largeur = fields.Float(string='Hauteur',digits=(10, 2))
    prix_p=fields.Float(related='id_gg_commande.prix_p', store=False, string='Prix Unitaire', readonly=True,digits=(10, 2))
    Qte = fields.Float(string='Qté', default=1,digits=(10, 2))
    ids__operation = fields.Many2many('gg_operation', string='gg_operation')
    # total_m = fields.Float(string='Montant HT')
    
    total_m = fields.Float(compute='_c_total_m',string='Montant HT',digits=(10, 2))
    @api.one
    @api.depends('longueur','largeur','prix_p','Qte')
    def _c_total_m(self):
        self.total_m=self.longueur*self.largeur*self.prix_p*self.Qte
        
        # self.total_m=10


class GG_lin_com3(models.Model):
    _name = 'gg_lin_com3'
    _description = 'gg_lin_com3'
    name = fields.Char(string='Name')
    id_gg_produit = fields.Many2one('gg_produit', string='produit')
    id_gg_facteur = fields.Many2one('gg_facteur', string='gg_facteur')
    qent = fields.Float(string='qent')
    unti = fields.Float(string='prix unti')

    @api.onchange("id_gg_produit")
    def bt1(self):
        self.unti=self.id_gg_produit.prix_unti
        pass
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
    PrixaA  =  fields.Float(string='PrixaA')
    PvDA  =  fields.Float(string='PvDA')
    PvGA  =  fields.Float(string='PvGA')
    PvGA  =  fields.Float(string='PvGA')
    note=fields.Char(string='note')
    depot_1=fields.Float(string='depot 1', default=0)
    depot_2=fields.Float(string='depot 2', default=0)
    depot_3=fields.Float(string='depot 3', default=0)
    depot_4=fields.Float(string='depot 4', default=0)
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


class GG_client(models.Model):
    _name = 'gg_client'
    _description = 'gg_client'
    name = fields.Char(string='Name')
    code = fields.Char(string='code')
    Mobile = fields.Char(string='Mobile')
    note = fields.Char(string='note')
    Adresse = fields.Char(string='Adresse')

class GG_facteur(models.Model):
    _name = 'gg_facteur'
    _description = 'gg_facteur'
    name = fields.Char(string='Name')
    note = fields.Text(string='Note')
    state = fields.Selection([
            ('0',"Brouillon"),
            ('1', "En cours"),
            ('2', "Terminé"),
            ],
        string='Status', default='0')
    
    depot_in = fields.Selection([
        ('depot_1', 'depot_1'),
        ('depot_2', 'depot_2'),
        ('depot_3', 'depot_3'),
        ('depot_4', 'depot_4'),],
        string='depot_in', default='')
    depot_out = fields.Selection([
        ('depot_1', 'depot_1'),
        ('depot_2', 'depot_2'),
        ('depot_3', 'depot_3'),
        ('depot_4', 'depot_4'),],
        string='depot_out', default='')
    ids__lin_com3 = fields.One2many('gg_lin_com3', 'id_gg_facteur', string='ids__lin_com3')
    
    
    def fun_calc(self):
        for rec in self.ids__lin_com3:
            
            if(self.depot_out=="depot_1"):
                rec.id_gg_produit.depot_1-=rec.qent
            elif(self.depot_out=="depot_2"):
                rec.id_gg_produit.depot_2-=rec.qent
            elif(self.depot_out=="depot_3"):
                rec.id_gg_produit.depot_3-=rec.qent
            elif(self.depot_out=="depot_4"):
                rec.id_gg_produit.depot_4-=rec.qent
            else:
                pass
            
            if(self.depot_in=="depot_1"):
                rec.id_gg_produit.depot_1+=rec.qent
            elif(self.depot_in=="depot_2"):
                rec.id_gg_produit.depot_2+=rec.qent
            elif(self.depot_in=="depot_3"):
                rec.id_gg_produit.depot_3+=rec.qent
            elif(self.depot_in=="depot_4"):
                rec.id_gg_produit.depot_4+=rec.qent
            else:
                pass
        self.state="1"

class GG_operation(models.Model):
    _name = 'gg_operation'
    _description = 'gg_operation'
    name = fields.Char(string='Name')
    code = fields.Char(string='code operation')
    qent = fields.Float(string='prix unit', default=0,digits=(10, 2))
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
