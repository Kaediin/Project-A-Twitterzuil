from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect

import TwitterZuil.db_utils as db
import TwitterZuil.weather_api as weather

MASTERPASSWORD = 'KaedinSchouten'

# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def tweet_page(request):
    return render(request, 'tweet_service.html', {})


def send_tweet(request):
    msg = request.POST.get('content-tweet')
    print(len(msg))
    username = request.POST.get('username')
    if username is None or username == "":
        username = "Anonymous"

    db.tweet_message(msg, username)

    if request.method == "POST":
        return HttpResponseRedirect("/Tweet")
    return render(request, 'tweet_service.html', {})


def review_tweet(request):
    naam = request.POST.get('moderator_name')
    password = request.POST.get('moderator_password')
    moderator = db.getModeratorByName(naam, password)
    if moderator is not None:
        tweet = db.getTweetToBeReviewed()

        return render(request, 'review_tweets.html', {
            'tweet': tweet,
            'moderator': moderator
        })

    messages.info(request, 'Invalid credentials')
    print('invalid credentials')
    return HttpResponseRedirect("/Aanmelden-Moderator")


def aanmelden_moderator(request):
    return render(request, 'aanmelden_moderator.html', {})


def handle_review_tweet(request):
    review = request.POST.get('review_score')
    tweet_id = request.POST.get('tweet_id')
    remark = request.POST.get('remark')
    moderator = request.POST.get('moderator')

    if review == 'accept':
        msg = request.POST.get('message')
        db.post_tweet(msg, tweet_id)
    elif review == 'reject':
        print('rejected')
        db.reject_tweet(tweet_id, remark, moderator)

    return review_tweet(request)


def scherm_aanmaken(request):
    return render(request, 'scherm_toevoegen.html', {})


def success_page(request, path, text):
    render(request, path, {
        'text': text
    })


def scherm_toevoegen(request):
    location = request.POST.get('locatie_scherm')
    name = request.POST.get('naam_scherm')
    master_password = request.POST.get('masterpassword')
    if isCorrectPassword(master_password):
        result = db.add_scherm(name, location)
        if result:
            return render(request, 'success_page.html', {
                'text': 'Uw scherm wordt toegevoegd.',
            })
        else:
            messages.info(request, 'Invalid city name')
    else:
        messages.info(request, 'Invalid password')

    return HttpResponseRedirect("/Scherm-Aanmaken")




def scherm_kiezen(request):
    schermen = db.getAllSchermen()
    return render(request, 'scherm_kiezen.html', {
        'schermen': schermen
    })


def scherm_weergeven(request, id):
    scherm = db.getSchermById(id)
    print('Scherm is opgehaald')
    tweet = db.getTweetsToDisplay(scherm)
    print('Tweet is opgehaald')
    weer = weather.getWeather(scherm.locatie)
    print('Weer is opgehaald')
    show_weather = tweet is None

    return render(request, 'scherm_weergeven.html', {
        'scherm': scherm,
        'tweet': tweet,
        'show_weather': show_weather,
        'weer': weer,
    })


def moderator_aanmaken(request):
    return render(request, 'moderator_toevoegen.html', {})


def moderator_toevoegen(request):
    master_pass = request.POST.get('masterPassword_new_moderator')
    password = request.POST.get('wachtwoord_new_moderator')
    firstname = request.POST.get('firstname_new_moderator')
    infix = request.POST.get('infix_new_moderator')
    lastname = request.POST.get('lastname_new_moderator')

    if master_pass != MASTERPASSWORD:
        messages.info(request, 'Incorrect master-password')
        return HttpResponseRedirect("/Aanmaken-Moderator")

    result = db.createNewModerator(firstname, infix, lastname, password)
    if not result:
        messages.info(request, 'User already exists')
        print('invalid name')
        return HttpResponseRedirect("/Aanmaken-Moderator")

    return render(request, 'success_page.html', {
        'text': 'Uw moderator account wordt aangemaakt.',
    })


def isCorrectPassword(password):
    return MASTERPASSWORD == password


def scherm_verversen(request, id):
    scherm = db.getSchermById(id)
    print('Scherm is opgehaald')
    tweet = db.getTweetsToDisplay(scherm)
    print('Tweet is opgehaald')
    weer = weather.getWeather(scherm.locatie)
    print('Weer is opgehaald')
    show_weather = tweet is None

    return render(request, 'scherm_weergeven.html', {
        'scherm': scherm,
        'tweet': tweet,
        'show_weather': show_weather,
        'weer': weer,
    })