from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm  

class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect("contact:contact")  
        return render(request, self.template_name, {'form': form})
