# https://opensource.org/licenses/GPL-3.0

# import esp
import gc
import machine
# import micropython
import ntptime
import time
import utime
# from common import led

from env_sense import bme280_int as bme280
from env_sense import pms7003
from env_sense import aqi
from env_sense import publishThingspeak

SECONDS_BETWEEN_READINGS = 16
SAMPLES = 2
FREQUENCY_BME_MINS = 10
FREQUENCY_AIR_MINS = 30
# assumes BME < AIR; and that AIR is a multiple of BME

# Thingspeak:
TS_CHANNEL_ID = b'1229949'
TS_CHANNEL_WRITE_API_KEY = b'MD2BOTGRJ8JE8J6U'

ts = None
air = None
bme = None
dummy_air = None


# https://cfpub.epa.gov/si/si_public_record_report.cfm?dirEntryId=349513&Lab=CEMM
# https://cfpub.epa.gov/si/si_public_file_download.cfm?p_download_id=540979&Lab=CEMM
def us_epa_correction(pm2_5cf1, rel_humi):
    if rel_humi == 0:
        rel_humi = 60
    return (0.52 * pm2_5cf1) - (0.085 * rel_humi) + 5.71


def ts_publish(ts, reading_bme, reading_air):
    if reading_air:
        pm2_5_corr = us_epa_correction(reading_air['pm2_5cf1'], rel_humi=reading_bme[2])
        aqi25_instant = aqi.AQI.PM2_5(pm2_5_corr)
        data = {'field1': round(aqi25_instant),
                'field2': reading_air['pm1_0'],
                'field3': reading_air['pm2_5'],
                'field4': reading_air['pm2_5cf1'],
                'field5': reading_air['pm10'],
                'field6': reading_bme[0],  # temp
                'field7': reading_bme[1],  # pressure
                'field8': reading_bme[2],  # humidity
                }
    else:
        data = {'field6': reading_bme[0],  # temp
                'field7': reading_bme[1],  # pressure
                'field8': reading_bme[2],  # humidity
                }
    print('Uploading: ', end='')
    for k, v in sorted(data.items(), key=lambda x: x[0]):
        print(v, end=', ')
    print()
    ts.publish(data)


# -----------------------------------------------------------------------------------------------------------
# Init / read sensors
# -----------------------------------------------------------------------------------------------------------
class Sensor:
    def wakeup(self):
        pass

    def sleep(self):
        pass

    def read(self):
        return {}


class SensorAir(Sensor):
    WARMUP_SECONDS = 30

    def __init__(self):
        self.sensor = pms7003.PassivePms7003Sensor(uart=0)
        time.sleep(5)  # a wakeup followed too quickly by sleep causes pms7003 to error out
        self.sensor.sleep()

    def wakeup(self, warmup=True):
        self.sensor.wakeup()
        if warmup:
            print("Warming up PMS7003: {} sec.".format(SensorAir.WARMUP_SECONDS))
            time.sleep(SensorAir.WARMUP_SECONDS)
        self.read()

    def read(self):
        return self.sensor.read()

    def sleep(self):
        self.sensor.sleep()

    # def read(self):
    #     return {'pm1_0': -1,
    #             'pm2_5': -1,
    #             'pm2_5cf1': -1,
    #             'pm10': -1}


# class SensorBME_dummy(Sensor):
#     def __init__(self):
#         pass

#     def read(self):
#         return [0, 0, 0]


class SensorBME(Sensor):
    # SCL = D1 = 5 = scl_pin_id
    # SDA = D2 = 4 = sda_pin_id

    def __init__(self):
        i2c = machine.I2C(scl=machine.Pin(5, machine.Pin.OUT),
                          sda=machine.Pin(4))
        self.bme = bme280.BME280(i2c=i2c)

    def read(self):
        t, p, h = self.bme.read_compensated_data()
        t /= 100
        t = t*1.8 + 32
        p /= 256
        h /= 1024
        return [round(t, 1), p/100, round(h, 1)]

    def wakeup(self):
        # first couple readings, especially after moving rooms and cold-booting tend to be outliers
        self.read()
        time.sleep(2)
        self.read()
        time.sleep(2)


def init_sensors():
    global ts, air, bme, dummy_air
    while True:
        try:
            ntptime.settime()
            ts = publishThingspeak.ThingspeakMqtt(TS_CHANNEL_ID, TS_CHANNEL_WRITE_API_KEY)
            air = SensorAir()
            bme = SensorBME()
            dummy_air = Sensor()
            break
        except Exception as e:
            print(e)
            print("init_sensors failed, retrying in 3.")
            time.sleep(3)  # retry
    return True


def read_sensors_and_publish(include_air=False):
    global need_to_run
    if not need_to_run:
        return
    air_or_dummy = air if include_air else dummy_air

    air_or_dummy.wakeup()
    bme.wakeup()
    for i in range(SAMPLES):
        ts_publish(ts, bme.read(), air_or_dummy.read())
        time.sleep(SECONDS_BETWEEN_READINGS)
    air_or_dummy.sleep()

    need_to_run = False


def main():
    global need_to_run
    init_sensors()
    retries = 0

    while True:
        try:
            # only call the air sensor occasionally
            include_air = utime.localtime()[4] % FREQUENCY_AIR_MINS == 0
            t = utime.localtime()
            t_fmt = "{}-{}-{} {}:{}:{} GMT".format(t[0], t[1], t[2], t[3], t[4], t[5])
            print('Main loop called: {}. Sensing air: {}'.format(t_fmt, include_air))
            need_to_run = True
            read_sensors_and_publish(include_air)
            # led.flash(2)

            # sleep until next wake up time
            try:
                ntptime.settime()
            except OSError:
                pass
            now = utime.localtime()
            secs_until_next = (FREQUENCY_BME_MINS - (now[4] % FREQUENCY_BME_MINS))*60 - now[5]
            gc.collect()
            print("Sleeping for {} seconds. Free mem: {}".format(secs_until_next, gc.mem_free()))
            time.sleep(secs_until_next+5)  # pad so we don't start too early if the RTC runs fast
            retries = 0
        except Exception as e:
            retries += 1
            if retries > 10:
                machine.reset()
            print(e)
            print("Main loop iteration failed. Retrying in 15.")
            time.sleep(15)  # retry


def do(include_air=True):
    global need_to_run
    need_to_run = True
    read_sensors_and_publish(include_air)
