from odoo import models, fields, api
from datetime import datetime

class MagangProgress(models.Model):
    _name = 'magang.progress'
    _description = 'Progress Peserta Magang'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Judul Progres', required=True, tracking=True)
    date = fields.Date(string='Tanggal', default=fields.Date.context_today, required=True, tracking=True)
    description = fields.Text(string='Deskripsi Kegiatan', required=True, tracking=True)
    
    # Field untuk lokasi
    location = fields.Char(string='Lokasi Kegiatan', tracking=True)
    map_url = fields.Char(string='URL Google Map', tracking=True, 
                          help="Masukkan URL embed map dari Google Maps")
    
    # Relasi Many2one ke magang.record
    magang_id = fields.Many2one('magang.record', string='Peserta Magang', required=True, ondelete='cascade', tracking=True)
    
    # Field relasi untuk mendapatkan nama peserta
    peserta_name = fields.Char(related='magang_id.name', string='Nama Peserta', store=True, readonly=True)
    peserta_divisi = fields.Selection(related='magang_id.divisi', string='Divisi Peserta', store=True, readonly=True)
    
    # Status progres
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Diajukan'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak')
    ], string='Status', default='draft', tracking=True)
    
    # Field untuk pembimbing
    approved_by = fields.Many2one('res.users', string='Disetujui Oleh', readonly=True, tracking=True)
    approval_date = fields.Datetime(string='Tanggal Persetujuan', readonly=True)
    approval_notes = fields.Text(string='Catatan Pembimbing')
    
    # Field untuk attachment/file
    attachment = fields.Binary(string='Lampiran', attachment=True)
    attachment_filename = fields.Char(string='Nama File')
    
    @api.model
    def create(self, vals):
        # Auto-generate sequence for name if not provided
        if not vals.get('name'):
            peserta = self.env['magang.record'].browse(vals.get('magang_id'))
            date_str = fields.Date.from_string(vals.get('date')).strftime('%d/%m/%Y')
            vals['name'] = f"Progres {peserta.name} - {date_str}"
        return super(MagangProgress, self).create(vals)
    
    def action_submit(self):
        self.write({'state': 'submitted'})
        
    def action_approve(self):
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id,
            'approval_date': fields.Datetime.now()
        })
        
    def action_reject(self):
        self.write({
            'state': 'rejected',
            'approved_by': self.env.user.id,
            'approval_date': fields.Datetime.now()
        })
        
    def action_reset_to_draft(self):
        self.write({
            'state': 'draft',
            'approved_by': False,
            'approval_date': False
        })
        
    def action_download_attachment(self):
        """Metode untuk mendownload lampiran"""
        self.ensure_one()
        if not self.attachment:
            return
            
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=magang.progress&id=%s&field=attachment&filename=%s&download=true' % (self.id, self.attachment_filename),
            'target': 'self',
        }
        
    def action_view_attachment(self):
        """Metode untuk melihat lampiran dalam tampilan penuh"""
        self.ensure_one()
        if not self.attachment:
            return
            
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=magang.progress&id=%s&field=attachment&filename=%s' % (self.id, self.attachment_filename),
            'target': 'new',
        }
    
    def action_view_map(self):
        """Metode untuk membuka peta lokasi kegiatan dalam tampilan baru"""
        self.ensure_one()
        if not self.map_url:
            return
            
        return {
            'type': 'ir.actions.act_url',
            'url': self.map_url,
            'target': 'new',
        }