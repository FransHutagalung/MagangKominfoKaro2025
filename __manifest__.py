{
    'name': 'Magang Komifo 2025',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Manajemen Magang dan Progres Peserta',
    'author': 'Fransiskus Hutagalung',
    'description': """
Modul ini digunakan untuk mengelola data peserta magang dan progres di Komifo.
==================================================================

Fitur:
- Manajemen data peserta magang
- Pelacakan progres dan aktivitas peserta
- Sistem persetujuan untuk laporan progres
- Tampilan kanban, calendar, dan tree untuk visualisasi data
- Dashboard untuk monitoring dan analisis data magang
    """,
    'website': 'https://www.komifo.com',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/action_views.xml',        
        'views/magang_views.xml',
        'views/progress_views.xml',
        # dashboard biasa
        # 'views/dashboard_form_view.xml',
        # dashboard futuristik
        'views/futuristik_dashboard.xml',
        'views/menu_views.xml',
        'views/menu_dashboard.xml',
        'views/dashboard_init.xml',
        'data/magang_record_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}