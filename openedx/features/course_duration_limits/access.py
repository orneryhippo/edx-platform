# -*- coding: utf-8 -*-
"""
Contains code related to computing content gating course duration limits
and course access based on these limits.
"""
from datetime import date, datetime, timedelta

from django.apps import apps
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import ugettext as _


from lms.djangoapps.courseware.access_response import AccessError
from lms.djangoapps.courseware.access_utils import ACCESS_GRANTED

COURSE_DURATION_CACHE_TIMEOUT = 3600


class AuditExpiredError(AccessError):
    """
    Access denied because the user's audit timespan has expired
    """
    def __init__(self, user, course, expiration_date):
        error_code = "audit_expired"
        developer_message = "User {} had access to {} until {}".format(user, course, expiration_date)
        # TODO: Translate the expiration_date
        user_message = _("Course access expired on ") + expiration_date.strftime("%B %d, %Y")
        super(AuditExpiredError, self).__init__(error_code, developer_message, user_message)


def get_user_course_expiration_date(user, course):
    """
    Return course expiration date for given user course pair.
    Return None if the course does not expire.
    """
    # TODO: Update business logic based on REV-531
    CourseEnrollment = apps.get_model('student.CourseEnrollment')
    enrollment = CourseEnrollment.get_enrollment(user, course.id)
    if enrollment is None or enrollment.mode == 'verified':
        return None

    try:
        start_date = enrollment.schedule.start
    except CourseEnrollment.schedule.RelatedObjectDoesNotExist:
        start_date = max(enrollment.created, course.start)

    pacing = getattr(course, pacing, None)
    course_end = getattr(course, 'end', None)
    if isinstance(course_end, date):
        # CourseOverview uses datetime while CourseDescriptor uses date, so we convert to match
        course_end = datetime(course_end.year, course_end.month, course_end.day)

    if pacing == 'instructor':
        
        pass
    # do self things

    # access_duration = timedelta(weeks=8)
    # if hasattr(course, 'pacing') and course.pacing == 'instructor':
    #     if course.end and course.start:
    #         access_duration = course.end - course.start

    # expiration_date = start_date + access_duration
    # return expiration_date

    expected_duration_data = {'weeks_to_complete': 6}
    # Replace with API call and cache
    expected_duration = expected_duration_data['weeks_to_complete']




def check_course_expired(user, course):
    """
    Check if the course expired for the user.
    """
    expiration_date = get_user_course_expiration_date(user, course)
    if expiration_date and timezone.now() > expiration_date:
        return AuditExpiredError(user, course, expiration_date)

    return ACCESS_GRANTED
