import datetime
import time
import logging
import socket
import psutil

from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

def get_ip_address(ifname):
    # Get all network interfaces
    ifaces = psutil.net_if_addrs()
    # Look for the specified interface
    for iface, addrs in ifaces.items():
        if iface == ifname:
            # Look for the first IPv4 address
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    return addr.address
    # If the interface is not found
    return None

while True:
    try:
        epd = epd2in13_V2.EPD() # get the display

        iface = "wlan0" #which interface IP to get
        ip_address = get_ip_address(iface)
        cpu_percent = psutil.cpu_percent(interval=1)
        mem_info = psutil.virtual_memory()
        mem_percent = mem_info.percent
        disk_info = psutil.disk_usage("/")
        disk_percent = disk_info.percent
        hostname = socket.gethostname()
        #Time check
        currtime = datetime.datetime.now()
        now = datetime.datetime.now()
        timeam = now.strftime("%p")
        timehour = currtime.hour
        timehour = str(timehour)
        timemin = currtime.minute
        timemin = str(timemin)
        if len(timemin) < 2:
            timemin = "0" + timemin

        epd.init(epd.FULL_UPDATE)
        title = ImageFont.truetype("./Font.ttc", 18)
        font = ImageFont.truetype("./Font.ttc", 12)
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        # clear screen and start writing text at x,y positions


        draw = ImageDraw.Draw(image)
        draw.text((10,10), "Time: "+timehour+":"+timemin+" "+timeam, font = title, fill = 0)
        draw.text((10,30), "Hostname: "+hostname, font = title, fill = 0)
        if ip_address:
            draw.text((10,50), "IP Address: "+ip_address, font = title, fill = 0)    
        else:
            draw.text((10,50), "No IP Address: ", font = title, fill = 0)
        draw.text((10,75), "CPU:"+str(cpu_percent)+"%", font = font, fill = 0)
        draw.text((70,75), "MEM:"+str(mem_percent)+"%", font = font, fill = 0)
        draw.text((140,75), "DSK:"+str(disk_percent)+"%", font = font, fill = 0)
        epd.display(epd.getbuffer(image.rotate(180)))
        epd.sleep()
        time.sleep(500)

    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        #epd2in13_V2.epdconfig.module_exit()
        epd.init(epd.FULL_UPDATE)           # initialize the display
        epd.Clear(0xFF)          # clear screen
        exit()