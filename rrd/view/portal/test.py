
import commands
url = "127.0.0.1:3000/lua/get_flows_data.lua?perPage=10"
user = "admin"
psw = "adminadmin"
def get_page_data(url, user, psw, page_num):
    cmd = 'curl -s --cookie "user=%s; password=%s" ' % (user, psw)
    cmd = cmd + '"' + url + '&currentPage=' + str(page_num) +'"'
    print(cmd)
    flows_data = commands.getoutput(cmd)
    return flows_data


print(get_page_data(url, user, psw, 2))