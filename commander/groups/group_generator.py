# generate group files given IPs and team numbers

groupname = "team15"
hosts = ["10.X.1.10", "10.X.1.20", "10.X.1.30", "10.X.2.2", "10.X.2.3", "10.X.2.5"]
teams = [15]

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

