#import MySQLdb
import random, time
from handlers import alarmHandler, alarm_types, burnerLogHandler
from utils import timeUtil
import sys, traceback

TEMPERATURES = ['BoilerTemperatureValue', 'IndoorTemperatureValue', 'OutdoorTemperatureValue', 'SupplyTemperatureValue']
STATES = ["Alarm","Stby","Ign1","Ign2","Ign3","Ign4","Ign5","Hi","Lo","Shtdwn","Shtdwn2","Test"]

try:
    SLEEP_TIME = int(sys.argv[1])
except:
    SLEEP_TIME = 1

def generate_temperature_logs(burner_sn = '1234567890A'):
    key = random.choice(TEMPERATURES)
    deg = random.randrange(100)
    burner_log = {'burner_sn': burner_sn, 'component_key': key, 'value': deg}
    print("Burnerlog generated: " + str(burnerLogHandler.insert(burner_log)))

def generate_state_change(burner_sn = '1234567890A'):
    state = random.choice(STATES)

    log = {
        'burner_sn' : burner_sn,
        'component_key' : state,
        'value': random.randrange(100)
    }
    print("STATECHANGE", burnerLogHandler.insert(log))

def generate_alarm(burner_sn = '1234567890A'):
    type_key = random.choice(list(alarm_types.ALARM_TYPES.keys()))
    severity = random.choice([alarm_types._ERROR, alarm_types._INFO, alarm_types._WARNING])
    print("Alarm generated: " + str(alarmHandler.create_alarm(type_key, severity, timeUtil.now(), burner_sn, 'Q')))

i = 0
while True:
    i += 1
    try:
        generate_alarm()
        generate_temperature_logs()

        if i % 3 == 0:
            generate_state_change()

    except Exception:
        traceback.print_exc()
        print("Some arbitrary error")
    finally:
        time.sleep(SLEEP_TIME)
