# generate group files given IPs and team numbers

groupname = "cloud"
hosts = ["10.X.2.2", "10.X.2.3", "10.X.2.5"]
teams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

ips = []

for host in hosts:
    for t in teams:
        new_ip = host.replace("X", str(t))
        ips.append(new_ip)

outf = groupname + ".group"
f= open(outf, 'w+')
for i in ips:
    wi = str(i) + "\n"
    f.write(wi)
f.close()

