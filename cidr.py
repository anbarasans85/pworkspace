prefix = 0
netmask = str()
octet_count = 0
for i in range(0, (prefix/8)):
    netmask = netmask + '255' + '.'
    octet_count += 1
if prefix % 8 != 0:
    netmask = netmask + str(0xff & (0xff << (8 - (prefix % 8)))) + '.'
    octet_count += 1
for j in range(0, 4 - octet_count):
    netmask = netmask + '0' + '.'

print netmask.strip('.')
