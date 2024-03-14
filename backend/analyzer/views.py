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
        site = request.POST.get('site')
        method = request.POST.get('method')
        offers_amount = int(request.POST.get('offers-amount'))

        if site == 'otodom':
            path = DataFinder.get_path()
            DataFinder.read_data(path)

            request_id = DataFinder.get_request_id(path)
            requester = request.user

            data = DataAnalyzer.analyze_apartments(path, 20 if method == "ai" else offers_amount)
            ai_response = DataAnalyzer.ai_analyzer(data, offers_amount) if method == "ai" else None

            save_otodom_data_to_database(data, request_id, requester, site, method, ai_response)
            print(f"Method: {method} analyzer\nRequest id: {request_id}\nRequester: {requester}")

            return redirect('analysis', request_id=request_id)

    return render(request, "analyzer/analyzer-form.html")


def display_analysis(request, request_id):
    data = OtodomData.objects.get(request_id=request_id)
    offers = data.offers.all()
    print("Offers: ", offers)

    if data.method == 'manual':
        context = {'offers': offers}
        return render(request, "analyzer/manual-analysis.html", context)
    elif data.method == 'ai':
        context = {"data": data}
        return render(request, "analyzer/ai-analysis.html", context)


def save_otodom_data_to_database(data, request_id, requester, site, method, ai_response=None):
    otodom_data = OtodomData.objects.create(request_id=request_id, requester=requester, site=site, method=method,
                                            ai_response=ai_response)

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



