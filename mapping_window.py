import PySimpleGUI as sg
import re
 
class Mapping_Window():
    def __init__(self):
        self.tbl_to_view_map_out = []
 
    def format_alert_col(self, tbl_populated):
        alert_str = ''
        if tbl_populated == 0:
            alert_str = '(!)'
        return alert_str
 
    def camel_to_underscores(self,camel_string):
        split = re.findall('[A-Z][^A-Z]*', camel_string)
        new_name = ''
        if not split or len(split) <= 1:
            new_name = camel_string.lower()
            if new_name == 'id':
                new_name = 'oldid'
        else:
            for item in split:
                new_name = new_name + "_" + item.lower()
            new_name = new_name[1:]
            if new_name.endswith('_id'):
                new_name = 'uuid_' + new_name.replace('_id','')
        return new_name
   
    def get_run_default(self,tbl_populated):
        if tbl_populated == 1:
            run_default = True
        else:
            run_default = False
        return run_default
   
    def get_inputs(self,tbl_to_view_mapping):
        sg.theme('LightBlue2')  
 
        src_tbl_col = [[sg.Text('Source Table Name',font=("Helvetica", 10, "bold"))]]
        dbo_vw_col = [[sg.Text('DBO View Name',font=("Helvetica", 10, "bold"))]]
        run_col = [[sg.Text('Run?',font=("Helvetica", 10, "bold"), pad = (0,1))]]
        alert_col = [[sg.Text('Empty?',font=("Helvetica", 10, "bold"), pad = (0,1))]]
 
        for row_num in range(len(tbl_to_view_mapping)):
            src_tbl = tbl_to_view_mapping[row_num][0]
            tbl_populated = tbl_to_view_mapping[row_num][1]
            src_tbl_col.append([sg.Text(src_tbl)])
            dbo_vw_col.append([sg.Input(self.camel_to_underscores(src_tbl), key = 'DBO VIEW ROW ' + str(row_num))])
            run_col.append([sg.Checkbox('', default = self.get_run_default(tbl_populated), pad = (0,1), key = 'RUN ROW ' + str(row_num))])
            alert_col.append([sg.Text(self.format_alert_col(tbl_populated))])
 
        layout_header = [sg.Button(u'\u2713All', size = (4,0))]
        layout_footer = [sg.Button('OK', size=(15, 0)), sg.Button('Cancel', size=(15, 0))]
        scale = 1
        if len(tbl_to_view_mapping) > 20:
            scale = round(len(tbl_to_view_mapping)/30)
 
        layout = [ 
            layout_header,
            [
            sg.Column(alert_col,element_justification = 'c',scrollable=True,vertical_scroll_only=True,size_subsample_height=scale),
            sg.Column(run_col, element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_height=scale),
            sg.Column(src_tbl_col, element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_height=scale),
            sg.Column(dbo_vw_col, element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_height=scale)
            ],
            layout_footer
        ]
 
 
        # Create the Window
        window = sg.Window('Map Source Tables to DBO Views', layout, resizable=True)
        # Handle events
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == u'\u2713All':
                #find out if all checkboxes are checked now
                all_true = 1
                for row_num in range(len(tbl_to_view_mapping)):
                    if values['RUN ROW ' + str(row_num)] == False:
                        all_true = 0
                #toggle checkboxes
                for row_num in range(len(tbl_to_view_mapping)):
                    if all_true == 1:
                        window['RUN ROW ' + str(row_num)].update(False)     
                    else:
                        window['RUN ROW ' + str(row_num)].update(True)       
            elif event == 'OK':
                for row_num in range(len(tbl_to_view_mapping)):
                    src_tbl = tbl_to_view_mapping[row_num][0]
                    dbo_vw = values['DBO VIEW ROW ' + str(row_num)]
                    run = values['RUN ROW ' + str(row_num)]
                    out_row = (src_tbl,dbo_vw,run)
                    self.tbl_to_view_map_out.append(out_row)
                break
 
        window.close()
        return self.tbl_to_view_map_out
 
def main():
    tbl_to_view_mapping = [
    ('appointments',''),
    ('employers',''),
    ('facilities','facility_details'),
    ]
    map_win = Mapping_Window()
    tbl_to_view_map_out = map_win.get_inputs(tbl_to_view_mapping)
    print(tbl_to_view_map_out)
 
if __name__ == '__main__':
    main()