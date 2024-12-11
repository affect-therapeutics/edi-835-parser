import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

import edi_835_parser  # noqa: E402

current_path = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def blue_cross_nc_sample():
	path = current_path + '/test_edi_835_files/blue_cross_nc_sample.txt'
	return edi_835_parser.parse(path)


@pytest.fixture
def emedny_sample():
	path = current_path + '/test_edi_835_files/emedny_sample.txt'
	return edi_835_parser.parse(path)


@pytest.fixture
def sample_835():
	path = current_path + '/test_edi_835_files/sample_835.txt'
	return edi_835_parser.parse(path)


@pytest.fixture
def sample_835_with_func():
	def modify_file_content(modify_func=None):
		path = current_path + '/test_edi_835_files/sample_835.txt'
		base_content = open(path, 'r').read()
		if modify_func:
			content = modify_func(base_content)
		else:
			content = base_content

		return edi_835_parser.parse_edi_string(content)

	return modify_file_content


@pytest.fixture
def sample_935_with_interests():
	path = current_path + '/test_edi_835_files/sample_835_with_interests.txt'
	return edi_835_parser.parse(path)


@pytest.fixture
def nevada_medicaid_sample():
	path = current_path + '/test_edi_835_files/nevada_medicaid.txt'
	return edi_835_parser.parse(path)


@pytest.fixture
def exhaustive_sample_path():
	return current_path + '/test_edi_835_files/exhaustive_sample.txt'


@pytest.fixture
def exhaustive_sample():
	path = current_path + '/test_edi_835_files/exhaustive_sample.txt'
	return edi_835_parser.parse(path)
