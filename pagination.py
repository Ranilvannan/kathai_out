import math


class Pagination:
    def __init__(self, total_count, page, per_page):
        self.total_count = total_count
        self.page = page
        self.per_page = per_page
        self.total_page = math.ceil(total_count / per_page)
        self.prev_page = page - 1
        self.next_page = page + 1

    def is_first(self):
        if self.page == 1:
            return True
        return False

    def is_last(self):
        if self.page == self.total_page:
            return True
        return False

    def has_next(self):
        if self.next_page <= self.total_page:
            return True
        return False

    def has_prev(self):
        if self.prev_page > 0:
            return True
        return False

    def is_valid(self):
        if 1 <= self.page <= self.total_page:
            return True
        return False

    def get_pages(self):
        page_list = [self.page]

        if 1 not in page_list:
            page_list.insert(0, 1)

        if self.total_page not in page_list:
            page_list.append(self.total_page)

        if (1 < self.prev_page < self.total_page) and (self.prev_page not in page_list) and self.has_prev():
            page_list.insert(1, '...')

        if (1 < self.next_page < self.total_page) and (self.next_page not in page_list) and self.has_next():
            page_list.insert(len(page_list) - 1, '...')

        return page_list
