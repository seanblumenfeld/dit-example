import logging

from django.core.mail import send_mail
from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import UpdateProcessView

from grants.applications.models import ApplicationProcess
from grants.applications.views import ApplicationView

logger = logging.getLogger(__name__)


@frontend.register
class ApplicationFlow(Flow):
    process_class = ApplicationProcess
    process_title = 'ApplicationFlow'
    process_description = 'Process used to apply for a grant.'

    start = flow.Start(ApplicationView).Next(this.legal_approval)

    legal_approval = flow.View(
        UpdateProcessView, fields=['legal_approved']
    ).Next(this.finance_approval)

    finance_approval = flow.View(
        UpdateProcessView, fields=['finance_approved']
    ).Next(this.notify_applicant)

    notify_applicant = flow.Handler(this.send_applicant_notification).Next(this.end)

    end = flow.End()

    def send_applicant_notification(self, activation):
        subject = 'Application rejected.'
        message = 'Sorry but your application has been rejected.'

        approved = all([activation.process.legal_approved, activation.process.finance_approved])

        if approved:
            subject = 'Application approved.'
            message = 'Congratulations, your application has been approved.'

        logger.info(subject, message)
        # TODO: send mail broken at the moment
        # send_mail(
        #     subject, message, 'from@example.com', [activation.process.email], fail_silently=False,
        # )

