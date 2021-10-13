from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ContactForm
from .tasks import send_email_contact


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title', '')
            message = form.cleaned_data.get('message', '')
            email_from = form.cleaned_data.get('email_from', '')

            try:
                send_email_contact.delay(
                    title=title,
                    email_from=email_from,
                    message=message,
                    )
                messages.success(request, 'Thank you! Your message has been sent successfully!')
            except Exception as wrong: # noqa
                messages.error(request, "Oops something went wrong...")

            return redirect('contact_us')
        else:
            messages.error(request, f"FAILED. {request.POST.get('email_from')} -Incorrect email address!")
    else:
        form = ContactForm()

    return render(request, 'contact/contact_form.html', {'form': form, 'Title': 'Contact'})


class ContactUs(FormView):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    success_url = reverse_lazy('contact_us')

    def form_valid(self, form):
        title = form.cleaned_data.get('title', '')
        message = form.cleaned_data.get('message', '')
        email_from = form.cleaned_data.get('email_from', '')
        try:
            send_email_contact.delay(
                title=title,
                email_from=email_from,
                message=message,
                )
            messages.success(self.request, 'Thank you! Your message has been sent successfully!')
        except Exception as wrong: # noqa
            messages.error(self.request, "Oops something went wrong...")
        return super(ContactUs, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f"FAILED. {self.request.POST.get('email_from')} -Incorrect email address!")
        return super().form_invalid(form)
