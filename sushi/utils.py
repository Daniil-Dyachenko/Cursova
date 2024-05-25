from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery,SearchRank,SearchHeadline
from sushi.models import Products

def q_search(query):

    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    search = Products.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")

    search = search.annotate(headline=SearchHeadline("name",query,start_sel='<span style ="background-color: green;">',stop_sel="</span>"))
    search = search.annotate(bodyline=SearchHeadline("description", query, start_sel='<span style ="background-color: green;">',stop_sel="</span>"))

    return search
