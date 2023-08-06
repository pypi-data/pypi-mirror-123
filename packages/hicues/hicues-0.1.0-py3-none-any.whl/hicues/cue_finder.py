import xmltodict
import sys
from datetime import datetime, date, timedelta

def today_date_as_list():
    return [int(x) for x in date.today().isoformat().split('-')]

def text_to_hhmmssms(text):
    dot_split = text.split('.')
    if len(dot_split) == 2:
        hhmmss = [int(x) for x in dot_split[0].split(':')]
        # pad if hour andor minute was missing
        hhmmss = [0] * (3 - len(hhmmss)) + hhmmss

        hhmmss.append(int(dot_split[1])*1000)
    else:
        hhmmss = [int(x) for x in dot_split[0].split(':')]
        # pad if hour andor minute was missing
        hhmmss = [0] * (3 - len(hhmmss)) + hhmmss + [0]
    
    return hhmmss
    
def text_to_datetime(text):
    return datetime(*(today_date_as_list() + text_to_hhmmssms(text)))

def as_list(thing):
    '''This is used for XML parsing where a one-item list is not 
    returned as a list but a single item'''
    if not isinstance(thing, list):
        return [thing]
    else:
        return thing

def pretty_table(my_dict, col_list=None):
    """ Prettify  a list of dictionaries (my_dict) as a dynamically sized table.
    If column names (col_list) aren't specified, they will show in random order.
    Original Author: "Thierry Husson - Use it as you want but don't blame me."
    https://stackoverflow.com/a/40389411
    """
    if not col_list: col_list = list(my_dict[0].keys() if my_dict else [])
    my_list = [col_list] # 1st row = header
    for item in my_dict: my_list.append([str(item[col] if item[col] is not None else '') for col in col_list])
    col_size = [max(map(len,col)) for col in zip(*my_list)]
    format_str = ' | '.join(["{{:<{}}}".format(i) for i in col_size])
    my_list.insert(1, ['-' * i for i in col_size]) # Seperating line
    return '\n'.join([format_str.format(*item) for item in my_list])

def get_cue_points_from_file(filename):
    with open(filename) as file:
        xmltext = file.read()
        project_data = xmltodict.parse(xmltext)
    
    cuepoints = {}
    
    for file in as_list(project_data['Session']['AudioPool'].get('File',[])):
        # if the file had CuePoints previously but they were removed, it will exist
        # in the tree but have a None value, hence the or operator here.
        cuepoints_list = as_list((file.get('File.CuePoints',{}) or {}).get('CuePoint',[]))
        if len(cuepoints_list) > 0:
            cuepoints_processed = []
            for cp in cuepoints_list:
                name = cp.get('@Name', '')
                time = cp['@Time']
                if len(time.split('.')[0]) == 5: # cp at less than an hour
                    time = '0:' + time
                time = text_to_datetime(time)

                cuepoints_processed.append((time, name))

            cuepoints[file['@Id']] = sorted(cuepoints_processed, key=lambda i: i[0])
    
    regions = []
    matched_cuepoints = []
    for track in project_data['Session']['Tracks']['Track']:
        for region in as_list(track.get('Region',[])):
            r = {}

            h, m, s, ms = text_to_hhmmssms(region['@Length'])
            r['length'] = timedelta(hours=h, minutes=m, seconds=s, microseconds=ms)

            h, m, s, ms = text_to_hhmmssms(region.get('@Offset', '00:00'))
            r['offset'] = timedelta(hours=h, minutes=m, seconds=s, microseconds=ms)

            r['start_in_file'] = text_to_datetime(region.get('@Offset', '00:00'))

            r['start'] = text_to_datetime(region.get('@Start', '00:00'))
            r['end_in_file'] = r['start_in_file'] + r['length']

            r['name'] = region['@Name']
            r['track'] = track['@Name']
            r['file_id'] = region['@Ref']

            # note: we do not actually use regions for anything after this point,
            # but this is stored for future development
            regions.append(r)        

            for cp in cuepoints.get(r['file_id'],[]):
                if r['start_in_file'] < cp[0] < r['end_in_file']:
                    matched_cuepoints.append({
                        'timestamp': (cp[0]-r['offset']+(r['start'] - datetime.combine(datetime.today(), datetime.min.time()))).time(),
                        'name': cp[1],
                        'track': r['track'],
                        'region': r['name']
                    })

    return sorted(matched_cuepoints, key= lambda x: x['timestamp'])