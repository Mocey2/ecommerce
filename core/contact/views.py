from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ContactHeader, ContactInfo, ContactMessage


def contact_view(request):
    header = ContactHeader.objects.first()
    contact_info = ContactInfo.objects.first()  # il n'y en aura qu'un seul

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        if nom and email and sujet and message:
            ContactMessage.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message
            )
            messages.success(request, "Votre message a été envoyé avec succès.")
            return redirect('contact')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, "contact/contact.html",
                  {
                      "header": header,
                      'contact_info': contact_info,
                  })