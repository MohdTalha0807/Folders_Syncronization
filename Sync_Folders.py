
# This program synchronizes (one-way) two folders: source and replica 
# The MD5hash has been used to perform integrity check between the source and replica folders

# Further improvements that could be implemented:

# hashing can be stored in the database
# standardize the command line argument
# exception handling

import os
import sys
import shutil
import hashlib
import time

n = len(sys.argv)    # number of inputs from the command line

if n != 5:              
    exit(1)

source_path = sys.argv[1]        
target_path = sys.argv[2]
sleep_time = sys.argv[3]
log_file = sys.argv[4]

hash_history = {}        # dictionary storing the MD5hash of the files 

while True:

    dir_list = set()       #   existing directories in the source
    file_list = set()      #   existing files in the source

    for cwd, dirs, files in os.walk(source_path):         
        
        for f in files:
            rel_path = os.path.relpath(os.path.join(cwd, f), source_path)      
            abs_path = os.path.join(cwd, f)

            md5Hashed = ''
      
            file_list.add(rel_path)

            with open(os.path.join(cwd, f), 'rb', buffering=0) as f_hash:
                md5Hashed = hashlib.file_digest(f_hash, 'sha256').hexdigest()
            
            # create and store the hash of the files in a dictionary
            
            if abs_path not in hash_history:              #  checking if the file exist in the hash history
                hash_history[abs_path] = md5Hashed
                dir_path = os.path.relpath(cwd, source_path)
                shutil.copy2(os.path.join(cwd, f), os.path.join(target_path, os.path.join(dir_path, f)))
                with open(log_file, 'a') as log_file_f:
                    log_file_f.write(f'{time.ctime()}: Copied {os.path.join(cwd, f)} to {os.path.join(target_path, os.path.join(dir_path, f))}\n')
                    print(f'{time.ctime()}: Copied {os.path.join(cwd, f)} to {os.path.join(target_path, os.path.join(dir_path, f))}\n')
            else:
                if hash_history[abs_path] != md5Hashed:    # if the file already exist then comparing the hash history
                    shutil.copy2(os.path.join(cwd, f), os.path.join(target_path, f))
                    with open(log_file, 'a') as log_file_f:
                        log_file_f.write(f'{time.ctime()}: Copied {os.path.join(cwd, f)} to {os.path.join(target_path, os.path.join(target_path, f))}\n')
                        print(f'{time.ctime()}: Copied {os.path.join(cwd, f)} to {os.path.join(target_path, os.path.join(target_path, f))}\n')

        for dir in dirs:                   # if the directory doesn´t exist then create the directory
            dir_path = os.path.relpath(cwd, source_path)
            if dir_path == '.':
                dir_list.add(dir)
            else:
                dir_list.add(os.path.join(dir_path, dir))
            if not os.path.exists(os.path.join(os.path.join(target_path, dir_path), dir)):
                os.makedirs(os.path.join(os.path.join(target_path, dir_path), dir))
                with open(log_file, 'a') as log_file_f:
                    log_file_f.write(f'{time.ctime()}: Created a directory in path {os.path.join(os.path.join(target_path, dir_path), dir)}\n')
                    print(f'{time.ctime()}: Created a directory in path {os.path.join(os.path.join(target_path, dir_path), dir)}\n')

    for cwd, dirs, files in os.walk(target_path):

        for f in files:
            rel_path = os.path.relpath(os.path.join(cwd, f), target_path)
            file_path = os.path.join(source_path, rel_path)

            if file_path not in hash_history:
                os.remove(os.path.join(target_path, rel_path)) # remove the extra file from the replica folder
                with open(log_file, 'a') as log_file_f:
                    log_file_f.write(f'{time.ctime()}: Removing the file in path {os.path.join(target_path, rel_path)}\n')
                    print(f'{time.ctime()}: Removing the file in path {os.path.join(target_path, rel_path)}\n')

            if rel_path not in file_list:
                os.remove(os.path.join(target_path, rel_path)) # remove the file that got deleted from the source folder
                with open(log_file, 'a') as log_file_f:
                    log_file_f.write(f'{time.ctime()}: Removing the file in path {file_path}\n')
                    print(f'{time.ctime()}: Removing the file in path {file_path}\n')

        for dir in dirs:                  #  delete the directory that got removed from the source
            dir_abs_path = os.path.join(cwd, dir)
            dir_rel_path = os.path.relpath(os.path.join(cwd, dir), target_path)
            if dir_rel_path not in dir_list:
                shutil.rmtree(dir_abs_path)
                with open(log_file, 'a') as log_file_f:
                    log_file_f.write(f'{time.ctime()}: Removing the directory in path {dir_rel_path}\n')
                    print(f'{time.ctime()}: Removing the directory in path {dir_rel_path}\n')

    time.sleep(int(sleep_time))              # polling interval
    
    
    
