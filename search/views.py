# from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
# sys.path.append(settings.PDNS_PATH)

from .forms import ToDoForm
from lib.database import Database
from lib.utils import check_ip
# import django.contrib.staticfiles


def index(request):

    db = Database()
    query_result = []
    if request.method == "POST":
        query = request.POST.get("query").strip()
        start_date = request.POST.get("Start_Date")
        end_date = request.POST.get("End_Date")
        if not start_date:
            start_date = '2016-01-01'
        if not end_date:
            end_date = datetime.date.today()
        if query:
            if check_ip(query):
                query_result = db.get_pdns_record(ip=query,
                                                  start=start_date,
                                                  end=end_date)
                record = db.get_malicious_ip_record(query)
                dn_ip = "ip"
            else:
                query_result = db.get_pdns_record(dn=query,
                                                  start=start_date,
                                                  end=end_date)
                record = db.get_malicious_dn_record(query)
                dn_ip = "domain"
            return render_to_response("search/result.html",
                                      {"results": query_result,
                                       "record": record,
                                       "type": dn_ip},
                                      context_instance=RequestContext(request))
        else:
            form = ToDoForm(request.POST)
            return render_to_response("search/index.html",
                                      {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = ToDoForm()
        return render_to_response("search/index.html",
                                  {'form': form},
                                  context_instance=RequestContext(request))
