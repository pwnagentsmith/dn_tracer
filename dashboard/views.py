from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.shortcuts import render
from lib.database import Database


# Create your views here.
def index(request):
    db = Database()
    report = dict(
        total_dn=db.count_dn(),
        total_alive_dn=db.count_alive_dn(),
        last_dn=db.last_added_dn(),
        top_mapping_ip=db.top_mapping_ip(),
        top10_country_amount=db.top10_country_amount()
    )
    return render_to_response("dashboard/index.html",
                              {"report": report},
                              context_instance=RequestContext(request))
