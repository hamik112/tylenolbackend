import time
from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request_async import EventRequestAsync
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.api import FacebookAdsApi




async def fire_fb_pixel(access_token, pixel_id,url, ip_address = None, user_agent=None,fname = None,lname = None,email=  None,phone = None, test_code = None):
    FacebookAdsApi.init(access_token=access_token)
    user_data = UserData(client_ip_address=ip_address,email = email, phone = phone,last_name=lname,first_name=fname)
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
    access_token = 'EAADoycsKvREBAHDDrdoZCqo8JJWcpWZCjrph6rspxmPW4tIbb2w9UbRYTBu8mqn6dQ3r0PXjizcXc3pKKFouM3wlVybThL7GcnEPbVa1MIjbNa6DyR8hJYSCkz2TUD398214fAZAfL1EWjyHQHl6CYZB4Y85OogBhZA6rLwLVkDpw9RChHzv8BmEKklqhnZCoZD'
    url = 'https://tylenolautism.consumerinjurysettlements.com'

    leads = [
        {
            'fname': "Naqqasha",
            'lname': "Syed",
            "ip_address": "43.247.121.22",
            "email": "naqqasha.syed@hotmail.com",
            "phone": "12533398199"

        },
        {
            'fname': "Marobeny",
            'lname': "De los Santos",
            "ip_address": "68.196.222.70",
            "email": "Marobenyhernandez@gmail.com",
            "phone": "19293511457"

        }

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