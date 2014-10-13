import logging, cherrypy
import splunk.appserver.mrsparkle.controllers as controllers
from splunk.appserver.mrsparkle.lib.decorators import expose_page
import splunk.entity

logger = logging.getLogger('splunk.appserver.controllers.refresh')

class RDPController(controllers.BaseController):

    @expose_page(must_login=True, methods=['GET']) 
    def connect(self, server=None, domain=None, **kwargs) :
        try:
            self.settings = settings = splunk.clilib.cli_common.getConfStanza('rdp_settings', 'default')

            administrative_session = settings.get('administrative_session')
            if not administrative_session:
                administrative_session = "1"

            audiomode = settings.get('audiomode')
            if not audiomode:
                audiomode = "2"

            desktopwidth = settings.get('desktopwidth')
            if not desktopwidth:
                desktopwidth = "1436"

            desktopheight = settings.get('desktopheight')
            if not desktopheight:
                desktopheight = "925"

            if domain is None:
                domain = settings.get('domain')

            screen_mode_id = settings.get('screen_mode_id')
            if not screen_mode_id:
                server_port = "1"

            rdp_content = """administrative session:i:{administrative_session}
audiomode:i:{audiomode}
desktopwidth:i:{desktopwidth}
desktopheight:i:{desktopheight}
domain:s:{domain}
full address:s:{full_address}
screen mode id:i:{screen_mode_id}""".format(
                administrative_session = administrative_session,
                audiomode = audiomode,
                desktopwidth = desktopwidth,
                desktopheight = desktopheight,
                domain = domain,
                full_address = server,
				screen_mode_id = screen_mode_id)

            cherrypy.response.headers["Content-Disposition"] = "attachment; filename=connect.rdp"
            cherrypy.response.headers["Content-Type"] = "application/rdp"

        except Exception, e:
            logger.exception(e)
            if hasattr(e, 'extendedMessages') and e.extendedMessages:
                errorMessage = e.extendedMessages[0]['text']
            else :
                errorMessage = e
            rdp_content = "Error occurred " + e.__class__.__name__ + " " + unicode(errorMessage)

        return rdp_content
