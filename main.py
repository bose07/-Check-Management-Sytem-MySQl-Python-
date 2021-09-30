unformatedDate = str('06-06-2021')
unformatedDate = unformatedDate.split('-')
passDate = {unformatedDate[2] + '-' + unformatedDate[1] + '-' + unformatedDate[0]}
passDate=str(passDate)

print("%s"%passDate[2:12])