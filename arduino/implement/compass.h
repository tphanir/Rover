// Mode Control (MODE)
const byte qmc5883l_mode_stby = 0x00;
const byte qmc5883l_mode_cont = 0x01;
// Output Data Rate (ODR)
const byte qmc5883l_odr_10hz  = 0x00;
const byte qmc5883l_odr_50hz  = 0x04;
const byte qmc5883l_odr_100hz = 0x08;
const byte qmc5883l_odr_200hz = 0x0C;
// Full Scale Range (RNG)
const byte qmc5883l_rng_2g    = 0x00;
const byte qmc5883l_rng_8g    = 0x10;
// Over Sample Ratio (OSR)
const byte qmc5883l_osr_512   = 0x00;
const byte qmc5883l_osr_256   = 0x40;
const byte qmc5883l_osr_128   = 0x80;
const byte qmc5883l_osr_64    = 0xC0;



double haversine(double lat1, double lon1, double lat2, double lon2) {
  lat1 = radians(lat1);
  lon1 = radians(lon1);
  lat2 = radians(lat2);
  lon2 = radians(lon2);

  double dlat = lat2 - lat1;
  double dlon = lon2 - lon1;

  double a = pow(sin(dlat / 2.0), 2.0)   + cos(lat1) * cos(lat2) * pow(sin(dlon/2.0), 2.0);
  double c = 2.0 * atan2(sqrt(a), sqrt(1 - a));
  double d = c * 6372795.0;

  return d;
}

double bearing(double lat1, double lon1, double lat2, double lon2) {
  lat1 = radians(lat1);
  lon1 = radians(lon1);
  lat2 = radians(lat2);
  lon2 = radians(lon2);

  double dlat = lat2 - lat1;
  double dlon = lon2 - lon1;

	double theta = atan2(sin(dlon) * cos(lat2), cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon));
	double bearing = degrees(theta);

	bearing = ((long)bearing + 360) % 360;
	return bearing;
}

double greatCircle(double lat1, double lon1, double lat2, double lon2)  {
	lat1 = radians(lat1);
  lon1 = radians(lon1);
  lat2 = radians(lat2);
  lon2 = radians(lon2);

	double delta = lon1 - lon2;
  double sdlong = sin(delta);
  double cdlong = cos(delta);
  double slat1 = sin(lat1);
  double clat1 = cos(lat1);
  double slat2 = sin(lat2);
  double clat2 = cos(lat2);
  delta = (clat1 * slat2) - (slat1 * clat2 * cdlong);
  delta = pow(delta, 2);
  delta += pow(clat2 * sdlong, 2);
  delta = sqrt(delta);
  double denom = (slat1 * slat2) + (clat1 * clat2 * cdlong);
  delta = atan2(delta, denom);
  double distanceToTarget =  delta * 6372795;	
	
	return distanceToTarget;
}

double bearing2(double lat1, double lon1, double lat2, double lon2)  {
	lat1 = radians(lat1);
  lon1 = radians(lon1);
  lat2 = radians(lat2);
  lon2 = radians(lon2);

  float dlon = lon2 - lon1;
  float a1 = sin(dlon) * cos(lat2);
  float a2 = sin(lat1) * cos(lat2) * cos(dlon);
  a2 = cos(lat1) * sin(lat2) - a2;
  a2 = atan2(a1, a2);
  if (a2 < 0.0)
  {
    a2 += M_PI * 2;
  }
  double targetHeading = degrees(a2);
  return (long)targetHeading;
}