from flask import request, current_app as app
from app import dictify

def paginate(query):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
        
    per_page = app.config['PAGINATION_PER_PAGE']
    offset = (page - 1) * per_page
    total_count = query.count()
    num_pages = total_count // per_page + (total_count % per_page > 0)
    items = query.limit(per_page).offset(offset).all()

    return dictify(locals(), ['page', 'per_page', 'total_count', 'num_pages', 'items'])