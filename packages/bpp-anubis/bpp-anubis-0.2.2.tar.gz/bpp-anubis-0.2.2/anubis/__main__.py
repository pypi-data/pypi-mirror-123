# __main__.py
import os
import sys
import multiprocessing
from datetime import datetime
from multiprocessing import Pool
import shutil
import json

# custom
from anubis import account_splitter
from anubis import feature_splitter
from anubis import arg_parser
from anubis.parallelizer import command_generator
from anubis import results

ANUBIS_ASCII = (
    """
                    ♡♡♡                                               
                    ♡♡♡                                                 
                  ♡♡ ♡♡♡♡                                               
             ♡♡♡♡♡♡♡♡♡♡♡♡                                               
                     ♡♡♡♡♡                                              
                      ♡♡♡♡♡                                             
                   ♡♡♡♡♡♡♡♡♡                                            
                  ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡        ♡♡♡♡♡♡                         
                  ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡ ♡♡♡♡                     
                  ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡                   
              ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡     ♡♡♡♡♡♡♡♡♡♡                  
    ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡       ♡♡♡♡♡     ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡                 
                                                        ♡♡♡              
              POWERED BY ANUBIS                          ♡♡♡♡            
    (and the power of love  Σ>―(〃°ω°〃)♡→)               ♡♡♡♡♡          
                                                          ♡♡♡♡♡         
                                                           ♡♡♡♡         
                                                              ♡♡      
    """
)


def main():
    print(ANUBIS_ASCII)
    start = datetime.now()

    # parse arguments
    arguments = arg_parser.parse_arguments()

    # create a temp dir that will contain results and be exported
    output_path = os.path.join(arguments.output_dir)
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)

    # set up the multiple processes
    multiprocessing.set_start_method('fork')
    pool = Pool(arguments.processes)

    # get account data available for parallel runs
    print('\n--- PARSING ACCOUNTS')
    print(f'\tfile:          <{arguments.account_file}>')
    print(f'\tsection:       <{arguments.account_section}>')
    accounts_data = account_splitter.get_accounts(arguments.processes, arguments.account_file, arguments.account_section)

    # split up the features and store as list
    print('\n--- GROUPING FEATURES & ACCOUNTS')
    print(f'\tfeature dir:   <{arguments.dir}>')
    print(f'\tincluded tags: <{",".join([t for t in arguments.itags])}>')
    print(f'\texcluded tags: <{",".join([t for t in arguments.etags])}>')
    account_feature_groups = feature_splitter.get_features(arguments, accounts_data)

    # run all the processes and save the locations of the result files
    num_groups = len(account_feature_groups)
    print(f'\n--- RUNNING <{num_groups} PROCESS{"ES" * int(num_groups > 1)}>')
    result_files = pool.map(command_generator, account_feature_groups)

    # recombine everything
    print('\n--- COMBINING RESULTS')
    try:
        results.create_aggregate(files=result_files, aggregate_out_file=arguments.res)
    except Exception as e:
        print(e)

    # zip output if required
    if arguments.zip_output:
        results.zipper(output_path)

    if not arguments.save_output:
        shutil.rmtree(output_path)

    end = datetime.now()

    # calculate passes/fails for quick summary
    res_string = None
    passes, failures, other = 0, 0, 0
    try:
        with open(os.path.join(arguments.res)) as f:
            res = json.load(f)
        for feature in res:
            for scenario in feature['elements']:
                if scenario['keyword'].lower() != 'background':
                    status = scenario['status']
                    passes += 1 * int(status == 'passed')
                    failures += 1 * int(status == 'failed')
                    other += 1 * int(status != 'passed' and status != 'failed')
        res_string = f'{passes / (passes + failures) * 100:.2f}%'
    except Exception as e:
        # I know that this is a terrible anti-pattern, but there's really nothing to do for a failure
        pass

    # extremely basic summary
    print('\n========================================')
    print('                SUMMARY')
    print('========================================')
    print(f'Env(s):     <{",".join(arguments.env)}>')
    print(f'Browser:    <{arguments.browser}>')
    if arguments.save_output:
        print(f'Results:    <{arguments.res}>')
    else:
        print('Results:   <Results not saved; use "-so" to save>')
    print(f'Pass Rate: <{res_string if res_string else "could not calculate"}>')
    print(f'Run Time:   <{(end - start)}>')
    print('========================================')


if __name__ == '__main__':
    # run everything
    main()
    sys.exit(0)
