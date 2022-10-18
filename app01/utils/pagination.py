"""
分页组件


#视图函数中
def pretty_list(request):

    #筛选数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    #实例化分页对象
    page_object = PagInation(request, queryset)

    #分完页的数据
    page_queryset = page_object.page_queryset
    #生成页码html
    page_string = page_object.html()

    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string
    }

    return render(request, "pretty_list.html", context)

#HTML中
    #展示当前数据
                {% for obj in queryset %}
                    <tr>
                        <td>{{ obj.id }}</td>
                        <td>{{ obj.moblie }}</td>
                        <td>{{ obj.price }}</td>
                        <td>{{ obj.level }}</td>
                        <td>{{ obj.status }}</td>
                        <td>
                            <a class="btn btn-primary btn-xs" href="/pretty/{{ obj.id }}/edit/">编辑</a>
                            <a class="btn btn-danger btn-xs" href="/pretty/{{ obj.id }}/delete/">删除</a>
                        </td>
                    </tr>
                {% endfor %}

    #展示页码
    <ul class="pagination">
        {{ page_string }}
    </ul>

"""

from django.utils.safestring import mark_safe
import copy

class PagInation(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=3):


        query_dict = copy.deepcopy(request.GET)
        self.query_dict = query_dict

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page_param = page_param
        self.page = page    #请求页码
        self.page_size = page_size  #页面数据总量
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start: self.end] #符合条件的所有数据

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)

        if div:
            total_page_count += 1

        self.total_page_count = total_page_count #总页数
        self.plus = plus

    def html(self):

        page_start = self.page - self.plus
        page_end = self.page + self.plus + 1
        if page_start <= 0:
            page_start = 1
        if page_end > self.total_page_count + 1:
            page_end = self.total_page_count + 1
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        first = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(first)
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            pre = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(pre)

        for i in range(page_start, page_end):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(next)

        self.query_dict.setlist(self.page_param, [self.total_page_count])
        last = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(last)

        page_string = mark_safe("".join(page_str_list))
        return page_string
