from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from app.logger import init_logging,logger
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from app.fb import fire_fb_pixel
import httpx


pixel_id ='612226083918432'
access_token ='EAADoycsKvREBAGW46MZAoLJPBdOdpofKSIwZBITVs4PVAhjiD7RyaCHItNzB2jlIJZA86oMcS964JfUAIiu1apOMlRCUhLW2vGSm54EpJrwzKaiQ0dXoXTVXp7biOkC2OfnXs0OemKWDrJxHmLj6qf4b02J18rknKEJH5cZB95tPYIjhoEcazC7vF2k2NlQZD'
url = 'https://tylenolautism.consumerinjurysettlements.com'


templates = Jinja2Templates(directory='templates')


async def index(request):
    return templates.TemplateResponse('index.html', {'request': request})


async def success(request):
    return templates.TemplateResponse('complete.html', {'request': request})


async def failure(request):
    return templates.TemplateResponse('complete.html', {'request': request})

async def ccpa(request):
    return templates.TemplateResponse('ccpa.html', {'request': request})


async def process_ccpa(request):
    payload = await request.json()
    return JSONResponse({"Success":True})

async def process(request):
    payload = await request.form()
    postdata = {
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
                "under_18" : payload['child_under_18'].lower(),
                "diagnosed_asd" : payload['asd_diagnosis'].lower()
    }
    logger.info(payload)
    async with httpx.AsyncClient() as client:
        r = await client.post('https://leadsapi.leadspediatrack.com/post.do', data = postdata)
        r = r.json()
        logger.info(r)
    if r.get('errors'):
        return JSONResponse({"error":True})
    else:
        if postdata['under_18'] == 'yes' and postdata['diagnosed_asd'] == 'yes':
            await fire_fb_pixel(
                        access_token = access_token,
                        pixel_id = pixel_id,
                        user_agent = request.headers['user-agent'],
                        url = url,
                        fname = postdata['first_name'],
                        lname = postdata['last_name'],
                        ip_address = request.client.host,
                        email = postdata['email_address'],
                        phone = postdata['phone_home']
            )
        return JSONResponse({"success": True})


routes = [
    Route('/', endpoint=index),
    Route('/ccpa',endpoint = ccpa),
    Route('/complete', endpoint=success),
    Route('/failure', endpoint=failure),
    Mount('/static', StaticFiles(directory='static'), name='static'),
    Route('/api/ccpa', endpoint=process_ccpa,methods = ["POST"]),
    Route('/api/submitform', endpoint=process,methods = ["POST"]),
]

middlewears = [ Middleware(ProxyHeadersMiddleware, trusted_hosts="*") ,
                Middleware(HTTPSRedirectMiddleware),
                Middleware(CORSMiddleware, allow_origins=['*'], allow_headers = ['*'],allow_methods = ['*'])

                ]

app = Starlette(debug=False, routes=routes,middleware = middlewears)
init_logging()
