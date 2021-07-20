import os
import fnmatch
import datetime

def get_path(key):
    return os.getcwd()+f'/experiment/log-{key}'


def get_log_files(basepath, ftype):
    files_in_basepath = None
    with os.scandir(basepath) as entries:
        files_in_basepath = (entry for entry in entries if entry.is_file() and entry.name.endswith('.log'))
        # for file in files_in_basepath:
        #     print(file.name)
    for file in files_in_basepath:
        print(file.name)
    return files_in_basepath

def count_many_sims(basepath, key):
    timeout = 0
    success = 0
    low_bat = 0
    bt_fail = 0
    total = 0

    succeded= []
    faileds = []
    lows    = [] 
    timeouts= []   
    # print("Opening file: "+str(files))
    # for file in files:
    #         print(file.name)
    with os.scandir(basepath) as entries:
        files_in_basepath = (entry for entry in entries if entry.is_file() and entry.name.endswith('.log'))
        for file in files_in_basepath:
            print("Opening file: "+file.name)
            with open(file, 'r') as opened_file:
                lines = opened_file.readlines()
                last_line = ''
                # print("Opening file: "+str(lines[-1]))
                try:
                    last_line = lines[-1]
                except Exception as e:
                    pass
                
                print("with last line: "+last_line)
                if "reach-target" in last_line:
                    success = success + 1
                    succeded.append(file.name)
                elif "failure-bt" in last_line:
                    bt_fail = bt_fail + 1
                    faileds.append(file.name)
                elif "low-battery" in last_line:
                    low_bat = low_bat + 1
                    lows.append(file.name)
                else:
                    if "timeout" in last_line:
                        timeout = timeout + 1
                        timeouts.append(file.name)
            total = success+low_bat+timeout+bt_fail
    lows.sort(), timeouts.sort(), faileds.sort()
    print("lows: "+str(len(lows)/total)+" : "+str(lows))
    print("timeouts: "+str(len(timeouts)/total)+" : "+str(timeouts))
    print("faileds: "+str(len(faileds)/total)+" : "+str(faileds))
    print("succeded: "+str(len(succeded)/total))
    print("total: "+str(total))

    current_date = datetime.datetime.today().strftime('%H-%M-%S-%d-%b-%Y')
    with open(f'results-{key}-{current_date}.csv', 'w') as file:
        file.write('Type,Quantity,Percentage\n')
        file.write('BT Failure,'+str(len(faileds))+','+("%.2f"%(100*len(faileds)/total))+'\n')
        file.write('Timeout,'+str(len(timeouts))+','+("%.2f"%(100*len(timeouts)/total))+'\n')
        file.write('Low Battery,'+str(len(lows))+','+("%.2f"%(100*len(lows)/total))+'\n')
        file.write('Success,'+str(len(succeded))+','+("%.2f"%(100*len(succeded)/total))+'\n')
        file.write('Total,'+str(total)+','+("%.2f"%(100*total/total))+'\n')


def main():
    path = get_path('baseline')
    print(path)
    list_of_files = get_log_files(path, '.log')
    print(list_of_files)
    count_many_sims(path, 'baseline')


    # path = get_path('planned')
    # print(path)
    # list_of_files = get_log_files(path, '.log')
    # print(list_of_files)
    # count_many_sims(path, 'planned')

if __name__ == '__main__':
    main()