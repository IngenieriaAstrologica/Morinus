import astrology
import chart
import houses
import planets
import options
import util


class Syzygy:
	LON = 0
	LAT = 1
	RA = 2
	DECL = 3

	#for topical almutens
	TOPICALDEFAULT = 0
	TOPICALCONIUNCTIO = 1
	TOPICALOPPOSITIO = 2
	TOPICALOPPOSITIORADIX = 3
	TOPICALMOON = 4

	def __init__(self, chrt):
		self.time = chrt.time
		self.lon = chrt.planets.planets[astrology.SE_MOON].data[planets.Planet.LONG]

		self.flags = astrology.SEFLG_SPEED+astrology.SEFLG_SWIEPH

		#for topical almutens
		self.lons = []

		if not chrt.time.bc:
			lonsun = chrt.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]
			lonmoon = chrt.planets.planets[astrology.SE_MOON].data[planets.Planet.LONG]

			d, m, s = util.decToDeg(lonsun)
			lonsun = d+m/60.0+s/3600.0
			d, m, s = util.decToDeg(lonmoon)
			lonmoon = d+m/60.0+s/3600.0

			diff = lonmoon-lonsun
			self.newmoon, self.ready = self.isNewMoon(diff)

			if not self.ready:
				ok, self.time, self.ready = self.getDateHour(self.time, chrt.place, self.newmoon)
				if not self.ready:
					ok, self.time, self.ready = self.getDateMinute(self.time, chrt.place, self.newmoon)
					if not self.ready:
						ok, self.time, self.ready = self.getDateSecond(self.time, chrt.place, self.newmoon)

			hses = houses.Houses(self.time.jd, 0, chrt.place.lat, chrt.place.lon, chrt.options.hsys, chrt.obl[0], chrt.options.ayanamsha, chrt.ayanamsha)
			moon = planets.Planet(self.time.jd, astrology.SE_MOON, self.flags, chrt.place.lat, hses.ascmc2)
			if self.newmoon:
				self.lon = moon.data[planets.Planet.LONG]
			else:
				if chrt.options.syzmoon == options.Options.MOON:
					self.lon = moon.data[planets.Planet.LONG]
				elif chrt.options.syzmoon == options.Options.ABOVEHOR:
					if moon.abovehorizon:
						self.lon = moon.data[planets.Planet.LONG]
					else:
						sun = planets.Planet(self.time.jd, astrology.SE_SUN, self.flags)
						self.lon = sun.data[planets.Planet.LONG]
				else:
					moon = planets.Planet(self.time.jd, astrology.SE_MOON, self.flags, chrt.place.lat, chrt.houses.ascmc2)
					if moon.abovehorizon:
						self.lon = moon.data[planets.Planet.LONG]
					else:
						sun = planets.Planet(self.time.jd, astrology.SE_SUN, self.flags)
						self.lon = sun.data[planets.Planet.LONG]

		ra, decl, dist = astrology.swe_cotrans(self.lon, 0.0, 1.0, -chrt.obl[0])
		self.speculum = [self.lon, 0.0, ra, decl]

		#the other syzygy (i.e. if the syzygy was conjunction then calculate the opposition and vice versa)
		self.lon2 = chrt.planets.planets[astrology.SE_MOON].data[planets.Planet.LONG]
		if not chrt.time.bc:
			self.time2 = self.time
			ok, self.time2, self.ready2 = self.getDateHour(self.time2, chrt.place, not self.newmoon)
			if not self.ready2:
				ok, self.time2, self.ready2 = self.getDateMinute(self.time2, chrt.place, not self.newmoon)
				if not self.ready2:
					ok, self.time2, self.ready2 = self.getDateSecond(self.time2, chrt.place, not self.newmoon)

			hses2 = houses.Houses(self.time2.jd, 0, chrt.place.lat, chrt.place.lon, chrt.options.hsys, chrt.obl[0], chrt.options.ayanamsha, chrt.ayanamsha)
			moon2 = planets.Planet(self.time2.jd, astrology.SE_MOON, self.flags, chrt.place.lat, hses2.ascmc2)
			if not self.newmoon:
				self.lon2 = moon2.data[planets.Planet.LONG]
			else:
				if chrt.options.syzmoon == options.Options.MOON:
					self.lon2 = moon2.data[planets.Planet.LONG]
				elif chrt.options.syzmoon == options.Options.ABOVEHOR:
					if moon2.abovehorizon:
						self.lon2 = moon2.data[planets.Planet.LONG]
					else:
						sun2 = planets.Planet(self.time2.jd, astrology.SE_SUN, self.flags)
						self.lon2 = sun2.data[planets.Planet.LONG]
				else:
					moon2 = planets.Planet(self.time2.jd, astrology.SE_MOON, self.flags, chrt.place.lat, chrt.houses.ascmc2)
					if moon2.abovehorizon:
						self.lon2 = moon2.data[planets.Planet.LONG]
					else:
						sun2 = planets.Planet(self.time2.jd, astrology.SE_SUN, self.flags)
						self.lon2 = sun2.data[planets.Planet.LONG]

			ra2, decl2, dist2 = astrology.swe_cotrans(self.lon2, 0.0, 1.0, -chrt.obl[0])
			self.speculum2 = [self.lon2, 0.0, ra2, decl2]

			#for topical almutens
			self.lons.append(self.lon)#Default
			if self.newmoon: #Conjunction
				self.lons.append(self.lon)
			else:
				self.lons.append(self.lon2)
			#Moon in chart of Syzygy
			hses = houses.Houses(self.time.jd, 0, chrt.place.lat, chrt.place.lon, chrt.options.hsys, chrt.obl[0], chrt.options.ayanamsha, chrt.ayanamsha)
			moonSyz = planets.Planet(self.time.jd, astrology.SE_MOON, self.flags, chrt.place.lat, hses.ascmc2)
			hses2 = houses.Houses(self.time2.jd, 0, chrt.place.lat, chrt.place.lon, chrt.options.hsys, chrt.obl[0], chrt.options.ayanamsha, chrt.ayanamsha)
			moonSyz2 = planets.Planet(self.time2.jd, astrology.SE_MOON, self.flags, chrt.place.lat, hses2.ascmc2)
			if not self.newmoon: #Opposition
				if moonSyz.abovehorizon:
					self.lons.append(moonSyz.data[planets.Planet.LONG])
				else:
					sun = planets.Planet(self.time.jd, astrology.SE_SUN, self.flags)
					self.lons.append(sun.data[planets.Planet.LONG])
			else:
				if moonSyz2.abovehorizon:
					self.lons.append(moonSyz2.data[planets.Planet.LONG])
				else:
					sun2 = planets.Planet(self.time2.jd, astrology.SE_SUN, self.flags)
					self.lons.append(sun2.data[planets.Planet.LONG])
			if not self.newmoon: #OppositionRadix
				moon = planets.Planet(self.time.jd, astrology.SE_MOON, self.flags, chrt.place.lat, chrt.houses.ascmc2)
				if moon.abovehorizon:
					self.lons.append(moon.data[planets.Planet.LONG])
				else:
					sun = planets.Planet(self.time.jd, astrology.SE_SUN, self.flags)
					self.lons.append(sun.data[planets.Planet.LONG])
			else:
				moon = planets.Planet(self.time2.jd, astrology.SE_MOON, self.flags, chrt.place.lat, chrt.houses.ascmc2)
				if moon.abovehorizon:
					self.lons.append(moon.data[planets.Planet.LONG])
				else:
					sun = planets.Planet(self.time.jd, astrology.SE_SUN, self.flags)
					self.lons.append(sun.data[planets.Planet.LONG])
			if not self.newmoon: #Opposition Moon
				self.lons.append(moonSyz.data[planets.Planet.LONG])
			else:
				self.lons.append(moonSyz2.data[planets.Planet.LONG])


	def isNewMoon(self, diff):
		newmoon = True
		ready = False

		if diff == 0.0:
			newmoon = True
			ready = True
		elif diff == 180.0 or diff == -180.0:
			newmoon = False
			ready = True
		elif diff < 0.0:
			if diff < -180.0:
				newmoon = True
			else:
				newmoon = False
		elif diff > 0.0:
			if diff > 180.0:
				newmoon = False
			else:
				newmoon = True

		return newmoon, ready


	# Max. rate of change of the Sun-Moon elongation, used only to undershoot
	# coarse jumps (deg per day/minute/second). The exact hour/minute/second
	# refinement below is unchanged, so results are identical.
	MAXELONGDAY = 15.5
	MAXELONGMIN = MAXELONGDAY/1440.0
	MAXELONGSEC = MAXELONGDAY/86400.0

	def elongLons(self, jd):
		# Light-weight Sun/Moon longitudes for the search: the same values
		# planets.Planet() would compute, without the speed/equatorial cost
		rflag, sundata, serr = astrology.swe_calc_ut(jd, astrology.SE_SUN, astrology.SEFLG_SWIEPH)
		rflag, moondata, serr = astrology.swe_calc_ut(jd, astrology.SE_MOON, astrology.SEFLG_SWIEPH)
		return sundata[planets.Planet.LONG], moondata[planets.Planet.LONG]

	def truncDiff(self, lonsun, lonmoon):
		d, m, s = util.decToDeg(lonsun)
		lonsun = d+m/60.0+s/3600.0
		d, m, s = util.decToDeg(lonmoon)
		lonmoon = d+m/60.0+s/3600.0
		return lonmoon-lonsun

	def coverBack(self, diff, newmoonorig):
		# Elongation degrees to step back to reach the wanted phase boundary.
		# Call with the raw (untruncated) elongation: truncation noise (up to
		# 2 arcsec) would translate into seconds of sizing error.
		if newmoonorig:
			return diff % 360.0
		return (diff-180.0) % 360.0

	def startsPastFlip(self, tim, newmoonorig, delta):
		# True if the loop below would return after a single step, i.e.
		# start-1unit is already flipped or exact. Then no jump is done,
		# mirroring the old path (this also rules out ~360deg covers that
		# would overshoot by a full lunation).
		lonsun, lonmoon = self.elongLons(tim.jd-delta)
		nm, ready = self.isNewMoon(self.truncDiff(lonsun, lonmoon))
		return nm != newmoonorig or ready

	def jumpBack(self, tim, place, days = 0, mins = 0, secs = 0):
		# Exact integer calendar stepping (no float round-trip), so the
		# landing point lies on the same grid the loops below would visit
		total = days*86400+mins*60+secs
		h, m, s = util.decToDeg(tim.time)
		y, mo, d = tim.year, tim.month, tim.day
		sod = h*3600+m*60+s-total
		backdays, sod = divmod(sod, 86400)
		for i in range(-backdays):
			y, mo, d = util.decrDay(y, mo, d)
		if y < 1:
			y = 1
		h, m, s = sod//3600, (sod%3600)//60, sod%60
		return chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)


	def getDateHour(self, tim, place, newmoonorig):
		lonsun, lonmoon = self.elongLons(tim.jd)
		diff0 = self.truncDiff(lonsun, lonmoon)
		if not self.startsPastFlip(tim, newmoonorig, 1.0/24.0):
			cover = self.coverBack(diff0, newmoonorig)
			days = int(cover/self.MAXELONGDAY)-1 # stop 1 day short: truncation noise is only seconds
			if days > 0:
				tim = self.jumpBack(tim, place, days = days)
		while True:
			h, m, s = util.decToDeg(tim.time) 
			y, mo, d = tim.year, tim.month, tim.day
			h -= 1
			if h < 0:
				h = 23	
				y, mo, d = util.decrDay(y, mo, d)
				if y == 0:
					y = 1
					tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
					return True, tim, True

			tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)

			lonsun, lonmoon = self.elongLons(tim.jd)
			diff = self.truncDiff(lonsun, lonmoon)

			newmoon, ready = self.isNewMoon(diff)
			if newmoon != newmoonorig or ready:
				return True, tim, ready

		return False, tim


	def getDateMinute(self, tim, place, newmoonorig):
		h, m, s = util.decToDeg(tim.time) 
		y, mo, d = tim.year, tim.month, tim.day
		h += 1
		if h > 23:
			h = 0	
			y, mo, d = util.incrDay(y, mo, d)

		tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)

		lonsun, lonmoon = self.elongLons(tim.jd)
		diff0 = self.truncDiff(lonsun, lonmoon)
		if not self.startsPastFlip(tim, newmoonorig, 1.0/1440.0):
			cover = self.coverBack(diff0, newmoonorig)
			mins = int(cover/self.MAXELONGMIN)-2 # stop 2 min short
			if mins > 0:
				tim = self.jumpBack(tim, place, mins = mins)

		while True:
			h, m, s = util.decToDeg(tim.time) 
			y, mo, d = tim.year, tim.month, tim.day
			y, mo, d, h, m = util.subtractMins(y, mo, d, h, m, 1)
			if y == 0:
				y = 1
				tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
				return True, tim, True

			tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)

			lonsun, lonmoon = self.elongLons(tim.jd)
			diff = self.truncDiff(lonsun, lonmoon)

			newmoon, ready = self.isNewMoon(diff)
			if newmoon != newmoonorig or ready:
				return True, tim, ready

		return False, tim


	def getDateSecond(self, tim, place, newmoonorig):
		h, m, s = util.decToDeg(tim.time) 
		y, mo, d = tim.year, tim.month, tim.day
		y, mo, d, h, m = util.addMins(y, mo, d, h, m, 1)

		tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)

		lonsun, lonmoon = self.elongLons(tim.jd)
		diff0 = self.truncDiff(lonsun, lonmoon)
		if not self.startsPastFlip(tim, newmoonorig, 1.0/86400.0):
			cover = self.coverBack(diff0, newmoonorig)
			secs = int(cover/self.MAXELONGSEC)-8 # stop 8 s short
			if secs > 0:
				tim = self.jumpBack(tim, place, secs = secs)

		while True:
			h, m, s = util.decToDeg(tim.time) 
			y, mo, d = tim.year, tim.month, tim.day
			y, mo, d, h, m, s = util.subtractSecs(y, mo, d, h, m, s, 1)
			if y == 0:
				y = 1
				tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)
				return True, tim, True

			tim = chart.Time(y, mo, d, h, m, s, False, tim.cal, chart.Time.GREENWICH, True, 0, 0, False, place, False)

			lonsun, lonmoon = self.elongLons(tim.jd)
			diff = self.truncDiff(lonsun, lonmoon)

			newmoon, ready = self.isNewMoon(diff)
			if newmoon != newmoonorig or ready:
				return True, tim, ready

		return False, tim




