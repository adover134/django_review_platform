from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from DBs.models import Review


class PermissionAjaxDatatableView(AjaxDatatableView):

    # 출력할 model
    model = Review
    title = 'Reviews'
    # 초기 정렬 조건
    initial_order = [["reviewKind", "asc"], ]
    # 개수 조절 드롭 박스의 출력 / 한 번에 출력할 column의 수
    length_menu = [[2, 4, 6], [2, 4, 6]]
    # 검색을 위한 or 연산
    search_values_separator = '+'
    # show_column_filters가 True이면 맨 윗줄에 row마다 검색 필터가 생깁니다.
    show_column_filters = False
    column_defs = [
        # render_row_tools_column_def() 는 넣으면 가장 왼쪽에 각 해에 대한 상세 정보를 출력하는 열이 추가됩니다.
        AjaxDatatableView.render_row_tools_column_def(),
        # 'name' : 모델에서의 feature 이름
        # 'visible' : 테이블에서의 출력 여부
        # name : DB에서 해당하는 속성의 이름 - model의 field 이름
        {'name': 'id', 'visible': False, },
        # title 값이 테이블의 헤더로 들어갑니다.
        {'name': 'name1', 'title': '작성자', 'foreign_field': 'uId__first_name', 'visible': False, },
        {'name': 'name2', 'title': '작성자', 'foreign_field': 'uId__last_name', 'visible': False, },
        {'name': 'name2', 'title': '작성자', 'foreign_field': {'uId__last_name', 'uId__last_name'}, 'visible': False, },
        {'name': 'reviewTitle', 'title': '리뷰 제목', 'visible': True, },
        {'name': 'reviewKind', 'visible': True, },
        {'name': '이메일', 'foreign_field': 'uId__email', 'visible': True, },
        {'name': '원룸 주소', 'foreign_field': 'roomId__address', 'visible': True, },
    ]
