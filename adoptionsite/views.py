import os
import redis

# import pandas
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pymongo

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from adoptionsite.models import Animal, CartItem

login_ids = [ 'pencil', 'flower', 'icecream', 'basketball', 'orange', 'placeholder' ]

# Initial load of animals
available_animals = []

# Start load from CSV
# REMOVE THIS BLOCK WHEN READING FROM MONGO DB INSTEAD OF CSV
# Load animals from CSV
# animals_df = pandas.read_csv('animals.csv', index_col='Id')

# for animal in animals_df.itertuples():
#     available_animals.append(Animal(id=animal.Index, name=animal.Name, description=animal.Description, age=animal.Age))
# End load from CSV

# Start Key Vault
# Uncomment this and fill out the details to integrate with Azure Key Vault
# You will need to set environment variables for Django__KeyVaultName and Django__Debug
# as part of this task too, don't forget to tidy up any duplicate declarations!
# key_vault_name = os.environ["Django__KeyVaultName"]
key_vault_name = "kv-oss-taa"
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

# See here for more information https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential
credential = DefaultAzureCredential()
key_vault_client = SecretClient(vault_url=key_vault_uri, credential=credential)
# End Key Vault

# Start Mongo DB
# Uncomment this and fill in the details to load the animals from Mongo DB
# Don't forget to remove the code above that is no longer required and the pandas
# package can also be removed from the requirements.txt file
# mongo_db_connection_string = key_vault_client.get_secret('MONGODB-ConnectionString').value
mongo_db_connection_string = key_vault_client.get_secret('MongoConnectionString').value
mongo_client = pymongo.MongoClient(mongo_db_connection_string)

# This is your database name (TAA_Portal)
mongo_db = mongo_client.TAA_Portal

# This is your collection name (AvailableAnimals)
mongodb_animals = mongo_db.AvailableAnimals

# MAKE SURE TO REMOVE THE LOAD FROM CSV BLOCK ABOVE
for animal in mongodb_animals.find():
    available_animals.append(Animal(id=animal['_id'], name=animal['name'], description=animal['description'], age=animal['age']))
# End Mongo DB


cart_items = [
    CartItem(id=0, quantity=0, name=available_animals[0].name),
    CartItem(id=1, quantity=0, name=available_animals[1].name),
    CartItem(id=2, quantity=0, name=available_animals[2].name),
    CartItem(id=3, quantity=0, name=available_animals[3].name)
]


r = redis.StrictRedis(host='redis-oss.redis.cache.windows.net',
        port=6380, db=0, password='aUQKrGIKJEdEMrq8WKHFFVDXmrhTU2mMIAzCaHwNOE8=', ssl=True)

r.set("test", "okkkkkk")

def index(request):
    available_animals = []
    for animal in mongodb_animals.find():
        available_animals.append(Animal(id=animal['_id'], name=animal['name'], description=animal['description'], age=animal['age']))

    context = {
        'available_animals': available_animals
    }

    return render(request, 'adoptionsite/index.html', context)

def cart(request):
    context = {
        'cart_items': cart_items
    }

    return render(request, 'adoptionsite/cart.html', context)

def login(request):
    context = {
        'login_ids': login_ids
    }

    return render(request, 'adoptionsite/login.html', context)

def logout(request):
    return render(request, 'adoptionsite/logout.html')

def perform_login(request):
    provided_username = request.POST['AvatarId']
    provided_password = request.POST.get('password')

    user = authenticate(request, username=provided_username, password=provided_password)

    if user is not None:
        auth_login(request, user)

        return redirect('Index')
    else:
        context = {
            'login_ids': login_ids,
            'error_message': 'Invalid username or password.'
        }

        return render(request, 'adoptionsite/login.html', context)

def adjust_cart_item_quantity(request, item_id):
    cart_item = next((item for item in cart_items if item.id == item_id))
    action = request.POST['action']

    if action == "increment":
        cart_item.increment()
    else:
        cart_item.decrement()

    return redirect('Cart')
