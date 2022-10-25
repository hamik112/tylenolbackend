from starlette.responses import RedirectResponse,PlainTextResponse
from starlette.requests import Request
from logger import logger
from fb import fire_fb_pixel


async def click_redirect(request:Request):
    hit_id = request.cookies.get('hit_id',request.query_params.get('hit_id',None))
    campaign_id = request.cookies.get('campaign_id',request.query_params.get('campaign_id',None))
    if hit_id is None or campaign_id is None:
        return PlainTextResponse('<html><body></body></html>')
    else:
        hit_id = int(hit_id)
        campaign_id = int(campaign_id)
    async with get_session() as session:
        campaign_result = await session.execute(select(Campaign).where(Campaign.id == campaign_id))
        campaign = campaign_result.scalars().first()
        url = campaign.offer_url
        url = url.replace('{hit_id}',str(hit_id)).replace('{campaign_id}',str(campaign_id))
    async with get_session() as session:
        hit_result = await session.execute(select(Hit).where(Hit.id == hit_id))
        hit = hit_result.scalars().first()
        logger.info(f"hit result: {hit}")
        if hit is not None:
            if hit.fbc is None and request.query_params.get('fbc') is not None:
                hit.fbc = request.query_params.get('fbc')
            if hit.fbp is None and request.query_params.get('fbp') is not None:
                hit.fbp = request.query_params.get('fbp')
            if hit.fbclid is None and request.query_params.get('fbclid') is not None:
                hit.fbclid = request.query_params.get('fbclid')
            hit.click_to_offer = True
            session.add(hit)
            await session.commit()
        return RedirectResponse(url)


async def campaign_direct(request):
    campaign_id = request.path_params['campaignid']
    if not campaign_id:
        return PlainTextResponse('<html><body></body></html>')
    async with get_session() as session:
        campaign_result = await session.execute(select(Campaign).where(Campaign.id == campaign_id))
        campaign = campaign_result.scalars().first()
        print(campaign)
        if campaign is not None:
            hit = Hit(campaign_id=campaign.id,
                      ipaddress=request.client.host,
                      user_agent=request.headers.get('User-Agent', ''),
                      s1 = request.query_params.get('s1'),
                      s2 = request.query_params.get('s2'),
                      s3 = request.query_params.get('s3'),
                      fbp = request.cookies.get('_fbp'),
                      fbc = request.cookies.get('_fbc'),
                      fbclid = request.query_params.get('fbclid')
                      )
            session.add(hit)
            await session.commit()
            r = RedirectResponse(f"{campaign.lander_url}?campaign_id={campaign_id}&hit_id={hit.id}&fbclid={request.query_params.get('fbclid','')}")
            r.set_cookie('hit_id', hit.id)
            r.set_cookie('campaign_id', campaign.id)
            return r
        else:
            return RedirectResponse(url='https://www.google.com/')


async def postback(request):
    hit_id = int(request.query_params.get('hit_id',None))
    campaign_id = int(request.query_params.get('campaign_id',None))
    if hit_id is None or campaign_id is None:
        return PlainTextResponse('<html><body></body></html>')
    else:
        hit_id = int(hit_id)
        campaign_id = int(campaign_id)
    async with get_session() as session:
        campaign_result = await session.execute(select(Campaign).where(Campaign.id == campaign_id))
        campaign = campaign_result.scalars().first()
    async with get_session() as session:
        hit_result = await session.execute(select(Hit).where(Hit.id == hit_id))
        hit = hit_result.scalars().first()
        if hit is not None:
            r =  await fire_fb_pixel(campaign.token, campaign.pixel_id,campaign.offer_payout,hit.ipaddress,hit.user_agent,
                                             campaign.fb_event, campaign.fb_action_source )
            logger.info(f"postback response: {r}")

    return PlainTextResponse("OK")
