from enum import Enum
from math import radians, degrees, sqrt, sin, asin, cos, tan, atan, atan2, pi


EARTH_RADIUS_M  = 6378137.0
EARTH_RADIUS_KM = EARTH_RADIUS_M / 1000.0
EARTH_GRAVITY   = 9.80665


def heading(lat_1: float, lon_1: float, lat_2: float, lon_2: float) -> float:
    '''
    Find the heading (in degrees) between two lat/lon coordinates (dd)
    
    Args:
        lat_1:
            First point's latitude (dd)
        lon_1:
            First point's longitude (dd)
        lat_2:
            Second point's latitude (dd)
        lon_2:
            Second point's longitude (dd)
    
    Returns:
            heading in degrees between point 1 and 2
    '''
    
    deltaLon_r = radians(lon_2 - lon_1)
    lat_1_r    = radians(lat_1)
    lat_2_r    = radians(lat_2)

    x = cos(lat_2_r) * sin(deltaLon_r)
    y = cos(lat_1_r) * sin(lat_2_r) - sin(lat_1_r) * cos(lat_2_r) * cos(deltaLon_r)

    return (degrees(atan2(x, y)) + 360) % 360

def distance(lat_1: float, lon_1: float, lat_2: float, lon_2: float, km: bool=False) -> float:
    '''
    Find the total distance (in km) between two lat/lon coordinates (dd)
    
    Args:
        lat_1:
            First point's latitude (dd)
        lon_1:
            First point's longitude (dd)
        lat_2:
            Second point's latitude (dd)
        lon_2:
            Second point's longitude (dd)
        km:
            Distance units in km, else m
    
    Returns:
            Distance in km between point 1 and 2
    '''
    
    lat_1_rad = radians(lat_1)
    lon_1_rad = radians(lon_1)
    lat_2_rad = radians(lat_2)
    lon_2_rad = radians(lon_2)
    
    d_lat = lat_2_rad - lat_1_rad
    d_lon = lon_2_rad - lon_1_rad
    
    a = (sin(d_lat / 2) ** 2) + cos(lat_1_rad) * cos(lat_2_rad) * (sin(d_lon / 2) ** 2)
    
    if km:
        return 2 * EARTH_RADIUS_KM * atan2(sqrt(a), sqrt(1 - a))
    return  2 * EARTH_RADIUS_M * atan2(sqrt(a), sqrt(1 - a))

def climbAngle(i_lat: float, i_lon: float, f_lat: float, f_lon: float, i_alt: float, f_alt: float) -> float:
    '''
    Finds the climb angle in degrees using the distance between two points and
    the corresponding difference in altitude in m
    
    Args:
        i_lat:
            Initial latitude (dd)
        i_lon:
            Initial longitude (dd)
        f_lat:
            Final latitude (dd)
        f_lon:
            Final longitude (dd)
        i_alt:
            Initial altitude (m)
        i_alt:
            Initial altitude (m)
        f_alt:
            Final altitude (m)
        f_alt:
            Final altitude (m)
    
    Returns:
            Climb angle in degrees
    '''
    
    dist  = distance(i_lat, i_lon, f_lat, f_lon)
    d_alt = f_alt - i_alt

    return degrees(atan(d_alt / dist))

def coord(lat: float, lon: float, dist: float, heading: float, km: bool=False) -> list:
    '''
    Finds the lat/lon coordinates "dist" km away from the given "lat" and "lon"
    coordinate along the given compass "heading"
    
    Args:
        lat:
            First point's latitude (dd)
        lon:
            First point's longitude (dd)
        dist:
            Distance in km the second point should be from the first point
        heading:
            heading in degrees from the first point to the second
        km:
            Distance units in km, else m
    
    Returns:
            Latitude and longitude in DD of the second point
    '''
    
    hdg   = radians(heading)
    lat_1 = radians(lat)
    lon_1 = radians(lon)
    
    if km:
        lat_2 = asin(sin(lat_1) * cos(dist / EARTH_RADIUS_KM) + cos(lat_1) * sin(dist / EARTH_RADIUS_KM) * cos(hdg))
        lon_2 = lon_1 + atan2(sin(hdg) * sin(dist / EARTH_RADIUS_KM) * cos(lat_1), cos(dist / EARTH_RADIUS_KM) - sin(lat_1) * sin(lat_2))
    else:
        lat_2 = asin(sin(lat_1) * cos(dist / EARTH_RADIUS_M) + cos(lat_1) * sin(dist / EARTH_RADIUS_M) * cos(hdg))
        lon_2 = lon_1 + atan2(sin(hdg) * sin(dist / EARTH_RADIUS_M) * cos(lat_1), cos(dist / EARTH_RADIUS_M) - sin(lat_1) * sin(lat_2))
    
    return [degrees(lat_2), degrees(lon_2)]

def orbitHeading(plane_lat: float, plane_lon: float, wpt_lat: float, wpt_lon: float, radius: float=1, clockwise: bool=True, hcMax: float=90, k: float=1) -> float:
    '''
    Finds the heading (in degrees) necessary to orbit a given waypoint
    
    Args:
        plane_lat:
            Plane's latitude (dd)
        plane_lon:
            Plane's longitude (dd)
        wpt_lat:
            Next waypoint's latitude (dd)
        wpt_lon:
            Next waypoint's longitude (dd)
        radius:
            Orbit radius (km) from the waypoint
        clockwise:
            Orbit clockwise, else counter-clockwise
        hcMax:
            Max heading output
        k:
            Path convergence factor (higher values mean faster convergence)
    
    Returns:
            Heading necessary to orbit a given waypoint
    '''
    
    d0    = distance(plane_lat, plane_lon, wpt_lat, wpt_lon, True)
    d     = d0 - radius
    theta = heading(plane_lat, plane_lon, wpt_lat, wpt_lon)
    hc    = -(2 / pi) * hcMax * atan(k * d)

    if clockwise:
        theta = (theta - 90) % 360
        hc *= -1
    else:
        theta = (theta + 90) % 360
    
    return (hc + theta + 360) % 360

def linePathHeading(plane_lat: float, plane_lon: float, wpt_lat: float, wpt_lon: float, wpt_hdg: float, hcMax: float, k: float) -> float:
    '''
    Finds the heading (in degrees) necessary to follow a line to a given
    waypoint
    
    Args:
        plane_lat:
            Plane's latitude (dd)
        plane_lon:
            Plane's longitude (dd)
        wpt_lat:
            Next waypoint's latitude (dd)
        wpt_lon:
            Next waypoint's longitude (dd)
        wpt_hdg:
            Heading of the line to follow
        hcMax:
            Max heading output
        k:
            Path convergence factor (higher values mean faster convergence)
    
    Returns:
            Heading necessary to follow a line to a given waypoint
    '''
    
    h1    = wpt_hdg
    h01   = heading(plane_lat, plane_lon, wpt_lat, wpt_lon)
    theta = (h01 - h1 + 360) %  360
    d0    = distance(plane_lat, plane_lon, wpt_lat, wpt_lon, True)
    dPerp = d0 * tan(radians(theta))
    hc    = -(2 / pi) * hcMax * atan(k * dPerp)
    
    return (h1 - hc + 360) %  360

def acuteAngle(refAngle: float, angle2: float) -> float:
    '''
    Finds the acute heading angle between two given heading angles (all in
    degrees)
    
    Args:
        refAngle:
            Reference heading angle (°)
        angle2:
            Second heading angle (°)
    
    Returns:
            Acute heading angle between two given heading angles (in degrees)
    '''
    
    normRefAngle = 180
    normAngle2   = (angle2 + 180 - refAngle + 360) %  360
    
    return (normAngle2 - normRefAngle) %  360


class point(object):
    def __init__(self):
        self.maxRoll    = 0 # °
        self.minTurnRad = 0 # m
        self.hitRadius  = 0 # m
        
        self.alt     = 0 # m
        self.speed   = 0 # m/s
        self.heading = 0 # °
        self.lat     = 0 # °
        self.lon     = 0 # °
        
        self.rc_lat = 0 # Right Turn Circle lat °
        self.rc_lon = 0 # Right Turn Circle lon °
        self.lc_lat = 0 # Left Turn Circle lat °
        self.lc_lon = 0 # Left Turn Circle lon °
        self.c_lat  = 0 # Selected Turn Circle lat °
        self.c_lon  = 0 # Selected Turn Circle lon °
        self.e_lat  = 0 # Enter/exit lat °
        self.e_lon  = 0 # Enter/exit lon °


class dubin(Enum):
    LSRU = 1 # Left Straight Right Up
    LSRD = 2 # Left Straight Right Down
    RSLU = 3 # Right Straight Left Up
    RSLD = 4 # Right Straight Left Down
    RSRU = 5 # Right Straight Right Up
    RSRD = 6 # Right Straight Right Down
    LSLU = 7 # Left Straight Left Up
    LSLD = 8 # Left Straight Left Down


class nav_frame(object):
    def __init__(self):
        self.path = dubin.LSRU # Dubin path type
        self.ni   = point()    # Current point
        self.nf   = point()    # Next point


class navigator(object):
    def process_frame(self, frame: nav_frame) -> nav_frame:
        self.findMTR(frame.ni)
        self.findMTR(frame.nf)
        
        self.findTurnCenters(frame.ni)
        self.findTurnCenters(frame.nf)
        
        self.findPath(frame)
        
        self.findEPts(frame)

    def findMTR(self, curPoint: point) -> float:
        curPoint.minTurnRad = (curPoint.speed * curPoint.speed) / (EARTH_GRAVITY * tan(radians(curPoint.maxRoll)))

    def findTurnCenters(self, curPoint: point) -> list:
        [curPoint.rc_lat, curPoint.rc_lon] = coord(curPoint.lat, curPoint.lon, curPoint.minTurnRad, (curPoint.heading + 90) % 360)
        [curPoint.lc_lat, curPoint.lc_lon] = coord(curPoint.lat, curPoint.lon, curPoint.minTurnRad, (curPoint.heading - 90) % 360)

    def findPath(self, frame: nav_frame) -> dubin:
        dist_ir = distance(frame.ni.rc_lat, frame.ni.rc_lon, frame.nf.lat, frame.nf.lon)
        dist_il = distance(frame.ni.lc_lat, frame.ni.lc_lon, frame.nf.lat, frame.nf.lon)

        if dist_ir <= dist_il:
            frame.ni.c_lat = frame.ni.rc_lat
            frame.ni.c_lon = frame.ni.rc_lon
        else:
            frame.ni.c_lat = frame.ni.lc_lat
            frame.ni.c_lon = frame.ni.lc_lon
            
        dist_fr = distance(frame.nf.rc_lat, frame.nf.rc_lon, frame.ni.lat, frame.ni.lon)
        dist_fl = distance(frame.nf.lc_lat, frame.nf.lc_lon, frame.ni.lat, frame.ni.lon)
    
        if dist_fr <= dist_fl:
            frame.nf.c_lat = frame.nf.rc_lat
            frame.nf.c_lon = frame.nf.rc_lon
        else:
            frame.nf.c_lat = frame.nf.lc_lat
            frame.nf.c_lon = frame.nf.lc_lon
    
        if dist_ir <= dist_il:
            if dist_fr <= dist_fl:
                if frame.nf.alt >= frame.ni.alt:
                    frame.path = dubin.RSRU
                else:
                    frame.path = dubin.RSRD
            else:
                if frame.nf.alt >= frame.ni.alt:
                    frame.path = dubin.RSLU
                else:
                    frame.path = dubin.RSLD
        else:
            if dist_fr <= dist_fl:
                if frame.nf.alt >= frame.ni.alt:
                    frame.path = dubin.LSRU
                else:
                    frame.path = dubin.LSRD
            else:
                if frame.nf.alt >= frame.ni.alt:
                    frame.path = dubin.LSLU
                else:
                    frame.path = dubin.LSLD

    def findEPts(self, frame: nav_frame) -> list:
    	theta_cc = heading(frame.ni.c_lat, frame.ni.c_lon, frame.nf.c_lat, frame.nf.c_lon)
    	stepSize = 0.001 # °
    	distTol  = 1 # m
    
    	if (frame.path == dubin.LSRU) or (frame.path == dubin.LSRD):
    		theta_i = theta_cc
    		theta_f = (theta_i + 180, 360)
    
    		[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    		[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    		test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    		[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)
    
    		dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
    		while dist > distTol:
    			theta_i = (theta_i + stepSize) % 360
    			theta_f = (theta_i + 180) % 360
    
    			[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    			[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    			test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    			[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)
    
    			dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    		
    		frame.ni.e_lat = p0_lat
    		frame.ni.e_lon = p0_lon
    
    		frame.nf.e_lat = p2_lat
    		frame.nf.e_lon = p2_lon
    	
    	elif (frame.path == dubin.RSLU) or (frame.path == dubin.RSLD):
    		theta_i = theta_cc
    		theta_f = (theta_i + 180) % 360
    
    		[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    		[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    		test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    		[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)
    
    		dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
    		while dist > distTol:
    			theta_i = (theta_i - stepSize) % 360
    			theta_f = (theta_i + 180) % 360
    
    			[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    			[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    			test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    			[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)
    
    			dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    		
    		frame.ni.e_lat = p0_lat
    		frame.ni.e_lon = p0_lon
    
    		frame.nf.e_lat = p2_lat
    		frame.nf.e_lon = p2_lon
    	
    	elif (frame.path == dubin.RSRU) or (frame.path == dubin.RSRD):
    		if frame.ni.minTurnRad == frame.nf.minTurnRad:
    			[frame.ni.e_lat, frame.ni.e_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, (theta_cc - 90) % 360)
    			[frame.nf.e_lat, frame.nf.e_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, (theta_cc - 90) % 360)
    		
    		elif frame.ni.minTurnRad > frame.nf.minTurnRad:
    			theta_i = (theta_cc - 90) % 360
    			theta_f = theta_i
    
    			[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    			[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    			test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    			[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)
    
    			dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
    			while dist > distTol:
    				theta_i = (theta_i + stepSize) % 360
    				theta_f = theta_i
    
    				[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    				[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    				test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    				[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)
    
    				dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
    			frame.ni.e_lat = p0_lat
    			frame.ni.e_lon = p0_lon
    
    			frame.nf.e_lat = p2_lat
    			frame.nf.e_lon = p2_lon
    		
    		else:
    			theta_i = theta_cc
    			theta_f = theta_i
    
    			[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    			[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    			test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    			[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)
    
    			dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
    			while dist > distTol:
    			
    				theta_i = (theta_i - stepSize) % 360
    				theta_f = theta_i
    
    				[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    				[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    				test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    				[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i + 90) % 360)
    
    				dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    			
    			frame.ni.e_lat = p0_lat
    			frame.ni.e_lon = p0_lon
    
    			frame.nf.e_lat = p2_lat
    			frame.nf.e_lon = p2_lon
                
    	elif (frame.path == dubin.LSLU) or (frame.path == dubin.LSLD):
    		if frame.ni.minTurnRad == frame.nf.minTurnRad:
    			[frame.ni.e_lat, frame.ni.e_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, (theta_cc + 90) % 360)
    			[frame.nf.e_lat, frame.nf.e_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, (theta_cc + 90) % 360)
                
    		elif frame.ni.minTurnRad > frame.nf.minTurnRad:
    			theta_i = (theta_cc + 90) % 360
    			theta_f = theta_i
    
    			[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    			[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    			test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    			[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)
    
    			dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
    			while dist > distTol:
    				theta_i = (theta_i - stepSize) % 360
    				theta_f = theta_i
    
    				[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    				[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    				test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    				[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)
    
    				dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    			
    			frame.ni.e_lat = p0_lat
    			frame.ni.e_lon = p0_lon
    
    			frame.nf.e_lat = p2_lat
    			frame.nf.e_lon = p2_lon
    		
    		else:
    			theta_i = (theta_cc + 90) % 360
    			theta_f = theta_i
    
    			[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    			[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    			test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    			[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)
    
    			dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
    			while dist > distTol:
    				theta_i = (theta_i + stepSize) % 360
    				theta_f = theta_i
    
    				[p0_lat, p0_lon] = coord(frame.ni.c_lat, frame.ni.c_lon, frame.ni.minTurnRad, theta_i)
    				[p2_lat, p2_lon] = coord(frame.nf.c_lat, frame.nf.c_lon, frame.nf.minTurnRad, theta_f)
    
    				test_pt_dist = distance(p0_lat, p0_lon, p2_lat, p2_lon)
    				[p1_lat, p1_lon] = coord(p0_lat, p0_lon, test_pt_dist, (theta_i - 90) % 360)
    
    				dist = distance(p1_lat, p1_lon, p2_lat, p2_lon)
    
    			frame.ni.e_lat = p0_lat
    			frame.ni.e_lon = p0_lon
    
    			frame.nf.e_lat = p2_lat
    			frame.nf.e_lon = p2_lon










