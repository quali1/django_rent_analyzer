import json

from .rent_analyzer import DataAnalyzer, DataFinder
from .models import Offer, OtodomData

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_page(request):
    return render(request, "analyzer/home.html")


@login_required(login_url="login")
def analyzer_form(request):
    if request.method == "POST":
        print(request.POST)
        site = request.POST.get('site')
        method = request.POST.get('method')
        offers_amount = int(request.POST.get('offers-amount'))

        if site == 'otodom':
            path = DataFinder.get_path()
            DataFinder.read_data(path)

            request_id = DataFinder.get_request_id(path)
            requester = request.user

            data = DataAnalyzer.analyze_apartments(path, offers_amount, method)

            print("Data: ", data)
            print("Request id: ", request_id)

            save_otodom_data_to_database(data, request_id, requester, site, method)
            print("Data saved")

            return redirect('analysis', request_id=request_id)

    return render(request, "analyzer/analyzer-form.html")


def display_analysis(request, request_id):
    data = OtodomData.objects.get(request_id=request_id)
    offers = data.offers.all()
    print("Offers: ", offers)

    return render(request, "analyzer/analysis.html", {'offers': offers})


def save_otodom_data_to_database(data, request_id, requester, site, method):
    otodom_data = OtodomData.objects.create(request_id=request_id, requester=requester, site=site, method=method)

    for offer_data in data:
        offer = Offer.objects.create(
            article_id=offer_data['article_id'],
            price=offer_data['price'],
            price_per_sqm=offer_data['price_per_sqm'],
            district=offer_data['district'],
            rooms=offer_data['rooms'],
            area=offer_data['area'],
            floor=offer_data['floor'],
            link=offer_data['link']
        )

        otodom_data.offers.add(offer)
