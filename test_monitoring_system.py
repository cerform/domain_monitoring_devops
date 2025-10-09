import time
from MonitoringSystem import MonitoringSystem as ME
from DomainManagementEngine import DomainManagementEngine as DME

dme = DME()
me = ME()

users = [f"test{i}" for i in range(1,12)]

# users_domains = {}
# for user in users: 
#     users_domains[user] = dme.load_user_domains(user)

for user in users:
    start = time.time()
    me.scan_user_domains(username=user)
    end = time.time()
    print(f"{user}'s domains check ended in {end-start:.2f} Seconds.")