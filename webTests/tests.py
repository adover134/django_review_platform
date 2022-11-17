from ajax_datatable.views import AjaxDatatableView
from DBs.models import Review
from django.shortcuts import render


class PermissionAjaxDatatableView(AjaxDatatableView):

    model = Review
    title = 'Review'
    initial_order = [["reviewTitle", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'reviewtitle', 'visible': True, },
        {'name': 'reviewdate', 'visible': True, },
        {'name': 'reviewkind', 'visible': True, },
        {'name': 'id', 'visible': False, },
    ]


def index(request):
    return render(request, 'tt.html', {})
