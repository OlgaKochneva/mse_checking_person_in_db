import sys
import pytest
from json import load

sys.path.append('../')

from checking_person_in_db.app import *

with open('test_suit.json', 'r') as f:
    test_suit = load(f)


@pytest.mark.parametrize('command_line_argument', test_suit['badFileFormatTest'])
def test_inadmissibility_inappropriate_file_format(command_line_argument):
    with pytest.raises(SystemExit):
        App(command_line_argument).run()


@pytest.mark.parametrize('command_line_argument', test_suit['videoExistenceTest'])
def test_video_stream_existance(command_line_argument):
    with pytest.raises(SystemExit):
        App(command_line_argument).run()