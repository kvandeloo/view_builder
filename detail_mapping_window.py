import PySimpleGUI as sg
 
class Detail_Mapping_Window():
    def __init__(self):
        self.tbl_to_view_map_out = []
 
    def format_alert_col(self, tbl_populated):
        alert_str = ''
        if tbl_populated == 0:
            alert_str = '(!)'
        return alert_str
 
    def get_inputs(self,tbl_to_view_mapping):
        sg.theme('LightBlue1')  
 
        src_tbl_col = [[sg.Text('Source Table Name',font=("Helvetica", 10, "bold"))]]
        dbo_vw_col = [[sg.Text('DBO View Name',font=("Helvetica", 10, "bold"))]]
        run_col = [[sg.Text('Run?',font=("Helvetica", 10, "bold"), pad = (0,1))]]
        alert_col = [[sg.Text('Empty?',font=("Helvetica", 10, "bold"), pad = (0,1))]]
        #detail view builder columns
        modal_name_col = [[sg.Text('DBO Parent View Name',font=("Helvetica", 10, "bold"))]]
        modal_lnk_id_col1 = [[sg.Text('DBO Parent View Link ID Column1',font=("Helvetica", 10, "bold"))]]
        src_dtl_lnk_id_col1 = [[sg.Text('Source Detail View Link ID Column1',font=("Helvetica", 10, "bold"))]]
        modal_lnk_id_col2 = [[sg.Text('DBO Parent View Link ID Column2',font=("Helvetica", 10, "bold"))]]
        src_dtl_lnk_id_col2 = [[sg.Text('Source Detail View Link ID Column2',font=("Helvetica", 10, "bold"))]]
 
        for row_num in range(len(tbl_to_view_mapping)):
            src_tbl = tbl_to_view_mapping[row_num][0]
            tbl_populated = tbl_to_view_mapping[row_num][1]
            src_tbl_col.append([sg.Text(src_tbl)])
            dbo_vw_col.append([sg.Input(src_tbl, key = 'DBO VIEW ROW ' + str(row_num))])
            run_col.append([sg.Checkbox('', default = True, pad = (0,1), key = 'RUN ROW ' + str(row_num))])
            alert_col.append([sg.Text(self.format_alert_col(tbl_populated))])
            modal_name_col.append([sg.Input('',key = 'DBO MODAL NAME ROW ' + str(row_num))])
            modal_lnk_id_col1.append([sg.Input('',key = 'DBO MODAL LNK1 ROW ' + str(row_num))])
            src_dtl_lnk_id_col1.append([sg.Input('',key = 'SRC DTL LNK1 ROW ' + str(row_num))])
            modal_lnk_id_col2.append([sg.Input('',key = 'DBO MODAL LNK2 ROW ' + str(row_num))])
            src_dtl_lnk_id_col2.append([sg.Input('',key = 'SRC DTL LNK2 ROW ' + str(row_num))])
 
        layout_header = [sg.Button(u'\u2713All', size = (4,0))]
        layout_footer = [sg.Button('OK', size=(15, 0)), sg.Button('Cancel', size=(15, 0))]
 
        layout = [ 
            layout_header,
            layout_footer,
            [
            sg.Column(alert_col,element_justification = 'c',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5),
            sg.Column(run_col, element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5),
            sg.Column(src_tbl_col, element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5),
            sg.Column(dbo_vw_col, element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5),
            sg.Column(modal_name_col,element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5),
            sg.Column(modal_lnk_id_col1,element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5),
            sg.Column(src_dtl_lnk_id_col1,element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5),
            sg.Column(modal_lnk_id_col2,element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5),
            sg.Column(src_dtl_lnk_id_col2,element_justification = '1',scrollable=True,vertical_scroll_only=True,size_subsample_width=2,size_subsample_height=5)
            ]
        ]
 
 
        # Create the Window
        window = sg.Window('Map Source Tables to DBO Views', layout)
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
                    dbo_modal_name = values['DBO MODAL NAME ROW ' + str(row_num)]
                    dbo_modal_lnk1 = values['DBO MODAL LNK1 ROW ' + str(row_num)]
                    src_dtl_lnk1 = values['SRC DTL LNK1 ROW ' + str(row_num)]
                    dbo_modal_lnk2 = values['DBO MODAL LNK2 ROW ' + str(row_num)]
                    src_dtl_lnk2 = values['SRC DTL LNK2 ROW ' + str(row_num)]
                    out_row = (src_tbl,dbo_vw,run,dbo_modal_name,dbo_modal_lnk1,src_dtl_lnk1,dbo_modal_lnk2,src_dtl_lnk2)
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
    map_win = Detail_Mapping_Window()
    tbl_to_view_map_out = map_win.get_inputs(tbl_to_view_mapping)
    print(tbl_to_view_map_out)
 
if __name__ == '__main__':
    main()