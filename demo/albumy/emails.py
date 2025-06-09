def send_confirm_email(user,token,to=None):
    send_mail(subject='Email Confirm',to=to or user.email,template='emails/confirm',user=user,token=token)
    