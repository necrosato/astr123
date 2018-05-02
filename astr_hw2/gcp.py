#!/usr/bin/python3

from math import cos, pi

class globular_cluster:
    def __init__(self, data):
        self.ra_hour = data[0]
        self.ra_min = data[1]
        self.dec_deg = data[2]
        self.dec_min = data[3] if data[2] >= 0 else -data[3]
        self.glat = data[4]
        self.glon = data[5]
        self.distance = data[6]

    def __repr__(self):
        return "rah: " + str(self.ra_hour) + "\nram: " + str(self.ra_min) + "\ndec_deg: " + str(self.dec_deg) + "\ndec_min: " + str(self.dec_min) + "\n"

milky_way_center = globular_cluster([17.0, 45.0, -29.0, 0.5, 0, 0, 0])

def estimate_center_distance(gcs):
    rah_low = 16.0
    ram_low = 45.0
    rah_high = 18.0
    ram_high = 45.0
    dec_deg_low = -34.0
    dec_deg_high = -24.0
    
    gcs_in_range = []
    for gc in gcs:
        if (gc.ra_hour > rah_low or (gc.ra_hour >= rah_low and gc.ra_min >= ram_low)) and (gc.ra_hour < rah_high or (gc.ra_hour <= rah_high and gc.ra_min <= ram_high)):
            if gc.dec_deg >= dec_deg_low and gc.dec_deg <= dec_deg_high:
                gcs_in_range.append(gc)

    #print(gcs_in_range)
    print("\nTotal number of gcs in range: " + str(len(gcs_in_range)))

    count_all = len(gcs_in_range)
    total_hour = 0
    total_dec_deg = 0
    total_dist = 0
    total_dist_better = 0

    for gc in gcs_in_range:
        total_hour += gc.ra_hour
        total_hour += gc.ra_min / 60
        total_dec_deg += gc.dec_deg
        total_dec_deg += gc.dec_min / 60
        total_dist += gc.distance
        d_better = gc.distance * cos(gc.glat * pi / 180) * cos(gc.glon * pi / 180)
        total_dist_better += d_better

    print("Appriximate center (mean): ")
    print("\tRAH: ", end='')
    print(total_hour / count_all)
    print("\tDEC_DEG: ", end='')
    print(total_dec_deg / count_all)
    print("\nDistance to center (simple mean of D): ", end='')
    print("%f kly" % (total_dist / count_all))
    print("\nDistance to center (D * cos(glat) * cos(glon)): ", end='')
    print("%f kly" % (total_dist_better / count_all))
    print()



def print_chart(gcs):
    ra = {}
    dec = {}
    ra_dec = {}
    for i in range(0, 24, 2):
        ra[i] = []
        ra_dec[i] = {}
    for i in range(-90, 90, 15):
        dec[i] = []       
        for j in range(0, 24, 2):
            ra_dec[j][i] = []
    total_hour = 0
    total_dec_deg = 0
    for gc in gcs:
        total_hour += gc.ra_hour
        total_hour += gc.ra_min / 60
        total_dec_deg += gc.dec_deg
        total_dec_deg += gc.dec_min / 60
        ra_hour = gc.ra_hour - (gc.ra_hour % 2)
        ra[ra_hour].append(gc)
        dec_deg = gc.dec_deg - (gc.dec_deg % 15)
        dec[dec_deg].append(gc)
        ra_dec[ra_hour][dec_deg].append(gc)

    print("      ", end='')
    count_all = 0
    for i in range(0, 24, 2):
        i = (i + 12) % 24
        print(format(str(i)+"  ", ">5"), end="")
    print()
    print('_'*66)
    for j in range(75, -105, -15):
        print(format(j, ">3"), end=" |")
        for i in range(0, 24, 2):
            i = (i + 12) % 24
            count = len(ra_dec[i][j])
            count_all += count
            print(format(str(count)+' |', ">5"), end='')
        print() 
        print('_'*66)
    print("\nTotal number of globular_clusters " + str(count_all))
    print("Appriximate center (mean): ")
    print("\tRAH: ", end='')
    print(total_hour / count_all)
    print("\tDEC_DEG: ", end='')
    print(total_dec_deg / count_all)



def main():
    with open('./equatorial_coordinates.txt') as f:
        gcs = []
        line = f.readline().strip()
        while line != '':
            # parse a cluster
            data = line.split()
            for i in range(7):
                data[i] = float(data[i])
            gc = globular_cluster(data)
            gcs.append(gc)
            line = f.readline().strip()

        print_chart(gcs)
        estimate_center_distance(gcs)

if __name__=='__main__':
    main()
