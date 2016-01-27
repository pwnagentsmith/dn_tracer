# from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import datetime
# sys.path.append(settings.PDNS_PATH)

# from .forms import ToDoForm
from lib.database import Database
from lib.utils import check_ip
# import django.contrib.staticfiles


def force_int(value):
    try:
        value = int(value)
    except:
        value = None
    finally:
        return value


def source_parse(value):
    try:
        value = ','.join(value.split())
    except:
        pass
    finally:
        return value


def index(request):

    if request.method == "POST":
        dn_ip = request.POST.get("dn_ip")
        date = datetime.date.today()
        port = force_int(request.POST.get("port"))
        source = request.POST.get("source")
        note = source_parse(request.POST.get("note"))

        db = Database()
        msg = ""

        if dn_ip and source:
            if check_ip(dn_ip):
                if not port and note:
                    msg = db.insert_malicious_ip_record(ip=dn_ip,
                                                        date=date,
                                                        source=source,
                                                        note=note)
                elif port and not note:
                    msg = db.insert_malicious_ip_record(ip=dn_ip,
                                                        date=date,
                                                        source=source,
                                                        port=port)
                else:
                    msg = db.insert_malicious_ip_record(ip=dn_ip,
                                                        date=date,
                                                        source=source)
            else:
                if not port and note:
                    msg = db.insert_malicious_dn_record(dn=dn_ip,
                                                        date=date,
                                                        source=source,
                                                        note=note)
                elif port and not note:
                    msg = db.insert_malicious_dn_record(dn=dn_ip,
                                                        date=date,
                                                        source=source,
                                                        port=port)
                else:
                    msg = db.insert_malicious_dn_record(dn=dn_ip,
                                                        date=date,
                                                        source=source)
        else:
            return render_to_response("add/index.html",
                                      context_instance=RequestContext(request))
    else:
        return render_to_response("add/index.html",
                                  context_instance=RequestContext(request))
    if msg:
        return render_to_response("error.html",
                                  {"error": str(msg)},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response("sucess.html",
                                  {"message": "Add {} to DB sucessfully".format(
                                      dn_ip)},
                                  context_instance=RequestContext(request))
