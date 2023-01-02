from datetime import datetime
import dateparser

""" Fetch Incidents Inputs """

# GLOBALS
utc_time_twelve = dateparser.parse('2022/01/01 12:00', settings={'TIMEZONE': 'UTC'})
utc_time_eleven = dateparser.parse('2022/01/01 11:00', settings={'TIMEZONE': 'UTC'})


""" TestFetchIncidentsHelperFunctions UT's """


def assert_datetime_objects(returned: datetime | None, expected: datetime | None):
    if not returned or not expected:
        return False
    return all(
        [(returned.year == expected.year),
            (returned.month == expected.month),
            (returned.day == expected.day),
            (returned.hour == expected.hour),
            (returned.minute == expected.minute)])


# test_add_time_filter_to_query_parameter arguments
case_query_without_time_filter = (
    '(query without time filter)', utc_time_twelve,
    "(query without time filter) and (time_generated geq '2022/01/01 12:00:00')")
test_add_time_filter_to_query_parameter_args = [case_query_without_time_filter]


# test_add_unique_id_filter_to_query_parameter arguments
case_log_type_query_with_previous_largest_id = ('(query)', '111111', "(query) and (seqno geq '111112')")
case_log_type_query_without_previous_largest_id = ('(query)', '', '(query)')
test_add_unique_id_filter_to_query_parameter_args = [
    case_log_type_query_with_previous_largest_id, case_log_type_query_without_previous_largest_id]


# test_log_types_queries_to_dict arguments
case_empty_log_type = ({}, {})
case_all_log_type_queries_selected = (
    {'log_types': ['All'],
     'traffic_query': 'traffic query', 'threat_query': 'threat query', 'url_query': 'url query',
     'data_query': 'data query', 'correlation_query': 'correlation query', 'system_query': 'system query',
     'wildfire_query': 'wildfire query', 'decryption_query': 'decryption query'},
    {'Traffic': 'traffic query', 'Threat': 'threat query', 'Url': 'url query', 'Data': 'data query',
     'Correlation': 'correlation query', 'System': 'system query', 'Wildfire': 'wildfire query',
     'Decryption': 'decryption query'})
case_one_valid_log_type_query_selected = (
    {'log_types': ['All'], 'traffic_query': 'traffic query'}, {'Traffic': 'traffic query'})
case_one_invalid_log_type_query_selected = (
    {'log_types': ['Traffic'], 'traffic_query': ''}, {})
case_one_valid_log_type_query_one_invalid_log_type_query_selected = (
    {'log_types': ['Traffic', 'URL'], 'traffic_query': 'traffic query',
     'url_query': ''},
    {'Traffic': 'traffic query'}
)

test_parse_queries_args = [case_empty_log_type, case_all_log_type_queries_selected,
                           case_one_valid_log_type_query_selected,
                           case_one_invalid_log_type_query_selected,
                           case_one_valid_log_type_query_one_invalid_log_type_query_selected]

# test_get_fetch_start_datetime_dict arguments
first_fetch = '24 hours'
{'X_log_type': '2022-1-1T12:00:00', 'Y_log_type': '2022-1-1T12:00:00'}
{'X_log_type': '(X_log_type query)', 'Y_log_type': '(Y_log_type query)'}

case_first_fetch = (
    {},
    first_fetch,
    {'X_log_type': '(X_log_type query)', 'Y_log_type': '(Y_log_type query)'},
    {'X_log_type': dateparser.parse(first_fetch, settings={'TIMEZONE': 'UTC'}),
     'Y_log_type': dateparser.parse(first_fetch, settings={'TIMEZONE': 'UTC'})})

case_one_incident_type_previously_fetched_fetch = (
    {'X_log_type': '2022-1-1T11:00:00'},
    first_fetch, {'X_log_type': '(X_log_type query)', 'Y_log_type': '(Y_log_type query)'},
    {'X_log_type': dateparser.parse('2022-1-1T11:00:00', settings={'TIMEZONE': 'UTC'}),
     'Y_log_type': dateparser.parse(first_fetch, settings={'TIMEZONE': 'UTC'})})

case_two_incidents_types_previously_fetched_fetch = (
    {'X_log_type': '2022-1-1T11:00:00', 'Y_log_type': '2022-1-1T13:00:00'},
    first_fetch, {'X_log_type': '(X_log_type query)', 'Y_log_type': '(Y_log_type query)'},
    {'X_log_type': dateparser.parse('2022-1-1T11:00:00', settings={'TIMEZONE': 'UTC'}),
     'Y_log_type': dateparser.parse('2022-1-1T13:00:00', settings={'TIMEZONE': 'UTC'})})

test_get_fetch_start_datetime_dict_args = [case_first_fetch,
                                           case_one_incident_type_previously_fetched_fetch,
                                           case_two_incidents_types_previously_fetched_fetch]


# test_parse_incident_entries arguments
case_no_incidents = ({}, (None, None, {}))

one_incident = [{'seqno': '00000000001', 'type': 'X_log_type', 'time_generated': '2022/01/01 12:00:00'}]
one_incident_result = (
    '00000000001', utc_time_twelve,
    [{'name': '00000000001', 'occurred': utc_time_twelve.isoformat() + 'Z',
      'rawJSON': '{"seqno": "00000000001", "type": "X_log_type", "time_generated": "2022/01/01 12:00:00"}',
      'type': 'X_log_type'}])
case_one_incident = (one_incident, one_incident_result)

two_incidents = [
    {'seqno': '00000000001', 'type': 'X_log_type', 'time_generated': '2022/01/01 11:00:00'},
    {'seqno': '00000000002', 'type': 'X_log_type', 'time_generated': '2022/01/01 12:00:00'}
]
two_incidents_result = (
    '00000000002',
    utc_time_twelve,
    [{'name': '00000000001', 'occurred': utc_time_eleven.isoformat() + 'Z',
      'rawJSON': '{"seqno": "00000000001", "type": "X_log_type", "time_generated": "2022/01/01 11:00:00"}',
      'type': 'X_log_type'},
     {'name': '00000000002', 'occurred': utc_time_twelve.isoformat() + 'Z',
        'rawJSON': '{"seqno": "00000000002", "type": "X_log_type", "time_generated": "2022/01/01 12:00:00"}',
      'type': 'X_log_type'}])
case_two_incident = (two_incidents, two_incidents_result)

test_parse_incident_entries_args = [case_no_incidents, case_one_incident, case_two_incident]


# test_get_parsed_incident_entries arguments
case_no_incidents = ({}, {}, {}, {})
case_valid_input = (
    {'X_log_type': {'seqno': '0000002'}},
    {},
    {},
    {
        'X_log_type':
        [{'name': '00000000001', 'occurred': '2022-01-01T12:00:00Z',
          'rawJSON': '{"seqno": "00000000001", "type": "X_log_type", "time_generated": "2022/01/01 12:00:00"}',
          'type': 'X_log_type'}]})

get_parsed_incident_entries_args = [case_no_incidents, case_valid_input]