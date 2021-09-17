ignore_role_names = [
    'modder', 
    'mode', 
    'bot', 
    'embed generator', 
    'invitelogger', 
    'operator', 
    'moderator', 
    'vip', 
    'mod', 
    'support', 
    'helper', 
    'developer',
    'admin', 
    'staff', 
    'epic', 
    'emperor', 
    'management'
    'partner', 
    'sáng lập', 
    'điều hành', 
    'server', 
    'quản lý', 
    'hỗ trợ', 
    'ban ngành', 
    'boots', 
    'pc', 
    'booster', 
    
],

checked_keys =  [
    'mod', 
    'modder', 
    'patron', 
    'bot', 
    'embed generator', 
    'invitelogger', 
    'operator', 
    'moderator', 
    'vip', 
    'mod', 
    'support', 
    'helper', 
    'developer', 
    'admin', 
    'staff', 
    'epic', 
    'emperor', 
    'management', 
    'partner', 
    'sáng lập', 
    'điều hành', 
    'server', 
    'quản lý', 
    'hỗ trợ', 
    'ban ngành', 
    'booster', 
]

# print(checked_keys)

def check_conclude_key(role_name): 
    for key in checked_keys: 
        if key in role_name.lower(): 
            return True

    return False 

def check_key(role_name): 
    for key in ignore_role_names: 
        if key == role_name.lower(): 
            return True
    return False