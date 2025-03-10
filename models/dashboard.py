from odoo import models, fields, api

class MagangDashboard(models.Model):
    _name = 'magang.dashboard'
    _description = 'Dashboard Magang'
    
    name = fields.Char(string='Nama', default='Dashboard')
    
    # Magang statistics
    total_magang = fields.Integer(string='Total Peserta Magang', compute='_compute_statistics')
    active_magang = fields.Integer(string='Peserta Aktif', compute='_compute_statistics')
    completed_magang = fields.Integer(string='Magang Selesai', compute='_compute_statistics')
    canceled_magang = fields.Integer(string='Magang Dibatalkan', compute='_compute_statistics')
    
    # Progress statistics
    total_progress = fields.Integer(string='Total Laporan Progres', compute='_compute_statistics')
    approved_progress = fields.Integer(string='Progres Disetujui', compute='_compute_statistics')
    pending_progress = fields.Integer(string='Progres Menunggu Persetujuan', compute='_compute_statistics')
    
    # Divisi statistics
    programmer_count = fields.Integer(string='Jumlah Programmer', compute='_compute_statistics')
    designer_count = fields.Integer(string='Jumlah Designer', compute='_compute_statistics')
    humas_count = fields.Integer(string='Jumlah Humas', compute='_compute_statistics')
    
    def action_refresh_dashboard(self):
        self.ensure_one()
        self._compute_statistics()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    @api.model
    def default_get(self, fields_list):
        res = super(MagangDashboard, self).default_get(fields_list)
        
   
        self._compute_dashboard_data(res)
        return res
    
    def _compute_dashboard_data(self, values):
        # Hitung statistik peserta magang
        magang_model = self.env['magang.record']
        values['total_magang'] = magang_model.search_count([])
        values['active_magang'] = magang_model.search_count([('status', '=', 'ongoing')])
        values['completed_magang'] = magang_model.search_count([('status', '=', 'completed')])
        values['canceled_magang'] = magang_model.search_count([('status', '=', 'canceled')])
        
        # Hitung statistik laporan progres
        progress_model = self.env['magang.progress']
        values['total_progress'] = progress_model.search_count([])
        values['approved_progress'] = progress_model.search_count([('state', '=', 'approved')])
        values['pending_progress'] = progress_model.search_count([('state', '=', 'submitted')])
        
        # Hitung statistik per divisi
        values['programmer_count'] = magang_model.search_count([('divisi', '=', 'programmer')])
        values['designer_count'] = magang_model.search_count([('divisi', '=', 'designer')])
        values['humas_count'] = magang_model.search_count([('divisi', '=', 'humas')])
        
        return values
    

    
    @api.depends('name')
    def _compute_statistics(self):
        for record in self:
            # Total magang by status
            record.total_magang = self.env['magang.record'].search_count([])
            record.active_magang = self.env['magang.record'].search_count([('status', '=', 'ongoing')])
            record.completed_magang = self.env['magang.record'].search_count([('status', '=', 'completed')])
            record.canceled_magang = self.env['magang.record'].search_count([('status', '=', 'canceled')])
            
            # Total progress by state
            record.total_progress = self.env['magang.progress'].search_count([])
            record.approved_progress = self.env['magang.progress'].search_count([('state', '=', 'approved')])
            record.pending_progress = self.env['magang.progress'].search_count([('state', '=', 'submitted')])
            
            # Divisi counts
            record.programmer_count = self.env['magang.record'].search_count([('divisi', '=', 'programmer')])
            record.designer_count = self.env['magang.record'].search_count([('divisi', '=', 'designer')])
            record.humas_count = self.env['magang.record'].search_count([('divisi', '=', 'humas')])
            
    # Dummy method untuk membuat record dashboard jika belum ada
    @api.model
    def get_dashboard(self):
        dashboard = self.search([], limit=1)
        if not dashboard:
            dashboard = self.create({'name': 'Dashboard Magang'})
        return dashboard.id