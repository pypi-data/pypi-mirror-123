import argparse
import sys
import json
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

from . import cue_finder

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, args):
        self.args=args
    
    def on_modified(self, event):
        #print(f'event type: {event.event_type}  path : {event.src_path}')
        
        # we check if we modified the project file
        # remove last letter because Hindenburg renames the file during saving
        # with a .nhsx~ extension
        if os.path.basename(event.src_path)[:-1] == os.path.basename(self.args['file']):
            clear_console()
            process_data(self.args)

def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def file_exists(x):
        """
        'Type' for argparse - checks that file exists but does not open it.
        https://stackoverflow.com/posts/11541495/revisions
        """
        if not os.path.exists(x):
            # Argparse uses the ArgumentTypeError to give a rejection message like:
            # error: argument input: x does not exist
            raise argparse.ArgumentTypeError("the file file {0} does not exist".format(x))
        return x

def process_data(args):
    # get the data – it will be a dict
    cue_points = cue_finder.get_cue_points_from_file(args['file'])

    # keep the data as json if to_json, else render it to a table
    if len(cue_points) == 0:
        if args['verbose']:
            sys.stderr.write('Warning: no cue points found.\n')

    if args['to_json']:
        output = json.dumps(cue_points, indent=args['json_indent'], ensure_ascii=False, default=str)
    else:
        # we need to explicitly pass the column names as otherwise
        # their order can't be guaranteed
        table_columns = ['timestamp','name']
        if not args['no_track']: table_columns.append('track')
        if not args['no_region']: table_columns.append('region')

        output = cue_finder.pretty_table(cue_points, table_columns)
    
    # output the results
    if args['verbose']:
        sys.stderr.write('Writing results to stdout:\n')
    sys.stdout.write(f'{output}\n')

def main():
    parser = argparse.ArgumentParser(
        description='''Get the locations of cue points on the timeline of a .nhsx 
        (Hindenburg) project file. By default, watch the file for changes
        and keep writing the cue points to console. Alternatively, check once and get 
        a list of the points.'''
    )

    # basic arguments
    mainargs = parser.add_argument_group('main arguments')

    mainargs.add_argument("file", type=file_exists, nargs=1,
                          help="[required] Hindenburg .nhsx file to open", metavar="FILENAME")
    mainargs.add_argument("-d", "--dump",
                          dest="dump", required=False,  action="store_true",
                          help="Dump the list of cuepoints to output once instead of watching for changes forever")
    
    # output arguments
    outputargs = parser.add_argument_group('arguments related to the output')

    outputargs.add_argument("-t", "--no-track",
                            dest="no_track", required=False,  action="store_true",
                            help="Remove track name from table output")
    outputargs.add_argument("-r", "--no-region",
                            dest="no_region", required=False,  action="store_true",
                            help="Remove region name from table output")

    outputargs.add_argument("-v", "--verbose",
                            dest="verbose", required=False,  action="store_true",
                            help="Print diagnostic messages to stderr")
    outputargs.add_argument("-j", "--json",
                            dest="to_json", required=False,  action="store_true",
                            help="Output the results in JSON format instead of a formatted table")
    outputargs.add_argument("--json-indent",
                            dest="json_indent", required=False, type=int,
                            help="If the output is JSON, this many spaces will be used to indent it. If not passed, everything will be on one line")
  
    # get args
    args = vars(parser.parse_args())
    args['file'] = args['file'][0]

    if not args['dump']:
        clear_console()
    
    process_data(args)

    if not args['dump']:
        filedir = os.path.dirname(args['file'])
        if not filedir:
            filedir = '.'

        event_handler = FileChangeHandler(args)
        observer = Observer()
        observer.schedule(event_handler, path=filedir, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == '__main__':
    main()