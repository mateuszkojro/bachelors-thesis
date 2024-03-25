import cortex
import time
import threading
import json
import os

RECORD_TITLE = "Record title"
RECORD_DESCRIPTION = "Record description"
EXPORT_FOLDER = './results/'
EXPORT_DATA = [
        # 'EEG', # Requires PRO license
        'MOTION', 
        'PM', 
        'BP']
EXPORT_FORMAT = "CSV"
EXPORT_VERSION = "V2"

class App():
    @staticmethod
    def injcect_marker(c: cortex.Cortex, value, label, **kwargs):
        device_time = time.time() * 1000
        c.inject_marker_request(device_time, value, label, **kwargs)

    @staticmethod
    def stop_recording(c: cortex.Cortex):
        c.stop_record()

    def __init__(self, device: cortex.Cortex, recording_id="no id", export_folder=EXPORT_FOLDER, on_export_done=None, **kwargs):
        self.c = device
        self.record_id = None
        self.recording_id = recording_id
        self.markers = []
        self.export_folder = os.path.abspath(export_folder)
        self.on_export_done = on_export_done
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(create_record_done=self.on_create_record_done)
        self.c.bind(stop_record_done=self.on_stop_record_done)
        self.c.bind(warn_cortex_stop_all_sub=self.on_warn_cortex_stop_all_sub)
        self.c.bind(inject_marker_done=self.on_inject_marker_done)
        self.c.bind(export_record_done=self.on_export_record_done)
        self.c.bind(inform_error=self.on_inform_error)

    def start(self):
        self.c.open()

    def app_func_handler(self):
        pass
        # self.app_function(self.c)
        # FIXME: Should wait for confirmation of the marker incjection
        # time.sleep(3)
        # self.c.stop_record()

    # callbacks functions
    def on_create_session_done(self, *args, **kwargs):
        self.c.create_record(self.recording_id, description=self.recording_id)

    def on_create_record_done(self, *args, **kwargs):
        # inject markers
        data = kwargs.get('data')
        self.record_id = data['uuid']
        th = threading.Thread(target=self.app_func_handler)
        th.start()
    
    def on_inject_marker_done(self, *args, **kwargs):    
        data = kwargs.get('data')
        self.markers.append(data)

    def on_stop_record_done(self, *args, **kwargs):
        self.c.disconnect_headset()

    def on_warn_cortex_stop_all_sub(self, *args, **kwargs):
        # cortex has closed session. Wait some seconds before exporting record
        time.sleep(3)
        self.c.export_record(self.export_folder, EXPORT_DATA,
                           EXPORT_FORMAT, [self.record_id], EXPORT_VERSION)


    def on_export_record_done(self, *args, **kwargs):
        self.c.close()
        with open(self.export_folder + "/markers.json", "w") as f:
            f.write(json.dumps(self.markers))
        
        if self.on_export_done is not None:
            self.on_export_done()

    def on_inform_error(self, *args, **kwargs):
        error_data = kwargs.get('error_data')
        print(error_data)

    @property
    def error(self):
        return self.c.error
        
def main():
    device = cortex.Cortex(
        client_id="DihnzihZqxJ44Cp3U6ZrGFJhecsA0yDCnL87hxDo",
        client_secret="pnMRf8NXC7adXPfAnF2Kuzqdiihyit509Kocyomde5ag8ifXMAVdL1vODesVmhTx5b0hw6DtmTSdfgMrRcTRyPahalgUWl6kFjvjeq0KIUHLRItsmBjRKOX4x9icByjO",
        debug_mode=True,
    )
    
    app = App(device=device)
    app.start()

if __name__ == "__main__":
    main()
