from services.osint import ip_address_checker as iac

ip_address = input("Enter the IP address to investigate: ")
iac.display_osint_info(ip_address)
