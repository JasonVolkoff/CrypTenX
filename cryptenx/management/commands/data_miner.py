from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cryptenx.models import EtheriumData
import requests
from calendar import timegm
from datetime import date, datetime, timedelta
from config.settings import CW_PUBLIC_KEY

# TODO: 
class Command(BaseCommand):
    help = "Gathers crypto data n' stuff."

    def add_arguments(self, parser):
        parser.add_argument('currency', type=str, help='Abbreviated currency code.')
        parser.add_argument('days', type=int, help='Total number of days of data to retrieve')

    def handle(self, *args, **kwargs):
        print("Initializing data mining session...")
        currency = kwargs['currency']
        self.days = kwargs['days']
        self.get_timestamps()
        try:
            params = {
                'after': self.stop_timestamp,
                'before': self.oldest_timestamp,
                'periods': [180],
                'apikey': CW_PUBLIC_KEY
            }
            resp = requests.get(f'https://api.cryptowat.ch/markets/coinbase-pro/{currency}usd/ohlc', params=params)
        
            if resp.ok:
                print("Gathering data from cryptowatch API")
                data = resp.json()
                result = data['result']['180']
                try:
                    for data_point in result:
                        timestamp = data_point[0]
                        datetime_obj_with_tz = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                        EtheriumData.objects.create(
                            close_time = datetime_obj_with_tz,
                            open_price = data_point[1],
                            high_price = data_point[2],
                            low_price = data_point[3],
                            close_price = data_point[4],
                            volume = data_point[5],
                            quote_volume = data_point[6]
                        )
                    print("Done!")
                except:
                    raise CommandError('Failed to save to the database.')
            else:
                print("Somthing went wrong dude...")
        except:
            raise CommandError('Operation Failed')

    def get_timestamps(self):
        print("Converting timestamps to UTC POSIX strings...")
        oldest_entry = EtheriumData.objects.first()
        if oldest_entry:
            # Get the oldest date and convert to UTC POSIX timestamp string.
            # We want to begin collection 3 minutes prior to the oldest entry.
            oldest_date = oldest_entry.close_time - timedelta(minutes=3)
            self.oldest_timestamp = oldest_entry.convert_to_unix()
        else:
            # A database does not exist yet, so we assume to start collecting
            # data from today's datetime.
            oldest_date = datetime.utcnow()
            self.oldest_timestamp = str(timegm(oldest_date.timetuple()))

        stop_date = oldest_date - timedelta(days=self.days)
        self.stop_timestamp = str(timegm(stop_date.timetuple()))
        print(f"Gathering data from {stop_date} to {oldest_date}")