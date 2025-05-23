from flask import(
    Blueprint,render_template,session,redirect,url_for
)
from ...repositories.MessagesRepo import getMessages
import json
from flask_babel import _

applayout_bp = Blueprint('applayout', __name__)

@applayout_bp.route('/applayout')
def applayout():
    if 'username' not in session:
        return redirect('/')
    routes = getRoutes()
    return render_template(
        'applayout.html', 
        routes=routes,
        routesJsonList=json.dumps(routes),
        messages=getMessages(app=applayout_bp))

def getRoutes():
    return [
         {
             "id": "applayout_route_id_members",
            "url": url_for("members.index"),
            "title": _("Members"),
            "icon":"icon-people"
         },
         {
             "id":"applayout_route_id_transactions",
             "url":url_for("transactions.index"),
             "title":_("Transactions"),
             "icon":"icon-transactions"
         },
         {
             "id":"applayout_route_id_my_account",
             "url":url_for("members.index"),
             "title":_("My Account"),
             "icon":"icon-man"
         },
         {
           "id": "applayout_route_id_auditrail",
            "url": url_for("audittrail.index"),
            "title": _("Audit Trail"),
            "icon":"icon-list"
         }


    ]