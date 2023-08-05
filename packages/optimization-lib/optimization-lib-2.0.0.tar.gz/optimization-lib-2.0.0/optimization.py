import os
import time
import logging
try:
    from colorama import init, Fore, Style
except:
    os.system("pip install colorama")
    from colorama import init, Fore, Style

__version__ = '0.0.2'


class OptimizationLibrary:

    def __init__(self, variance=None, color=False):
        init()
        logging.basicConfig(level=logging.DEBUG)
        self.start_time = time.time()
        self.color = color
        self.vairance = variance

    def start_timer(self):
        if self.color:
            print(f"{Fore.MAGENTA}Starting optimization{Style.RESET_ALL}")
        else:
            logging.debug("Starting optimization")
        return time.time()

    def end_timer(self):
        if self.vairance:
            test_range = self.vairance
        else:
            test_range = .005
        optimized_time = time.time() - self.start_time
        if self.color:
            print(f"{Fore.MAGENTA}Overall Run-time:")
            print(f"{optimized_time} {Style.RESET_ALL}")
            runtime = os.getcwd() + '/run_file.txt'
        else:
            logging.debug(f"Overall Run-time:")
            logging.debug(f"{optimized_time}")
            runtime = os.getcwd() + '/run_file.txt'
        try:
            with open(runtime, 'r') as run:
                last_runtime = float(run.readline())
            if last_runtime:
                upper_bound = last_runtime + test_range
                lower_bound = last_runtime - test_range
                if optimized_time > upper_bound:
                    if self.color:
                        print(f"{Fore.RED}Previous Run-time: {Style.RESET_ALL}")
                        print(f"{Fore.RED}{last_runtime} {Style.RESET_ALL}")
                        print(f"{Fore.RED}Decrease in run performance {Style.RESET_ALL}")
                    else:
                        logging.debug("Previous Run-time:")
                        logging.debug(str(last_runtime))
                        logging.debug("Decrease in run performance")

                elif optimized_time < lower_bound:
                    if self.color:
                        print(f"{Fore.GREEN}Previous Run-time: {Style.RESET_ALL}" )
                        print(f"{Fore.GREEN}{last_runtime} {Style.RESET_ALL}")
                        print(f"{Fore.GREEN}Increase in run performance {Style.RESET_ALL}")
                    else:
                        logging.debug("Previous Run-time:")
                        logging.debug(str(last_runtime))
                        logging.debug("Increase in run performance")

                else:
                    if self.color:
                        print(f"{Fore.RED} Previous Run-time: {Style.RESET_ALL}")
                        print(f"{Fore.RED} {last_runtime} {Style.RESET_ALL}")
                        print(f"{Fore.RED} Decrease in run performance {Style.RESET_ALL}")
                    else:
                        logging.debug("Previous Run-time:")
                        logging.debug(str(last_runtime))
                        logging.debug("No performance change")
        except Exception as e:
            logging.debug(f"No previous run information: {e}")
        with open(runtime, 'w') as run:
            run.write(str(optimized_time))

