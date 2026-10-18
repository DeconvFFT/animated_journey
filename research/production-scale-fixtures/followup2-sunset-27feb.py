# NOAA solar calculator (approximate, +/- 2 min). Computed for 2027-02-27, local standard time offsets as stated.
import math, datetime
def sunset(lat, lon, tz, date):
    n = date.timetuple().tm_yday
    g = 2*math.pi/365*(n-1+(12-12)/24)
    eqt = 229.18*(0.000075+0.001868*math.cos(g)-0.032077*math.sin(g)-0.014615*math.cos(2*g)-0.040849*math.sin(2*g))
    decl = 0.006918-0.399912*math.cos(g)+0.070257*math.sin(g)-0.006758*math.cos(2*g)+0.000907*math.sin(2*g)-0.002697*math.cos(3*g)+0.00148*math.sin(3*g)
    la = math.radians(lat)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833))/(math.cos(la)*math.cos(decl))-math.tan(la)*math.tan(decl)))
    ss = 720-4*(lon-ha)-eqt+tz*60 if False else 720-4*(lon-ha)-eqt  # UTC minutes
    # sunset uses -ha
    ss = 720-4*(lon-ha)-eqt
    ss_local = ss + tz*60
    return f"{int(ss_local//60):02d}:{int(ss_local%60):02d}"
d = datetime.date(2027,2,27)
for name,lat,lon,tz in [("London",51.51,-0.13,0),("New York",40.71,-74.01,-5),("Chicago",41.88,-87.63,-6),("Los Angeles",34.05,-118.24,-8),("Toronto",43.65,-79.38,-5),("Dubai",25.2,55.27,4),("Karachi",24.86,67.0,5),("Delhi",28.61,77.21,5.5),("Singapore",1.35,103.82,8),("Sydney",-33.87,151.21,11)]:
    print(f"{name:12s} sunset about {sunset(lat,lon,tz,d)} local standard time (no daylight saving in force on 27 Feb for these zones except Sydney, which is on AEDT +11)")
