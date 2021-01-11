from pathlib import Path
from src import log_to_file
import os
import pytest

@pytest.fixture(scope='session')
def return_temp_dir_path(tmpdir_factory):
    temp_dir_path = tmpdir_factory.mktemp('tmp')
    assert os.path.exists(temp_dir_path) == True 
    #print(f'temp dir string: {str(temp_dir_path)}')
    return str(temp_dir_path)

@pytest.fixture(scope='session')
def return_non_pre_existing_filepath(return_temp_dir_path):
    not_exist_filename = 'this_file_not_exist'
    str_temp_path = os.path.join(return_temp_dir_path, not_exist_filename) 
    #print(f'non exist file path {str_temp_path }')
    return str_temp_path
     

@pytest.fixture(scope='session')
def return_existing_empty_filepath(tmpdir_factory):
    exist_empty_filename = 'this_empty_file_exist'
    temp_path = tmpdir_factory.mktemp('tmp').join(exist_empty_filename) 
    assert os.path.exists(temp_path) == False 
    #print(temp_path)
    return temp_path 

@pytest.fixture(scope='session')
def return_existing_non_empty_filepath(tmpdir_factory):
    exist_non_empty_filename = 'this_non_empty_file_exist'
    temp_path = tmpdir_factory.mktemp('tmp').join(exist_non_empty_filename) 
    # should not exist b4 we create it
    assert os.path.exists(temp_path) == False 
    # create this file
    file_content = []
    with open(temp_path, 'w+') as f:
        for i in range(0, 10):
            f.write(f'{i} these content exists before the day of time')


    return temp_path 



def test_log_to_non_pre_existing_file(return_non_pre_existing_filepath):
    #print(temp_path) 
    '''
    temp_path =  return_non_pre_existing_filepath()
    print(temp_path)
    assert temp_path != None 
    '''

    string_to_be_written = 'this file only contains this!'
    log_to_file(return_non_pre_existing_filepath, string_to_be_written) 
    # test if file is created
    assert os.path.exists(return_non_pre_existing_filepath) == True 
    # test if file content is not empty and its content should  matches what we write
    file_content = []
    with open(return_non_pre_existing_filepath) as f:
        for line in f:
            file_content.append(line)
    assert len(file_content)  == 1
    assert ''.join(file_content) == string_to_be_written 

def test_log_to_existing_empty_file(return_existing_empty_filepath):
    #temp_path = return_existing_empty_filepath

    # create this empty file
    with open(return_existing_empty_filepath, 'w'):
        pass
    # test if file is created
    assert os.path.exists(return_existing_empty_filepath) == True 

    #print(temp_path) 
    string_to_be_written = 'this file only contains this!'
    log_to_file(return_existing_empty_filepath, string_to_be_written) 
    # test if file content is not empty and its content should  matches what we write
    file_content = []
    with open(return_existing_empty_filepath) as f:
        for line in f:
            file_content.append(line)
    assert len(file_content)  == 1
    assert ''.join(file_content) == string_to_be_written 


def test_log_to_existing_non_empty_file(return_existing_non_empty_filepath):
    # fixture cannot be call directly
    #temp_path = return_existing_non_empty_filepath
        # test if file is created
    #assert os.path.exists(return_existing_non_empty_filepath) == True 
    # test file content is not empty
    file_content = []
    with open(return_existing_non_empty_filepath, 'r') as f:
        for line in f:
            file_content.append(list) 
    assert len(file_content) > 0
    #print(temp_path) 
    string_to_be_written = 'this file only contains this!'
    log_to_file(return_existing_non_empty_filepath, string_to_be_written) 
    # test if file content is not empty and its content should  matches what we write
    file_content = []
    with open(return_existing_non_empty_filepath) as f:
        pass


