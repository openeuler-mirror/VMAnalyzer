#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Route alerts to multiple notification channels."""
import json, logging, subprocess as sp
LOG=logging.getLogger(__name__)

class NotificationRouter:
    """Send alerts via email, webhook, log, or custom channels."""
    def __init__(self):
        self.channels={}

    def register(self,name,handler_func):
        self.channels[name]=handler_func

    def send(self,alert):
        results={}
        for name,handler in self.channels.items():
            try:
                handler(alert)
                results[name]=True
            except Exception as e:
                LOG.error(f"Notification {name} failed: {e}")
                results[name]=False
        return results

    @staticmethod
    def email_handler(smtp_host,to_addr):
        def send(alert):
            import smtplib
            from email.mime.text import MIMEText
            msg=MIMEText(json.dumps(alert,indent=2)); msg["Subject"]=f"VMAnalyzer Alert: {alert.get(level,INFO)}"; msg["To"]=to_addr
            with smtplib.SMTP(smtp_host) as s: s.send_message(msg)
        return send

    @staticmethod
    def webhook_handler(url):
        def send(alert):
            import urllib.request
            data=json.dumps(alert).encode()
            urllib.request.urlopen(urllib.request.Request(url,data=data,headers={"Content-Type":"application/json"}),timeout=5)
        return send
