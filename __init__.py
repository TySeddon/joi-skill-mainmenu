from importlib import reload
import os
import webbrowser
from uuid import uuid4
from time import sleep
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.messagebus import Message
from mycroft.audio import wait_while_speaking
import joi_skill_utils
reload(joi_skill_utils)

from joi_skill_utils.enviro import get_setting
from joi_skill_utils.joiclient import JoiClient, MUSIC_TYPE

class JoiMainMenuSkill(MycroftSkill):

    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.learning = True
        self.stopped = False
        self.JOI_SERVER_URL = get_setting('joi_server_url')

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        self.log.info("initialize")

        # establish connection to Joi server
        self.joi_device_id = get_setting("device_id")
        self.joi_client = JoiClient(self.joi_device_id)
        resident = self.joi_client.get_Resident()
        self.resident_name = resident.first_name

        self.start_monitor()
        pass

    ###########################################

    @intent_handler(IntentBuilder('MainMenuIntent').require('MainMenu').optionally("Show"))
    def handle_show_mainmenu_intent(self, message):
        """ This is an Adapt intent handler, it is triggered by a keyword."""
        self.log.info("handle_show_mainmenu_intent")
        self.open_browser_home()

    def stop(self):
        """ The stop method is called anytime a User says "Stop" or a similar command. 
        It is useful for stopping any output or process that a User might want to end 
        without needing to issue a Skill specific utterance such as media playback 
        or an expired alarm notification.
        """
        self.log.info("mycroft.stop")
        return True

    def shutdown(self):
        """ The shutdown method is called during the Skill process termination. 
        It is used to perform any final actions to ensure all processes and operations 
        in execution are stopped safely. This might be particularly useful for Skills 
        that have scheduled future events, may be writing to a file or database, 
        or that have initiated new processes.
        """
        self.log.info("shutdown")

    ###########################################

    def open_browser_home(self):
        joi_server_url = get_setting("joi_server_url")
        url = f"{joi_server_url}/joi/joi_home?token={self.joi_client.token}&device={self.joi_device_id}"

        retry_count = 0
        success = False
        while not success and retry_count < 3:
            success = webbrowser.open(url=url, autoraise=True)
            sleep(1)
            retry_count += 1

    def close_browser(self):
        try:
            os.system("killall chromium-browser")
        except:
            self.log.warn("Error closing web browser")


    ###########################################

    def start_monitor(self):
        # Clear any existing event
        self.stop_monitor()
        if self.stopped: return

        self.log.info("start_monitor")
        # Schedule every few seconds to monitor Joi Server
        self.schedule_repeating_event(
            self.monitor_joi_server, None, 3, name="MonitorJoiServer"
        )

    def stop_monitor(self):
        self.log.info("stop_monitor")
        self.cancel_scheduled_event("MonitorJoiServer")
        self.not_playing_count = 0

    def monitor_joi_server(self):
        #self.log.info("monitor_joi_server")
        messages = self.joi_client.get_DeviceMessages()
        if messages:
            self.log.info(f"Received {len(messages)} messages from Joi Server")
            for msg in messages:
                if msg.action:
                    if msg.action == "play_photos":
                        self.bus.emit(Message("skill.joi-skill-photo.start"))
                    elif msg.action == "play_music":
                        self.bus.emit(Message("skill.joi-skill-music.start"))
                    elif msg.action == "stop_photos":
                        self.bus.emit(Message("skill.joi-skill-photo.stop"))
                    elif msg.action == "stop_music":
                        self.bus.emit(Message("skill.joi-skill-music.stop"))
                    else:
                        self.log.warn(f"Unknown action {msg.action}")

    def handle_listener_started(self, message):
        self.log.info("handle_listener_started")
        if self.play_state and self.play_state.is_playing:
            self.pause_song()
            self.start_idle_check()

    def start_idle_check(self):
        self.idle_count = 0
        self.stop_idle_check()
        self.schedule_repeating_event(
            self.check_for_idle, None, 1, name="IdleCheck"
        )       

    def stop_idle_check(self):
        self.cancel_scheduled_event("IdleCheck")

    def check_for_idle(self):
        self.log.info("check_for_idle")
        if self.play_state and self.play_state.is_playing:
            self.stop_idle_check()
            return
        self.idle_count += 1
        if self.idle_count >= 5:
            # Resume playback after 5 seconds of being idle
            self.stop_idle_check()
            if self.stopped: return
            self.resume_song()

    ###########################################        


def create_skill():
    return JoiMainMenuSkill()

