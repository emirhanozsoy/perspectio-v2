from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.http import JsonResponse

# Create your views here.
def homepage(request):

    print(request.POST)
    if request.method == 'POST' and request.POST.get("send"):
        print('hey')
        message= get_template('homepage/email_template.html').render({'name':request.POST.get("name")})
        # plain_message = strip_tags(html_message)
        msg = EmailMessage(
                'Thank you for your email',
                message,
                'info@perspect-io.com',
                [request.POST.get("email")],
            )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

        # message= get_template('homepage/email_template.html').render({'name':request.POST.get("name")})
        # plain_message = strip_tags(html_message)
        msg2 = EmailMessage(
                request.POST.get("subject"),
                request.POST.get("message"),
                'info@perspect-io.com',
                ['emirhan.ozsoy@gmail.com'],
            )
        # msg.content_subtype = "html"  # Main content is now text/html
        msg2.send()

        # send_mail('hello',plain_message,'info@perspect-io.com',['emirhan.ozsoy@gmail.com'],fail_silently=False)

        return JsonResponse({'success': True})

    

    return render(request,'homepage/homepage.html')