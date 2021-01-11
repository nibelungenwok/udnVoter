from pathlib import Path
import os

def log_to_file(filename, string_to_log):
    # assume this filename is in current directory?
    if os.path.exists(Path.resolve(Path(filename))):
        print(Path(filename))
        print(f'file name : {filename} exist')
        fileobject = None
        if os.path.isfile(filename):
            # if file exists
            # append content to file
            try:
                with open(filename, 'a') as f:
                    f.write(string_to_log + '\n')
            except Exception as e:
                print('{e} happened')
        else:
            print('{filename} exists but not a file') 
            # path not a file
    else:
        print(f'file name : {filename} does not exist')
        # if file not exist
        # create it 
        # write content to it
        try:
            with open(filename, 'w') as f:
                f.write(string_to_log + '\n')
        except Exception as e:
            print('{e} happened')


if __name__ == "__main__":
    assert False == log_to_file('a_file_not_exist', 'what')
    assert False == log_to_file('empty_file', 'what')
