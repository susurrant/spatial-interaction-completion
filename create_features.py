
import csv

with open('data/fn_1km.csv', 'w', newline='') as rf:
    sheet = csv.writer(rf, delimiter=',')
    #sheet.writerow(['ogid', 'dgid', 'm'])
    with open('data/pt_fn_vertices.txt', 'r') as f:
        f.readline()
        i = 0
        line = f.readline().strip()
        co = []
        while line:
            d = line.split(',')
            co.append(d[3][:10])
            co.append(d[4][:9])
            i += 1
            if i == 5:
                sheet.writerow(co[:-2])
                co = []
                i = 1
            line = f.readline().strip()


grid = {}
with open('data/pt_fn_cen.txt', 'r') as f:
    f.readline()
    line = f.readline().strip()
    while line:
        d = line.split(',')
        grid[d[1]] = (d[2][:10], d[3][:9])
        line = f.readline().strip()

with open('data/flow_30.csv', 'w', newline='') as rf:
    sheet = csv.writer(rf, delimiter=',')
    #sheet.writerow(['ogid', 'dgid', 'm'])
    with open('data/taxi_1km_t30.txt', 'r') as f:
        f.readline()
        line = f.readline().strip()
        while line:
            d = line.split(',')
            sheet.writerow([grid[d[0]][0], grid[d[0]][1], grid[d[2]][0], grid[d[2]][1]])
            line = f.readline().strip()