from odoo import models, fields, api
import base64
from io import BytesIO
try:
    from PIL import Image
except ImportError:
    Image = None

class Magang(models.Model):
    _name = 'magang.record'
    _description = 'Data Magang'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nama Peserta', required=True, tracking=True)
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='No. Telepon')
    start_date = fields.Date(string='Tanggal Mulai', tracking=True)
    end_date = fields.Date(string='Tanggal Selesai', tracking=True)
    divisi = fields.Selection([
        ('programmer', 'Programmer'),
        ('designer', 'Designer'),
        ('humas', 'Humas')
    ], string='Divisi', default='programmer', tracking=True)
    status = fields.Selection([
        ('ongoing', 'Sedang Berjalan'),
        ('completed', 'Selesai'),
        ('canceled', 'Dibatalkan')
    ], string='Status', default='ongoing', tracking=True)
    notes = fields.Text(string='Catatan')
    image = fields.Binary(string='Foto', attachment=True)
    image_small = fields.Binary(string='Foto Kecil', attachment=True, store=True)
    
    progress_ids = fields.One2many('magang.progress', 'magang_id', string='Daftar Progres')
    
    progress_count = fields.Integer(string='Jumlah Progres', compute='_compute_progress_count')
    
    last_progress_date = fields.Date(string='Progres Terakhir', compute='_compute_last_progress')
    last_progress_desc = fields.Text(string='Deskripsi Terakhir', compute='_compute_last_progress')

    @api.onchange('image') 
    def _onchange_image(self):
        if self.image and Image:
            image = Image.open(BytesIO(base64.b64decode(self.image)))
            image.thumbnail((64,64))
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            self.image_small = base64.b64encode(buffer.getvalue())
            
    @api.depends('progress_ids')
    def _compute_progress_count(self):
        for record in self:
            record.progress_count = len(record.progress_ids)
            
    @api.depends('progress_ids')
    def _compute_last_progress(self):
        for record in self:
            progress = record.progress_ids.sorted('date', reverse=True)
            if progress:
                record.last_progress_date = progress[0].date
                record.last_progress_desc = progress[0].description
            else:
                record.last_progress_date = False
                record.last_progress_desc = False
                
    def action_view_progresses(self):
        self.ensure_one()
        return {
            'name': f'Progres {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'magang.progress',
            'view_mode': 'tree,form',
            'domain': [('magang_id', '=', self.id)],
            'context': {'default_magang_id': self.id},
        }