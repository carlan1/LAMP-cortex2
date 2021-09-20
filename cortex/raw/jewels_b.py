""" Module for raw feature jewels_b """
import LAMP
from ..feature_types import raw_feature


@raw_feature(
    name="lamp.jewels_b",
    dependencies=["lamp.jewels_b"]
)
def jewels_b(_limit=10000,
             cache=False,
             recursive=True,
             **kwargs):
    """ Get jewels_b data bounded by time interval.

    Args:
        _limit (int): The maximum number of sensor events to query for in a single request
        cache (bool): Indicates whether to save raw data locally in cache dir
        recursive (bool): if True, continue requesting data until all data is
                returned; else just one request

    Returns:
        timestamp (int): The UTC timestamp for the jewels_a event.
        duration (int): the duration in ms
        activity (str): the activity id
        activity_name (str): 'lamp.jewels_b'
        static_data (dict): a dict which includes 'point', 'score', 'total_attempts',
                'total_bonus_collected', 'total_jewels_collected'
        temporal_slices (list): list of dicts which include the 'duration',
                'item', 'level', 'status', and 'value' for each attempt
    """

    jewels_b_ids = [activity['id'] for activity in
                    LAMP.Activity.all_by_participant(kwargs['id'])['data']
                    if activity['spec'] == 'lamp.jewels_b']

    _jewels_b = [{'timestamp': res['timestamp'],
                  'duration': res['duration'],
                  'activity': res['activity'],
                  'activity_name': 'lamp.jewels_b',
                  'static_data': res['static_data'],
                  'temporal_slices': res['temporal_slices']}
                 for res in LAMP.ActivityEvent.all_by_participant(kwargs['id'],
                                                                  _from=kwargs['start'],
                                                                  to=kwargs['end'],
                                                                  _limit=_limit)['data']
                 if res['activity'] in jewels_b_ids]

    while _jewels_b and recursive:
        to = _jewels_b[-1]['timestamp']
        _jewels_b_next = [{'timestamp': res['timestamp'],
                           'duration': res['duration'],
                           'activity':res['activity'],
                           'activity_name':'lamp.jewels_b',
                           'static_data':res['static_data'],
                           'temporal_slices':res['temporal_slices']}
                          for res in LAMP.ActivityEvent.all_by_participant(kwargs['id'],
                                                                           _from=kwargs['start'],
                                                                           to=to,
                                                                           _limit=_limit)['data']
                          if res['activity'] in jewels_b_ids]

        if not _jewels_b_next or _jewels_b_next[-1]['timestamp'] == to:
            break
        _jewels_b += _jewels_b_next

    return _jewels_b
