#!/usr/bin/env python
import gcn
import lxml.etree

from twython import Twython

import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style, quantity_support
plt.style.use(astropy_mpl_style)
quantity_support()
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz


################################################################
# special keys
APP_KEY = 'VQUgZXEkV3gkKoNBQYnJwv2Fo'
APP_SECRET = '2sMFx22wSkpNsNNl4heLfra4uIaJuEENiLTnsXy4bhOrl0cUN9'
Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAFU1GwEAAAAAo0QEn52OqoO%2BcvWNGR6zg7VQwL0%3D1swAN6l5Bs98W3jDlGAHiAGOODRO3IymFDvS6eh86oHcKX4Obn'
OAUTH_TOKEN = '4646451566-iIP0vbk49KDbq7mRrjMt8d03PGPhbryWQm47Otj'
OAUTH_TOKEN_SECRET = 'f6uqAzRKR3Yed3cuRz7siTEIz1y5ZZfqmmRpqUeiZBV4j'


################################################################
# open twitter connection
twitter = Twython(  APP_KEY, 
                    APP_SECRET,
                    OAUTH_TOKEN, 
                    OAUTH_TOKEN_SECRET)



####################################
# Define your custom handler here.

@gcn.include_notice_types(
    gcn.notice_types.FERMI_GBM_FIN_POS,   # Fermi GBM localization (final)
    gcn.notice_types.SWIFT_BAT_GRB_POS_ACK,
    gcn.notice_types.SWIFT_XRT_POSITION,
    gcn.notice_types.SWIFT_UVOT_POS)

    

def handler(payload, root):
    # Look up right ascension, declination, and error radius fields.
    pos2d = root.find('.//{*}Position2D')
    ra = float(pos2d.find('.//{*}C1').text)
    dec = float(pos2d.find('.//{*}C2').text)
    radius = float(pos2d.find('.//{*}Error2Radius').text)

    # Print.
    print('New GRB Coordinates! ra = {:g}, dec={:g}, radius={:g}'.format(ra, dec, radius))
    pointing_type = "none"
    for param in root.findall('./What/Param'):
        name = param.attrib['name']
        value = param.attrib['value']
        print('{} = {}'.format(name, value))
        if name == 'Coords_String':
            pointing_type = value





    


    ##############################################################################
    # Set values for obs
    #ra = 177.79
    #dec = 19.94

    from datetime import datetime

    date = datetime.today().strftime('%Y-%m-%d')
    time = date+' 00:00:00' #utc


    ##############################################################################
    # `astropy.coordinates.SkyCoord.from_name` uses Simbad to resolve object
    # names and retrieve coordinates.
    #
    # Get the coordinates of your source:

    source = SkyCoord(ra, dec, unit="deg")

    ##############################################################################
    # Use `astropy.coordinates.EarthLocation` to provide the location
    # and provide utc offset:

    CTMO = EarthLocation(lat=25.9*u.deg, lon=-97.4*u.deg, height=390*u.m)
    utcoffset = -6*u.hour  


    ##############################################################################
    # Find the alt,az coordinates of your source at 100 times evenly spaced between 10pm
    # and 7am EDT:

    midnight = Time(time) - utcoffset
    delta_midnight = np.linspace(-2, 10, 100)*u.hour
    frame_July13night = AltAz(obstime=midnight+delta_midnight,
                              location=CTMO)
    sourcealtazs_July13night = source.transform_to(frame_July13night)


    ##############################################################################
    # Use  `~astropy.coordinates.get_sun` to find the location of the Sun at 1000
    # evenly spaced times between noon on July 12 and noon on July 13:

    from astropy.coordinates import get_sun
    delta_midnight = np.linspace(-12, 12, 1000)*u.hour
    times_July12_to_13 = midnight + delta_midnight
    frame_July12_to_13 = AltAz(obstime=times_July12_to_13, location=CTMO)
    sunaltazs_July12_to_13 = get_sun(times_July12_to_13).transform_to(frame_July12_to_13)


    ##############################################################################
    # Do the same with `~astropy.coordinates.get_moon` to find when the moon is
    # up. Be aware that this will need to download a 10MB file from the internet
    # to get a precise location of the moon.

    from astropy.coordinates import get_moon
    moon_July12_to_13 = get_moon(times_July12_to_13)
    moonaltazs_July12_to_13 = moon_July12_to_13.transform_to(frame_July12_to_13)

    ##############################################################################
    # Find the alt,az coordinates of your source at those same times:

    sourcealtazs_July12_to_13 = source.transform_to(frame_July12_to_13)

    ##############################################################################
    # Make a beautiful figure illustrating nighttime and the altitudes of your source and
    # the Sun over that time:

    plt.plot(delta_midnight, sunaltazs_July12_to_13.alt, color='r', label='Sun')
    plt.plot(delta_midnight, moonaltazs_July12_to_13.alt, color=[0.75]*3, ls='--', label='Moon')
    plt.scatter(delta_midnight, sourcealtazs_July12_to_13.alt,
                c=sourcealtazs_July12_to_13.az, label='GRB Source', lw=4, s=8,
                cmap='viridis')
    plt.fill_between(delta_midnight, 0*u.deg, 90*u.deg,
                     sunaltazs_July12_to_13.alt < -0*u.deg, color='0.5', zorder=0)
    plt.fill_between(delta_midnight, 0*u.deg, 90*u.deg,
                     sunaltazs_July12_to_13.alt < -18*u.deg, color='k', zorder=0)
    plt.colorbar().set_label('Azimuth [deg]')
    plt.legend(loc='upper left')
    plt.xlim(-4*u.hour, 8*u.hour)
    plt.xticks((np.arange(6)*2-4)*u.hour)
    plt.ylim(0*u.deg, 90*u.deg)
    plt.xlabel('Hours from CT Midnight')
    plt.ylabel('Altitude [deg]')
    plt.title("GRB Source" + str(date))
    plt.savefig('/Users/mrd/Documents/CTMO/gcn_updates/' + str(date) +"_"+ str(ra)+"_" + str(dec) + '.png')
    #plt.show()
    plt.close()

    image = '/Users/mrd/Documents/CTMO/gcn_updates/' + str(date) +"_"+ str(ra) + "_" + str(dec) + '.png'
    message = pointing_type + " at \nRA: " + str(ra) + "\nDec: " + str(dec) + "\nRadius: "+str(radius)+"\n" + "\nthis message was sent automatically"  
    
    photo = open(image, 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status=message, media_ids=[response['media_id']])

# Listen for VOEvents until killed with Control-C.
gcn.listen(handler=handler)












