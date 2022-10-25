from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from logger import init_logging,logger
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from starlette.middleware import Middleware
from fb import fire_fb_pixel
import httpx


pixel_id ='612226083918432'
access_token ='EAADoycsKvREBAGeTwQkAX6xZBZBvXXdZCoX3NV0YLMFqttemnjxg7dLCUSWRAr4xYJFSMQmAlydZBdOnBGEDJfRaZAl9AYV2ZAjgDOunaoACGA3zRFzfJC0Pt6sVhNmXSoTUDLAHaYfutDtgAkSeFbkzZBBssNgpCylDOH9Y4bhywj6ZCiEZAh2ZCW'
url = 'https://tylenolautism.consumerinjurysettlements.com'


templates = Jinja2Templates(directory='templates')


async def index(request):
    return templates.TemplateResponse('index.html', {'request': request})


async def success(request):
    return templates.TemplateResponse('complete.html', {'request': request})


async def failure(request):
    return templates.TemplateResponse('complete.html', {'request': request})


async def process(request):
    payload = await request.json()
    payload = {
                'lp_campaign_id' : "6348d8d6859cf",
                "lp_campaign_key" : "WtCHRxBbvYc9VLhkpJD7",
                "trusted_form_cert_id" : payload['trusted_form_cert_id'],
                'journaya_lead_id' : payload['universal_leadid'],
                'leadid_tcpa_disclosure': payload['leadid_tcpa_disclosure'],
                "lp_s1" : payload['lp_s1'],
                "lp_s2" : payload['lp_s2'],
                "lp_s3" : payload['lp_s3'],
                "lp_s4" : payload['lp_s4'],
                "lp_s5" : payload['lp_s5'],
                "lp_response": "json",
                "lp_test" : "0",
                "first_name" : payload['firstname'],
                "last_name" : payload['lastname'],
                "phone_home" : payload['phonenumber'],
                "email_address" : payload['email'],
                "ip_address" : request.client.host,
                "brand" : payload['brand'],
                "description" : payload['description'],
                "under_18" : payload['child_under_18'],
                "diagnosed_asd" : payload['asd_diagnosis']
    }
    async with httpx.AsyncClient() as client:
        r = await client.post('https://leadsapi.leadspediatrack.com/post.do', data = payload)
        r = r.json()
    logger.info(r)
    if r.get('errors'):
        return JSONResponse({"error":True})
    else:
        await fire_fb_pixel(
                          access_token = access_token,
                          pixel_id = pixel_id,
                          url = url,
                          ip_address = request.client.host,
                          user_agent= request.headers['user-agent'],
                          email = payload['email'],
                          phone = payload['phonenumber']
                          )
        return JSONResponse({"success": True})


routes = [
    Route('/', endpoint=index),
    Route('/success', endpoint=success),
    Route('/failure', endpoint=failure),
    Mount('/static', StaticFiles(directory='static'), name='static'),
    Route('/api/submitform', endpoint=process,methods = ["POST"]),
]

middlewears = [ Middleware(ProxyHeadersMiddleware, trusted_hosts="*") ,
                Middleware(HTTPSRedirectMiddleware)
                ]

app = Starlette(debug=False, routes=routes,middlewears = middlewears)
init_logging()
