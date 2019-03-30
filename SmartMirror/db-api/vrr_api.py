from requests import get
from pprint import pprint




def get_station_information(station_name, number_of_connections):
    ''' Function to get the json file from the VRR-API

        Input Params
        station_name - Name of the desired station
        number_of_connections - Number of maximal connections we want to get
                                from the API. This is depends obviously on the
                                station.

        Output Params
        The fucntions outputs a dictionary which contains the following
        keys:
        arrival_time - Arrival time of each connection
        direction - Direction of each connection
        type - Type of the connection i.e. bus or S-Bahn
        line - Name of the connection i.e. S4 or 436
        delay - Realtime delay of the connection, if is delay = -9999
                than the connection is cancelled

    '''

    base_html = "http://efa.vrr.de/standard/XSLT_DM_REQUEST?language=de&type_dm=stop&mode=direct&dmLineSelectionAll=1&depType=STOPEVENTS&includeCompleteStopSeq=0&useRealtime=1&outputFormat=json"

    station_information = get(base_html + '&' + f'limit={number_of_connections}' + '&' + f'name_dm={station_name}').json()
    depature_list = station_information['departureList']

    arrival_time = []
    direction = []
    type = []
    line = []
    delay = []

    for connection in depature_list:
        arrival_time.append(connection['dateTime'])
        direction.append(connection['servingLine']['direction'])
        type.append(connection['servingLine']['name'])
        line.append(connection['servingLine']['symbol'])

        try:
            delay.append(connection['servingLine']['delay'])

        except KeyError:
            delay.append('unknown')

    essential_depature_informations = {'arrival_time': arrival_time,
                                       'direction': direction,
                                       'type': type, 'line': line,
                                       'delay': delay}

    return essential_depature_informations


if __name__ == '__main__':
    pprint(get_station_information('Dortmund Brackel', 10))
