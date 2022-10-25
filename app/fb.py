import time
from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request_async import EventRequestAsync
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.api import FacebookAdsApi




async def fire_fb_pixel(access_token, pixel_id,url, ip_address, user_agent,email,phone, test_code = None):
    FacebookAdsApi.init(access_token=access_token)
    user_data = UserData(client_ip_address=ip_address, client_user_agent=user_agent,email = email, phone = phone)
    event = Event(
        event_source_url = url,
        event_name="Lead",
        event_time=int(time.time()),
        user_data=UserData(client_ip_address=ip_address, client_user_agent=user_agent),
        #custom_data=CustomData(value=conversion_value,currency="USD"),
        action_source=ActionSource.WEBSITE
    )
    if test_code:
        event_request_async = EventRequestAsync(events=[event], pixel_id=pixel_id,test_event_code = test_code)
    else:
        event_request_async = EventRequestAsync(events=[event], pixel_id=pixel_id)
    return await event_request_async.execute()


if __name__ =="__main__":
    import asyncio

    pixel_id = '612226083918432'
    access_token = 'EAADoycsKvREBAGeTwQkAX6xZBZBvXXdZCoX3NV0YLMFqttemnjxg7dLCUSWRAr4xYJFSMQmAlydZBdOnBGEDJfRaZAl9AYV2ZAjgDOunaoACGA3zRFzfJC0Pt6sVhNmXSoTUDLAHaYfutDtgAkSeFbkzZBBssNgpCylDOH9Y4bhywj6ZCiEZAh2ZCW'
    url = 'https://tylenolautism.consumerinjurysettlements.com'

    r = asyncio.run(fire_fb_pixel(access_token = access_token,
                              pixel_id = pixel_id,
                              url = url,
                              ip_address = '198.72.192.43',
                              user_agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
                              email = 'akhverdyanh@gmail.com',
                              phone = '18187263197',
                              test_code = 'TEST61688',
                              ))
    print(r)