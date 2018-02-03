def return_nav_html(para=False, username='null'):
    string = r'''
            <li></li>     
            <li><a data-toggle="modal" data-target="#log">管理员登录</a></li>
            '''
    if para == True:
        string = r'''
                 <li id="username"><a>管理员: ''' + username + '''</a></li>     
                 <li><a href="{% url 'WQPS:user_logout' %}">[注销]</a></li>
                 '''
    return string