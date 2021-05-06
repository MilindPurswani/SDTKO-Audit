from Cloudflare import *
from Notifications import *
from NucleiWrapper import *
from Report import *
from TMOWrapper import *


if __name__ == '__main__':
    domain_name = "milindpurswani.com"
    notify_bot = Notifications()
    notify_bot.send_debug_notification("Starting new subdomain audit at "+str(datetime.datetime.now()))
    print("[*] Starting SDTKO Audit")
    cloudflare = Cloudflare()
    data = cloudflare.get_cname_domains(domain_name)
    print("[*] Running Nuclei Scanner")
    nuclei_wrapper = NucleiWrapper()
    nuclei_result = nuclei_wrapper.check_takeover(data)
    if len(nuclei_result) == 0:
        print("[*] Nuclei scan completed no results found.")
        notify_bot.send_debug_notification("Nuclei scan completed, no results found.")

    print("[*] Running Takemeon Scanner")
    tmo_wrapper = TMOWrapper()
    tmo_result = tmo_wrapper.check_takeover(data)

    if len(tmo_result) == 0:
        print("[*] takemeon scan completed no results found.")
        notify_bot.send_debug_notification("Takemeon scan completed, no results found.")
    nuclei_result.extend(tmo_result)
    if len(nuclei_result) == 0:
        print("[*] No subdomain takeovers found")
        notify_bot.send_debug_notification("SDTKO scan completed, no results found.")
        exit(0)

    for item in nuclei_result:
        notify_bot.send_important_notification("Found Subdomain "+item['sub']+" pointing to "+item['resolution'])
        print("Found Subdomain "+item['sub']+" pointing to "+item['resolution'])
    r = Report(domain_name)
    r.create_report(nuclei_result)
    notify_bot.send_debug_notification("SDTKO scan completed with "+str(len(nuclei_result))+" results.")




