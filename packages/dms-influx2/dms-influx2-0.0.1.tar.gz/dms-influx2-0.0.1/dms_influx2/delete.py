import itertools
from datetime import datetime

from influxdb_client import DeleteApi


class Delete(DeleteApi):
    def __init__(self, client):
        self.org = client.org
        super().__init__(client)

    def delete_data(self, bucket, measurements=None, device_ids=None, descriptions=None, org=None,
                    time_range=None, time_from=None, time_to=None) -> list:

        #TODO add time_range

        if org is None:
            org = self.org

        start = "1900-01-01T00:00:00Z"
        stop = datetime.utcnow().isoformat() + 'Z'
        if time_from is not None:
            start = time_from.isoformat() + 'Z'
        if time_to is not None:
            start = time_to.isoformat() + 'Z'

        predicates = []

        if measurements is not None:
            _predicates = []
            for measurement in measurements:
                _predicates.append(f'_measurement="{measurement}"')
            predicates.append(_predicates)

        if device_ids is not None:
            _predicates = []
            for device_id in device_ids:
                _predicates.append(f'device_id="{device_id}"')
            predicates.append(_predicates)

        if descriptions is not None:
            _predicates = []
            for description in descriptions:
                _predicates.append(f'description="{description}"')
            predicates.append(_predicates)

        # Filter empty lists and find all combinations for predicates, execute all queries
        predicates = list(filter(None, predicates))
        predicates = [predicate for predicate in itertools.product(*predicates)]
        predicates = [" and ".join(i for i in predicate) for predicate in predicates]
        for predicate in predicates:
            self.delete(start=start, stop=stop, predicate=predicate, bucket=bucket, org=org)
        return predicates





