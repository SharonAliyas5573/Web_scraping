import requests



def update_proxies():

    api_url =  'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&google=true'
    response = requests.get(api_url)

    if response.status_code == 200:
        proxy_list = response.json()
        proxies = {}
        for proxy in proxy_list['data']:
            url = f"{proxy['protocols'][0]}://{proxy['ip']}:{proxy['port']}"
            proxies[url] = None
        return proxies
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        
def proxy_request(target_url):
    proxies= update_proxies()



    # check if each proxy is working or not
    for proxy in proxies:
        try:
            response = requests.get(target_url, proxies={proxy: None}, timeout=100)
            if response.status_code == 200:
                
                return response
            else:
                pass
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    
    # if all proxies failed, update proxies and try again
    print("All proxies failed. Updating proxies and trying again...")
    proxies = update_proxies()
    return proxy_request(target_url, proxies)



