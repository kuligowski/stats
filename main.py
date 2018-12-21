import asyncio
from pandas.io.json import json_normalize
from .RequestController import *
from .CsvWriter import *
from .PlotDrawer import *

class Stat:

    def __init__(self, statName, statData, kind='bar', yFormatter = None):
        self._name = statName
        self._statData = statData
        self._statKind = kind
        self._yaxisFormatter = yFormatter


async def main():

    c = RestController()
    s = PlotDrawer()

    data = await c.fetchasync()  
    data.sort(key=lambda f: (f['launch_year'], f['rocket']['rocket_id']))

    payloads = json_normalize(data,
        record_path=[['rocket', 'second_stage', 'payloads']],
        meta=['flight_number','launch_success','mission_name','mission_id','launch_year', ['rocket','rocket_id']])
    payloadByYearAndRocket = payloads.groupby(['launch_year','rocket.rocket_id'])
    payloadSum = payloadByYearAndRocket['payload_mass_kg'].sum()
    launchSuccessRate = payloadByYearAndRocket['launch_success'].mean()

    cores = json_normalize(data,
        record_path=[['rocket', 'first_stage', 'cores']],
        meta=['flight_number','launch_success','mission_name','mission_id','launch_year', ['rocket','rocket_id']])
    coresLanding = cores.query('landing_intent == True').query('land_success == True or land_success == False')
    coresLanding['land_success'] = coresLanding['land_success'].apply(lambda x: bool(x))
    landSuccessRate = coresLanding.groupby(['launch_year','rocket.rocket_id'])['land_success'].mean()

    coresLandingASDSSuccessRate = coresLanding.query('landing_type == "ASDS"').groupby(['launch_year','rocket.rocket_id'])['land_success'].mean()
    coresLandingOceanSuccessRate = coresLanding.query('landing_type == "Ocean"').groupby(['launch_year','rocket.rocket_id'])['land_success'].mean()


    stats = [
        Stat('payload in kg', payloadSum.unstack(), 'area'),
        Stat('total launches', payloadByYearAndRocket.size().unstack()),
        Stat('launch success rate', launchSuccessRate.unstack(), yFormatter='percent'),
        Stat('landing success rate', landSuccessRate.unstack(), yFormatter='percent'),
        Stat('ASDS landing success rate', coresLandingASDSSuccessRate.unstack(), yFormatter='percent'),
        Stat('Ocean landing success rate', coresLandingOceanSuccessRate.unstack(), yFormatter='percent')]

    cw = CsvWriter()

    writeCSVTasks = [cw.writeToCSV(stat._statData, stat._name) for stat in stats]
    writeCSVTasks.append(cw.writeToCSV(payloads, 'payloadData'))
    writeCSVTasks.append(cw.writeToCSV(cores, 'coresData'))
    await asyncio.gather(*writeCSVTasks)   

    s.drawStats(stats)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())  
    loop.close()
