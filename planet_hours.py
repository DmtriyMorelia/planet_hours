#!/usr/bin/env python3
#!python3 -m pip install suntime
import datetime, time,locale
from suntime import Sun, SunTimeException
planets = dict([
	["Sun", "\u2609"],
	["Venera" , "\u2640"],
	["Mercury" , "\u263F"],
	["Moon" , "\u263D"],
	["Saturn" , "\u2644"],
	["Jupyter" , "\u2643"],
	["Mars" , "\u2642"]])
latitude, longitude = 59+(56+23/60)/60,30+(18+35/60)/60
latitude, longitude = 59.9983859, 30.3877919
latitude, longitude = 59.998411,30.388522
DBG = 0
def coord(latitude, longitude):
	g1, g2 = int(latitude), int(longitude)
	s1, s2 = (latitude - g1) * 3600, (longitude - g2) * 3600
	m1, m2 = s1 // 60, s2 // 60
	s1, s2 = s1 % 60, s2 %60
	return [int(g1),int(m1),s1,int(g2),int(m2),s2]
def tude(tude):
	return  "{0[0]}°{0[1]}\'{0[2]:2.3f}\"".format(
		[
			int(tude),
			int(tude * 60 % 60),
			tude * 360000 % 6000 /100
		])
def sun_rise_set(latitude, longitude, abd, TZ="UTC" ):
	sun = Sun(latitude, longitude)
	if (TZ == "UTC"):
		today_sr = sun.get_sunrise_time()
		today_ss = sun.get_sunset_time()
		if DBG:
			print('Today at {2[0]}°{2[1]}\'{2[2]:2.2f}"N {2[3]}°{2[4]}\'{2[5]:2.2f}"E the sun raised at {0} and get down at {1} UTC'.format( today_sr.strftime('%H:%M:%S'), today_ss.strftime('%H:%M:%S'), coord(latitude, longitude)))
		return today_sr, today_ss
	else:
		abd_sr = sun.get_local_sunrise_time(abd)
		abd_ss = sun.get_local_sunset_time(abd)
		if DBG:
			print('On {0} the sun at {2[0]}°{2[1]}\'{2[2]:2.2f}\"N {2[3]}°{2[4]}\'{2[5]:2.2f}\"E raised at {1} and get down at {3}.'.
			format(
				abd,
				abd_sr.strftime('%H:%M:%S'),
				coord(latitude, longitude),
				abd_ss.strftime('%H:%M:%S')))
		return abd_sr, abd_ss
def answer(prompt=""):
	x = input(prompt)
	return x in set(["", "y", "Y", "д", "Д"])

if answer('рассчёт на сегодня["д"|"н"]?'):
	abd = datetime.date.today()
else:
	abd = datetime.date(int(input('год: ')), int(input('месяц: ')), int(input('число: ')))

sr,ss = sun_rise_set(latitude, longitude, abd, "local")
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
print("рассчёт на: ", abd.strftime('%A %Y-%m-%d'))
while True:
	print("координаты  места: {}N {}E[{},{}] ?".format( tude(latitude), tude(longitude), latitude, longitude), end='')
	if  answer(""):
		break
	else:
		latitude, longitude = [float(x) for x in input("координаты:  ").split(",")]
#		print(latitude, longitude)
print("https://google.com/maps/dir/Current+Location/{0},{1}/@{home_lat},{home_lon},{zoom}z".format(latitude,longitude,home_lat=latitude,home_lon=longitude,zoom=19))
print("восход {} ; закат {}".format(sr.strftime('%H:%M:%S'),ss.strftime('%H:%M:%S')))
day_time = ss - sr
magic_hour = day_time / 12
print("долгота дня : ", day_time)#.strftime('%H:%M:%s'))
print("дневной магический час :", magic_hour)
fh = sr
day_num = abd.isoweekday()
print("время начала дневных планетарных часов")
for i in range(13):
	magic_hour_num = (24 * day_num + i)% 7
	print("{0}. ({1}) {3}".format(("\n начало 1-го планетарный час ночи ",i+1)[i!=12],list(planets.values())[magic_hour_num],list(planets.keys())[magic_hour_num],fh.strftime('%H:%M:%S')), end="\t")
#	print("{0} ({2:8}{1}) {3}".format(i+1,list(planets.values())[magic_hour_num],list(planets.keys())[magic_hour_num],fh.strftime('%H:%M:%S')), end="\t")
#	print(i+1," (",list(planets.values())[magic_hour_num],list(planets.keys())[magic_hour_num],") : ",fh.strftime('%H:%M:%S'), end="\t")
	fh += magic_hour
