from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from synchro import call_synchronize, reset_synchro
from synchro.models import options


@staff_member_required
def synchro(request):
    if 'synchro' in request.POST:
        try:
            msg = call_synchronize()
            messages.add_message(request, messages.INFO, msg)
        except Exception as e:
            msg = _('An error occured: %(msg)s (%(type)s)') % {'msg': str(e),
                                                               'type': e.__class__.__name__}
            messages.add_message(request, messages.ERROR, msg)
    elif 'reset' in request.POST:
        reset_synchro()
        msg = _('Synchronization has been reset.')
        messages.add_message(request, messages.INFO, msg)
    return TemplateResponse(request, 'synchro.html', {'last': options.last_check})
