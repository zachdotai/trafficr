from multiprocessing import Process
import pyrebase
import requests
from time import localtime, sleep, strftime

import os

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
BASE_URL = "https://maps.googleapis.com/maps/api/directions/json?"
TIME_INTERVAL_IN_SECONDS = 1200 # every 20 minutes

def execute_api_request(road):
    url_request = requests.get(road.url)

    if url_request.status_code < 400 :
        json = url_request.json()

        if json["status"] == "OK" :
            print("Executing API request for " + road.name + " - " + road.direction + " direction")

            # The following line was commented in order to prevent
            # your local time from interfereing with the current database

            record_time_of_update_to_database()

            distance = json["routes"][0]["legs"][0]["distance"]["value"]
            duration_in_traffic = json["routes"][0]["legs"][0]["duration_in_traffic"]["value"]

            average_speed = distance / duration_in_traffic
            average_speed_in_kmph = average_speed * 3.6

            # The following line was commented in order to prevent
            # your local time from interfereing with the current database

            record_average_speed_to_database(road, average_speed_in_kmph)
        else :
            print(json["status"])
            record_status_update_to_database(json["status"], road.name, road.direction)
    else :
        record_response_update_to_database(str(url_request.status_code), road.name, road.direction)

def record_status_update_to_database(status, road_name, road_direction):
    status_update = {road_direction: status}
    time_string = strftime("%m-%d-%Y %H:%M", localtime())

    db = firebase.database()
    db.child("status").child(road_name).child(time_string).set(status_update)

def record_response_update_to_database(response, road_name, road_direction):
    response_update = {road_direction: response}
    time_string = strftime("%m-%d-%Y %H:%M", localtime())

    db = firebase.database()
    db.child("responses").child(road_name).child(time_string).set(response_update)

def record_time_of_update_to_database():
    hour_string = strftime("%H", localtime())
    day_string = strftime("%b %d", localtime())

    db = firebase.database()
    db.child("hours").child(day_string).child(hour_string).set(True)

def record_average_speed_to_database(road, average_speed):
    hour_string = strftime("%H", localtime())
    day_string = strftime("%b %d", localtime())

    db = firebase.database()
    readings_per_hour = db.child("readings").child(road.name).child(road.direction).child(day_string).child(hour_string).get()

    if readings_per_hour.val() == None :
        db.child("readings").child(road.name).child(road.direction).child(day_string).child(hour_string).set(1)
        db.child("results").child(road.name).child(road.direction).child(day_string).child(hour_string).set(average_speed)
    else :
        previously_recorded_vav = db.child("results").child(road.name).child(road.direction).child(day_string).child(hour_string).get()
        new_average_speed = (readings_per_hour.val() * previously_recorded_vav.val() + average_speed) / (readings_per_hour.val() + 1)

        db.child("readings").child(road.name).child(road.direction).child(day_string).child(hour_string).set(readings_per_hour.val() + 1)
        db.child("results").child(road.name).child(road.direction).child(day_string).child(hour_string).set(new_average_speed)

class Road:
    def __init__(self, name, origin, destination, waypoints, direction):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.waypoints = waypoints
        self.direction = direction
        self.url = BASE_URL + "origin=" + str(origin.latitude) + "," + str(origin.longtitude) + "&destination=" + str(destination.latitude) + "," + str(destination.longtitude) + "&waypoints=via:enc:" + waypoints + ":&departure_time=now&key=" + API_KEY

class Location:
    def __init__(self, latitude, longtitude):
        self.latitude = latitude
        self.longtitude = longtitude

# SCRIPT EXECUTION STARTS HERE

config = {
  "apiKey": API_KEY,
  "authDomain": os.getenv('AUTH_DOMAIN'),
  "databaseURL": os.getenv('DATABASE_URL'),
  "storageBucket": os.getenv('STORAGE_BUCKET'),
}

firebase = pyrebase.initialize_app(config)

roads = [
    Road("First Ring Road", Location(29.372077926186684, 47.968904972076416), Location(29.381436521355056, 47.99455761909485), "{tgrDgxwcH~SlQfKfLfUvPtLyBvHaWpA{h@SmXuBwl@yLi^qMaTkLqM_T}JySgDkN{BgSsA{N`G", "to"),
    Road("First Ring Road", Location(29.381314986673438, 47.99431085586548), Location(29.37182, 47.96860), "yoirDk~|cHjPaNhRvAzNzBfj@xQnIpJfNtTdFhLrGd]t@fb@Q|u@yKpa@kKbAwSePsIqJcUoR", "from"),
    Road("Second Ring Road", Location(29.34836438767089, 47.95699596405029), Location(29.36815098664146, 48.012657165527344), "qacrDwrucHlD{GrGiOrCaJhBuHfBsJzAsN^cNSyQmAwNyA_MkByL}FeYyGwU}Mc]cM}V{QmXwIcKmE_Fae@q_@cIiF{LaG", "to"),
    Road("Second Ring Road", Location(29.36810423644881, 48.01222801208496), Location(29.347980960981452, 47.95763969421387), "m|frDwj`dHjIfEfTzMfVdStM|NpUp[|MlV~Rng@vMpj@~@xGpCbTpAtSiAfb@eLdg@{I`T", "from"),
    Road("Third Ring Road", Location(29.35972, 48.02431), Location(29.31881, 47.92627), "cgerDmrbdHbKnTdOpRpT|OjG`DjKtIfMdR`QrX|KhTfQ~c@tMld@hKzk@|D`]vBt_@g@re@aDnd@_Etj@|Rt_@nm@bjAzZjx@", "to"),
    Road("Third Ring Road", Location(29.31848, 47.92603), Location(29.35961, 48.02451), "uh}qDgsocH}[uy@w|@wbB}CsPdGoj@~Bi`@ZyVmNa}A}Jqd@gVmr@iz@irAkb@uYgLoOcJ{R", "from"),
    Road("Fourth Ring Road", Location(29.30923, 47.88834), Location(29.33281106964723, 48.05387735366821), "ql{qDughcHbLy`BiNut@aTgmAmJ}vA}Dcw@kF_aAeFk_AoAwT}KiuBiMsxBqJwl@{_@maBiFof@sIwiA", "to"),
    Road("Fourth Ring Road", Location(29.33283, 48.05317), Location(29.30966, 47.88830), "s``rDofhdH|Gj_AtKz{@fOpo@vTlbAdNfwB~Bhe@xGlmA|Ej`AlCde@dJtdBrJteBdd@xhCeG~vA", "from"),
    Road("Fifth Ring Road", Location(29.32388, 48.08697), Location(29.30030, 47.78548), "{k~qDoundHwHj~@rOt}@dd@lw@zUv[rTriArO~iB|HzhB|Bht@zEtgBzFbsB~EjaBtF`}BtEh`AzCldAzKtcDlExsAXxkEw@xyDcCvlA", "to"),
    Road("Fifth Ring Road", Location(29.30556, 47.78377), Location(29.32355, 48.08725), "_yxqDedubHn@sfCd@ovBl@koCcAyz@gG_hBqJmtCyJwfCeF}wBkG_vBoE_aBwF_qBmLsvCwg@kuDqiAotCbKa}@", "from"),
    Road("Sixth Ring Road", Location(29.268224945070134, 48.082791566848755), Location(29.26508, 47.84243), "qksqDu}mdH~Q`cBXxiCx@t`Co@hdAuFd|CXlhB_AdeBkDnuBaBf~CvGvzG", "to"),
    Road("Sixth Ring Road", Location(29.26499, 47.84183), Location(29.26823, 48.08362), "ywrqDob`cHkFsgBsGueG`AmuB`EkdDpAefCGmnBnFyrCe@_cDsBsuDsOunA", "from"),
    Road("Seventh Ring Road", Location(29.26469, 47.83782), Location(29.18366, 48.11124), "uorqD_u~bHlt@q{BdeBceCxzEkMlsCitSfj@uoKsSk~AwYyyAoBcqBmOwx@", "to"),
    Road("Seventh Ring Road", Location(29.18387, 48.11130), Location(29.26685, 47.83294), "g{bqD}lsdH~Mnv@dB~eAJvl@nYptAxRv~Asn@pzGxEz`BgSprD}tB|sN}gI|hCyiAbjC", "from"),
    Road("Gulf Road", Location(29.35251, 47.94483), Location(29.26948, 48.08567), "m~crDkdscHwgAmtAezA}uAaf@mo@y`@utA~Fmm@blAmQdr@qs@zZ_|@z]}O`s@}i@`}@mnBfEapAkIek@gWehA{MsbAvL_StlAhM|sBfe@zi@bErbA~Dpg@uBjbCmA", "to"),
    Road("Gulf Road", Location(29.26943, 48.08598), Location(29.35227, 47.94480), "}_tqDudodH{x@J}dA|LcjByButAmLqeAq]}mAcJ~GthB`Rrz@RxyBarBjvC{v@tkAirAb{@}r@`WtKjsAzs@xhAxhAjiAnWzVbp@lz@`W~X", "from"),
    Road("Jamal Abdul Naser Street", Location(29.358318948743094, 47.956212759017944), Location(29.31974, 47.80504), "e|drDigucHzMb^|Y~h@xYhl@pm@|rAjOrc@``@xaAlUzq@t_@j`AdYv[hCb{BsM|wCiDzvBjDdm@Phg@", "to"),
    Road("Jamal Abdul Naser Street", Location(29.31958, 47.80517), Location(29.35785, 47.95588), "ao}qDi_xbHaDwhAjEcoAhEk_BbHutBjH{iAeKwb@e^qi@_Scm@cn@uwAuZoz@gUyr@yRi_@kJ_PeZcl@_Wqc@yTuh@", "from"),
    Road("Jahra Road", Location(29.35880, 47.96277), Location(29.31170, 47.78988), "eaerDuuvcH|c@bT~SvTxUhUl`@lt@xo@xmAx_@rdAv^bbAl}@`qCdLlq@HxmAo@v`BqEhs@s@foDq@ddC", "to"),
    Road("Jahra Road", Location(29.31149, 47.78787), Location(29.35863, 47.96294), "g{{qDcyubHP_sAbJatJg@kgBcNw_@afA_wCyQef@i[k_Ac{@s~Ayn@}`AwWeT{b@aT", "from"),
    Road("Airport Road", Location(29.34786, 47.94029), Location(29.25334273629128, 47.97278881072998), "c{brDulrcHfb@a[`K{Fx^y[`LkI~o@y[hk@ySp[iDxQuBvc@{Exf@mFv{BqVhl@sGndA{Kp[kD", "to"),
    Road("Airport Road", Location(29.25251, 47.97314), Location(29.34798, 47.94045), "_spqDuuxcHq|@rJ}a@vEoeB~Qc_@|DihAzLqn@|Geh@~F}g@nOcv@z^a_@fUuUlT{[pV", "from"),
    Road("Riyadh Road", Location(29.35786, 47.97365), Location(29.24590, 47.96786), "indrDcyxcHnaAjDraAlG|k@aFpo@mK~q@mN|a@uIpk@oLpuAuZxd@mEziAgHl{Ajz@oE|l@zc@jS", "to"),
    Road("Riyadh Road", Location(29.24613, 47.96820), Location(29.35794, 47.97470), "wfoqDyuwcHab@q[|BeaBipACc}@hG}{@vGcy@~QodA`T}pA`X{h@bJcu@lJkbAeGg|@}C", "from"),
    Road("Al Maghreb Road - 1", Location(29.36067, 47.98682), Location(29.26550, 48.04197), "q~drD}x{cH~HuEbd@mWlj@{[tP{J|w@{c@zx@ue@twAex@vlBso@dz@k]xtAmj@", "to"),
    Road("Al Maghreb Road - 1", Location(29.26521, 48.04242), Location(29.36053, 47.98772), "{dsqDwcfdH_nA`g@ijA|e@wdBtk@u~Aj|@aq@l`@g{@`f@su@tc@cj@t[", "from"),
    Road("Al Maghreb Road - 2", Location(29.26449, 48.04236), Location(29.17649, 48.06873), "qprqDyifdHnp@yMt{AeZnvB}a@v{AeZxnDss@", "to"),
    Road("Al Maghreb Road - 2", Location(29.17659, 48.06891), Location(29.26393, 48.04283), "eyaqDejkdHuuAzYsjAfUgbB|[osBna@}vC`k@", "from"),
    Road("Fahaheel Road - 1", Location(29.37305, 47.99695), Location(29.26911, 48.08456), "sugrDq|}cHbd@caAxHyPpGyKf_@sa@rV}Ub]uZx_@_V~nAkj@r`Asr@hj@wa@v~@sq@~y@qm@niAiq@jgAyk@", "to"),
    Road("Fahaheel Road - 1", Location(29.26931, 48.08478), Location(29.37292, 47.99810), "q|sqDcmndH{kAnn@mcA~l@qbAlt@ql@vc@aW`Rq`Avr@ia@xYycAxc@ev@tf@mh@hg@wWlXoSp^sVzh@wQz`@", "from"),
    Road("Fahaheel Road - 2", Location(29.18428, 48.11210), Location(29.26871, 48.08499), "idcqDmzsdHyfAhUskAzVmhBp_@{~@|RcfAhVorBpf@", "to"),
    Road("Fahaheel Road - 2", Location(29.26862, 48.08474), Location(29.18425, 48.11185), "qisqD}rndHb}@{Sts@oQn|Aw]|kAaW~u@iPzyAuZ`vAaZ", "from")
]

while True:
    time_of_exectuion = strftime("%m-%d-%Y %H:%M", localtime())
    print("Executing a new request on " + time_of_exectuion)
    for road in roads :
        #print("Executing a new request")
        process = Process(target=execute_api_request(road))
        process.start()

    print("Waiting...")
    sleep(TIME_INTERVAL_IN_SECONDS)
