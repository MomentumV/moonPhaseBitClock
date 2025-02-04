
import math

ephemeris = {
    # 'terms' : 20, Each of the longitude parameters have 20 terms. These are taken from https://github.com/pedrokkrause/fourier_ephem
    'lon_amp' : [\
    2.0997114145913383, 0.058788819732109025, 0.021817807823316257, 0.015287461678069016, 0.05704928918395102, \
    1.274022543400498, 0.04088947470233743, 0.03480907580344298, 6.288866525864952, 0.03038311209712805, \
    0.008553210965104922, 0.045749613060558324, 0.6583238862729489, 0.0067867178305394665, 0.21362889970023194, \
    0.11439054914258501, 0.010668730644463246, 0.05332142314318798, 0.010038139997356752, 0.012530924996523632],
    'lon_omega' : [\
    0.017201958018643045, 0.030516812233724676, 0.03440384179284957, 0.03625385094011172, 0.18030842801487001, \
    0.19751028046764654, 0.21082531611323058, 0.21276765085018443, 0.22802714563071028, 0.24522923972952337, \
    0.3950207554073134, 0.4083356187778078, 0.4255374274835673, 0.44274080680761646, 0.45605429838949113, \
    0.46179141433928894, 0.6230477436021405, 0.6535647361095923, 0.6840814350677442, 0.6898185676295449],
    'lon_phases' : [\
    3.089604216647668, 1.1899836208633094, 3.032002167838634, -2.4738768799094597, 0.5442551956665871, \
    0.49595791597236416, -1.4071829419118291, 2.696913578318282, -1.4571943878878129, -4.655907951124683, \
    0.9888568957693797, -0.9144471671920004, -0.9613016042428135, 2.073545293143804, -2.9146531404270615, \
    2.8430869974361563, -0.46750483657955993, -2.424386739471904, 1.9115975754293626, 1.3857751954942001]
    }

def excelDate(t):
    """take seconds since 1970, return excel day as floating point of days since Dec 30, 1899"""
    offset = 25569  # days between excel epoch and 1970
    addition = t / (60 * 60 * 24) # fractional days in 1970 epoch
    return offset+addition

def dot(list1, list2):
    return sum([i*j for (i,j) in zip(list1,list2)])

def phase(day):
    temp = [math.sin(day * omega + phase) for (omega,phase) in zip(ephemeris['lon_omega'],ephemeris['lon_phases'])]
    # dot product of lon_amp and the vector constructed above
    correction = dot(ephemeris['lon_amp'],temp)
    angle = correction + 360/29.530589 *  day - 262827.5235067
    percent = (angle % 360)/360
    return percent
