from mycroft import MycroftSkill, intent_file_handler


class TempereatureReader(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('reader.tempereature.intent')
    def handle_reader_tempereature(self, message):
        self.speak_dialog('reader.tempereature')


def create_skill():
    return TempereatureReader()

