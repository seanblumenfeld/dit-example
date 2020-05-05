from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView
from viewflow.flow.views import get_next_task_url, StartFlowMixin

from grants.applications.forms import ApplicationForm


class ApplicationView(StartFlowMixin, SessionWizardView):
    template_name = 'application.html'
    form_list = [ApplicationForm]

    def done(self, form_list, form_dict, **kwargs):
        row = form_dict['0'].save(commit=False)

        for field, value in form_dict['0'].cleaned_data.items():
            setattr(row, field, value)
            setattr(self.request.activation.process, field, value)

        row.save()
        self.request.activation.done()

        return redirect(get_next_task_url(self.request, self.activation.process))
