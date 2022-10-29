import time
from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request_async import EventRequestAsync
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.api import FacebookAdsApi




async def fire_fb_pixel(access_token, pixel_id,url, ip_address = None, fname = None,lname = None,email=  None,phone = None,user_agent =None):
    FacebookAdsApi.init(access_token=access_token)
    user_data = UserData(client_ip_address=ip_address,email = email, phone = phone,last_name=lname,first_name=fname,client_user_agent = user_agent)
    event = Event(
        event_source_url = url,
        event_name="Lead",
        event_time=int(time.time()),
        user_data=user_data,
        #custom_data=CustomData(value=conversion_value,currency="USD"),
        action_source=ActionSource.WEBSITE
    )
    event_request_async = EventRequestAsync(events=[event], pixel_id=pixel_id)
    return await event_request_async.execute()


if __name__ =="__main__":
    import asyncio

    pixel_id = '612226083918432'
    access_token = 'EAADoycsKvREBADZCRf0pOShuka5a2mrma8w9TP3hDhd7P6PwNNXktkFVtcnVXsxYroQwesx84aqjOkyxqhjXiPUG5lqcXZCtGG7krGxjZACKyiER78rqBH0gHaO7XuC9NdMu7ZA4qLDiC8daHEMKW89jiaHpEo49ZCKJ5ZBaDFZBbJDtVJKqVzwX31l7X6aRVgZD'
    url = 'https://tylenolautism.consumerinjurysettlements.com'

    leads = [
        {
            'fname':"Kaitlyn",
            'lname':"Moyer",
            "email":"KateMoyer22@gmail.com",
            "phone":"5732024288",
            "ip_address":"166.196.114.61",
            "url":url,
        },
        {
            'fname': "Sophie",
            'lname': "Umoru",
            "email": "Sofiabdul@gmail.com",
            "phone": "8322311434",
            "ip_address": "98.196.75.7",
            "url": url,
        },
    ]
    for l in leads:
        r = asyncio.run(fire_fb_pixel(access_token = access_token,pixel_id = pixel_id,
                                      url = url,ip_address = l['ip_address'],
                                      fname = l['fname'],
                                      lname = l['lname'],
                                      email = l['email'],
                                      phone = l['phone']
                                      ))
        print(r)