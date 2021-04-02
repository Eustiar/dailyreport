# HITSZ哈小深每日上报
哈尔滨工业大学（深圳）每日上报自动填写脚本
<br><br>
需求`schedule`和`requests`库。
<br><br>
使用你的学号和密码替换userdata文件中的`username` 和 `password`
<br><br>
`python dailyreport_xg.py` 即可，修改代码中的`work_schedule`函数中的时间可以更改每日上报的时间，配合tmux或者supervisor等使用更佳。
<br><br>
可以自行配置yagmail、wxpusher等库通过邮件或微信通知自己填报是否完成。
<br><br>
代码中注释掉的部分（一共十行，分散在不同位置）就是用yagmail实现的发送邮件，如果使用，需要取消注释，并在userdata的第三行和第四行分别写上邮箱和授权码（详情百度）