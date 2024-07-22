from flask import (
    Blueprint, render_template, session, redirect, url_for
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
            "id": "applayout_route_id_saccos",
            "url": url_for("acg.index"),
            "title": _("SACCOs"),
            "icon":"icon-people"
        },
        {
            "id": "applayout_route_id_transactions",
            "url": url_for("acg.index"),
            "title": _("Transactions"),
            "icon":"icon-transactions"
        },
        {
            "id": "applayout_route_id_auditrail",
            "url": url_for("acg.index"),
            "title": _("Audit Trail"),
            "icon":"icon-list"
        },
        {
            "id": "applayout_route_id_users",
            "url": url_for("acg.index"),
            "title": _("Users"),
            "icon":"icon-people"
        },
        {
            "id": "applayout_route_id_acgs",
            "url": url_for("acg.index"),
            "title": _("ACGs"),
            "icon":"icon-control-center"
        },
    ]