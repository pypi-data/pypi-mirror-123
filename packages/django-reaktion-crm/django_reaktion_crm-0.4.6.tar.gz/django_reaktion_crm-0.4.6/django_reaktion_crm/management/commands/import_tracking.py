import pytz
import os

from .error_report import create_error_reports

from icecream import ic
from pymongo import MongoClient  # type: ignore
from datetime import datetime, timedelta
from urllib.parse import urlparse

from urllib.parse import urlparse
from urllib.parse import parse_qs

from django.core.management.base import BaseCommand

from django_reaktion_crm.models import Visits
from django_reaktion_crm.models import Clients
from django_reaktion_crm.models import NewsletterLink, Newsletter

debug = False

conn = os.environ['MONGO_CONN']
client = MongoClient(conn)

my_db_tracking = client['tracking-prod']
tz = pytz.timezone('Europe/Stockholm')


def find_campaign_by_url(url, url_timestamp, uid):
    """
    Attach campaign id to user based on url (m2m relation)
    URLs must be added to Newsletter model by admin
    :param url:
    :return Newsletter object
    """

    user = Clients.objects.filter(uid=uid).get()
    campaigns = Newsletter.objects.all()

    utc = pytz.UTC

    if user:

        if 'uid' not in url:
            #ic("no UID in url")
            return

        """
        Loop over campaings and check url date
        """
        for campaign in campaigns:
            campaign_end = campaign.created_at.replace(
                tzinfo=tz) + timedelta(days=6)

            """
            ic(url)
            ic(campaign.name)
            ic(campaign.created_at.replace(tzinfo=tz))
            ic(url_timestamp.replace(tzinfo=tz))
            ic(campaign_end.replace(tzinfo=tz))
            """

            if campaign.created_at.replace(tzinfo=tz) <= url_timestamp.replace(tzinfo=tz) <= campaign_end.replace(tzinfo=tz):

                ic("add campaign {}".format(campaign.id))
                """
                Check if link is campign's urls                
                """
                newsletter_urls = NewsletterLink.objects.filter(
                    newsletter_id=campaign.pk).all()

                for link in newsletter_urls:
                    if link.link in url:
                        user.campaigns.add(campaign)

            else:
                ic("does not match", campaign_end)
    else:
        ic("no user founded")


def agg_last_visits(uid, days, domain_id):
    """
    Count visit <days> ago
    It excludes documents from '.adressgruppen.se' domain
    """
    now = datetime.now(tz=tz)
    start = now - timedelta(days)

    count = my_db_tracking['trackings'].aggregate([
        {
            '$match': {
                'uid': uid,
                'url': {'$not': {'$regex': 'adressgruppen.se'}},
                'domain_id': domain_id,
                'createdAt': {
                    '$gte': start
                }
            }
        }, {
            '$count': 'domain_id'
        }
    ])
    if count:
        for i in count:
            return i['domain_id']

    return 0


def find_param_value(url, param_name):
    parsed_url = urlparse(url)
    captured_value = parse_qs(parsed_url.query)[param_name][0]
    return captured_value


def agg_last_7_days_visits(uid, domain_id):
    return agg_last_visits(uid, 7, domain_id=domain_id)


def agg_last_30_days_visits(uid, domain_id):
    return agg_last_visits(uid, 30, domain_id=domain_id)


def agg_all_visits(uid, domain_id):
    return Visits.objects.filter(uid=uid).count()


def last_user_visit(uid):
    """
    TODO
    :param uid:
    :return:
    """
    pass


def agg_user_visits_by_day(uid, day):
    """
    TODO
    :param uid:
    :param day:
    :return:
    """
    pass


class Command(BaseCommand):
    help = 'Import latest activity from tracking database'

    def add_arguments(self, parser):
        parser.add_argument('delta', nargs='+', type=str)

    def handle(self, *args, **options):

        collection_impressions_agg = my_db_tracking['trackings']

        missing_clients = []
        wrong_base_64 = []
        unregistered = []
        unregistered_unique = []

        """
        Set up date
        """
        now = datetime.utcnow()
        if options['delta']:
            hours = int(options['delta'][1])
        else:
            hours = 4

        start_date = now - timedelta(hours=hours)
        domain_id = int(os.environ['DOMAIN_ID'])

        now = pytz.utc.localize(now)
        start_date = pytz.utc.localize(start_date)
        """
        delete for period
        """
        Visits.objects.filter(created_at__range=[start_date, now]).delete()

        """
        Take all trakcings
        """
        # ic(start_date)
        # ic(now)
        # ic(domain_id)

        cursor_agg_impressions = collection_impressions_agg.find(
            {'domain_id': domain_id,

                'createdAt': {
                    '$gte': start_date,
                    '$lt': now
                }})

        for post in cursor_agg_impressions:

            """
            Exclude payload without UID
            """
            if post['uid'] is None:
                continue

            """
            Exclude direct redirects from EDR
            """
            if '/redirect?' in post['url']:
                continue

            uid = post['uid']

            aware_date = pytz.utc.localize(post['createdAt'])

            if Clients.objects.filter(uid=uid).count():

                if len(post['url']) > 255:
                    post['url'] = post['url'][:255]

                """
                Don't add urls from adressgruppen.se domain
                They can be only unregister or redirects
                """

                if not 'adressgruppen.se' in post['url']:
                    ic(post['url'])
                    """
                    Add to visits table
                    """ 
                    visits = Visits(
                        uid=uid, url=post['url'], created_at=aware_date)
                    visits.save()

            else:
                continue

            """
            Find campaign name (webpower) in url.
            """
            if "&rtm=" in post['url']:
                campaign_name = find_param_value(post['url'], 'rtm')
                obj, created = Newsletter.objects.get_or_create(
                    name=campaign_name,
                    defaults={'created_at': datetime.now()},
                )

                if obj:
                    """
                    Add customer to newsletter/campaign
                    """
                    my_client = Clients.objects.filter(uid=uid).get()
                    my_client.campaigns.add(obj)

            """
            Unregister in new EDRs
            """
            if "/unregister?" in post['url']:
                """
                TODO: May be url['tags'] should be checked
                """
                unregistered.append(post)
                unregistered_unique.append(post['uid'])
                try:
                    person = Clients.objects.filter(uid=uid).get()
                    person.active = False
                    person.save()
                except Clients.DoesNotExist:
                    print("Missing uid")

            """
            PHP EDRs
            TODO: Probaly not necessary. Test it. 
            """
            if "avprenumerera/?ok" in post['url']:
                unregistered.append(post)
                unregistered_unique.append(post['uid'])
                try:
                    person = Clients.objects.filter(uid=uid).get()
                    person.active = False
                    person.save()
                except Clients.DoesNotExist:
                    print("Missing uid")

            try:
                """
                find -7 and -30 days visits                
                """
                last_7_days = agg_last_7_days_visits(uid, domain_id=domain_id)
                last_30_days = agg_last_30_days_visits(
                    uid, domain_id=domain_id)
                all_visits = agg_all_visits(uid, domain_id=domain_id)

                """
                Update user data
                """
                find_client_by_uid = Clients.objects.filter(uid=uid).get()
                find_client_by_uid.all_visits = all_visits
                find_client_by_uid.last_visit = aware_date
                find_client_by_uid.last_7_days_visits = last_7_days
                find_client_by_uid.last_30_days_visits = last_30_days
                find_client_by_uid.save()

            except Clients.DoesNotExist:
                missing_clients.append(uid)
                continue
            except Clients.MultipleObjectsReturned:
                print(f"Duplicated clients {post['uid']}")
                wrong_base_64.append(uid)
                exit(0)
            except Clients.DataError:
                pass

        if debug is True:
            create_error_reports(domain_id, unregistered, unregistered_unique)

        ic("Import finished.")
