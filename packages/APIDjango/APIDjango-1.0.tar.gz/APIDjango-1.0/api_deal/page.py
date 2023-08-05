import math


def get_start_end_inx(data, res, total_count):
    """获取分页页码"""
    page_no = data.get("page_no", "")
    page_rows = data.get("page_rows", "")
    if page_no and str(page_no).isdigit():
        page_no = int(page_no)
    else:
        page_no = 1
    if page_no < 1:
        page_no = 1
    if page_rows and str(page_rows).isdigit():
        page_rows = int(page_rows)
    else:
        page_rows = 20
    if 1 > page_rows > 100:
        page_rows = 20
    total_page = math.ceil(total_count / page_rows)
    page = {
        'page_no': page_no,
        'page_rows': page_rows,
        'total_count': total_count,
        'total_page': total_page
    }
    res['page'] = page
    start_inx = (page_no - 1) * page_rows
    end_inx = page_no * page_rows
    return start_inx, end_inx
