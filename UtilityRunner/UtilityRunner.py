from UtilityRunner.UtilityScripts.ExampleUtilityScript import ExampleUtilityScript
import logging
import sys
from UtilityRunner.UtilityScripts.Exceptions.TooManyInputFiles import TooManyInputFiles
from UtilityRunner.UtilityScripts.PopulateYahooScript import PopulateYahooScript
from UtilityRunner.UtilityScripts.LoadNasdaqTickers import LoadNasdaqTickers
from UtilityRunner.UtilityScripts.RunComponentsScript import RunComponentScript

logging.basicConfig(level=logging.INFO)


utilityScripts = [
    ExampleUtilityScript(),
    PopulateYahooScript(),
    LoadNasdaqTickers(),
    RunComponentScript()
]


def main():
    numScript = 0
    for i in utilityScripts:
        print(str(numScript) + ":: \t \t \t " + i.getDescription())
        numScript += 1
    scriptToRun = input("What script would you like to run?\nScript Number: \t")

    if(len(sys.argv) == 2):
        utilityScripts[int(scriptToRun)].runWithArgFile(sys.argv[1])
    elif(len(sys.argv) == 1):
        utilityScripts[int(scriptToRun)].run()
    else:
        raise TooManyInputFiles

main()