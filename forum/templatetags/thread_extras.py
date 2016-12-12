import arrow
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def get_total_subject_posts(subject):
    total_posts = 0
    for thread in subject.threads.all():
        total_posts += thread.posts.count()
    return total_posts


@register.simple_tag
def get_total_thread_posts(thread):
    return thread.posts.count()


@register.simple_tag
def get_distinct_thread_voices(thread):
    # thread.posts.distinct('user_id') not supported in sqlite / mysql
    voices = thread.posts.order_by('user_id').values('user_id').distinct().count()
    return voices


@register.filter
def started_time(created_at):
    return arrow.get(created_at).humanize()


@register.simple_tag
def last_posted_user_name(thread):
    if thread.posts.exists():
        return thread.posts.latest('created_at').user.public_name
    else:
        return "Deleted"


@register.simple_tag
def last_post_time(thread):
    if thread.posts.exists():
        latest_post_time = thread.posts.latest('created_at').created_at
        return arrow.get(latest_post_time).humanize()
    else:
        return ""


@register.simple_tag
def user_vote_button(thread, subject, user):
    vote = thread.poll.votes.filter(user_id=user.id).first()

    if not vote:
        if user.is_authenticated():
            link = '<div class="btn-vote"><a href="%s" class="btn btn-info">Vote</a></div>' \
                   % reverse('forum_cast_vote', kwargs={'thread_id': thread.id, 'subject_id': subject.id})
            return link

    return ""


@register.filter
def vote_percentage(subject):
    count = subject.votes.count()
    if count == 0:
        return 0
    total_votes = subject.poll.votes.count()
    return (100 / total_votes) * count
