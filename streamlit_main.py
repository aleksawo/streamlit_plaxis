import streamlit as st
from plxscripting.easy import *
import pandas as pd
import os

#streamlit run your_script.py --server.port 80


tab1, tab2 = st.tabs(["Plott modell", "Hent ankerkrefter"])


def run_plaxis_model_plotter():

    st.title('Plaxis plotter')
    pw = st.text_input('input plaxis passord')
    #pw='?GBz75iy^BwZy/2Y'#input("Passord for remote scripting server: ")
    port_num = st.number_input('port input',value=10000)
    port_num_output = st.number_input('port output',value=10001)

    #port_num = 10000
    #port_num_output = 10001

    s_o, g_o = new_server('localhost', port_num_output, password=pw)
    s_i, g_i = new_server('localhost', port_num, password=pw)


    col1, col2 = st.columns([0.5, 0.5])


    #st.sidebar.write('plott jord')


    def project_title():
        proj_info = g_i.echo()
        proj_info_list = proj_info.splitlines()
        proj_title = proj_info_list[1].split("Title: ", 1)[1]
        proj_title = proj_title[1:-1]
        return proj_title

    def get_phase_screenname(phase):
        return '{} - {}'.format(phase.Name.value, phase.Identification.value.split('[')[0].strip())

    def checkbox_container(data):
        cols = st.columns(3)
        if cols[0].button('Select All'):
            for i in data:
                st.session_state['dynamic_checkbox_' + i] = True
            st.experimental_rerun()
        if cols[1].button('UnSelect All'):
            for i in data:
                st.session_state['dynamic_checkbox_' + i] = False
            st.experimental_rerun()
        for i in data:
            st.checkbox(i, key='dynamic_checkbox_' + i)



    def get_selected_checkboxes():
        return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

    def get_phase_name(phasechoices):
        phase_list_names = []
        phaselist = []
        if phasechoices:
            for phase in g_o.Phases[:]:
                if get_phase_screenname(phase) in phasechoices:
                    phaselist.append(phase)
                    phase_list_names.append(phase.Identification.value)

        phases = phaselist[:]
        phase_name = phase_list_names[:]
        return phases, phase_name

    def ask_phases():
        """ asks the user to specify the phase to get the results for """
        # at first, just one phase, but can be expanded to more phases
        phaselist = []
        choicelist = [get_phase_screenname(phase) for phase in g_o.Phases[:]]
        msg = 'Select one or more phases to generate plate results for'
        # issue with easygui 0.97.4: multchoicebox acts as choicebox
        phasechoices = st.multiselect('select phases', choicelist)

        phase_list_names = []
        phaselist = []
        if phasechoices:
            for phase in g_o.Phases[:]:
                if get_phase_screenname(phase) in phasechoices:
                    phaselist.append(phase)
                    phase_list_names.append(phase.Identification.value)
        phases = phaselist[:]
        phase_name = phase_list_names[:]
        return phases, phase_name


    with col1:
        st.header("Velg faser")
    #    phases, phase_name = ask_phases()


        if 'phase_data' not in st.session_state.keys():
            phase_data = [get_phase_screenname(phase) for phase in g_o.Phases[:]]
            st.session_state['dummy_data'] = phase_data
        else:
            phase_data = st.session_state['dummy_data']
        checkbox_container(phase_data)

        #st.write('You selected:')
        #st.write(get_selected_checkboxes())

        phases, phase_name = get_phase_name(get_selected_checkboxes())

        #st.write(phase_name)

        save_location = st.text_input('mappe for lagring')
    #save_location= r'C:\Users\alew\Documents\Jobbting\Plaxis\Test_plott'


        #type_plot = st.multiselect('Velg plott', ['Utot','U_inc',3])

    with col2:
        type_plot = st.multiselect('Velg plot', ['U_tot', 'U_inc', 'delta_y_s', 'tot_y_s'])


        brukerdefinert_zoom = st.checkbox('Brukerdefinert zoom på plottene')
        if brukerdefinert_zoom:
            st.markdown('Skriv inn 2 kordinater som angir kvadrated som skal plottes - ofte y1 og y2 som styrer zoom nivå, og snitt av x1 og x2 blir senter')
            col5, col6, col7, col8= st.columns([0.25,0.25,0.25,0.25])

            with col5:
                x1 = st.number_input('x_1')
            with col6:
               y1 = st.number_input('y_1 ')
            with col7:
                x2 = st.number_input('x_2')
            with col8:

                y2 = st.number_input('y_2')




    #g_o.Plots[-1].zoom(-10, 10, 10, 40)

    os.chdir(save_location)

    if 'Utot' in type_plot:
        for phase in phases[0:]:
            newest_plot = g_o.Plots[-1]
            newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
            newest_plot.ResultType = g_o.ResultTypes.Soil.Utot
            newest_plot.PlotType = 'shadings'
            max_disp = max(g_o.getresults(phase, g_o.ResultTypes.Soil.Utot, 'node'))
            newest_plot.LegendSettings.MaxValue = max_disp
            name_plot = save_location + '''//''' + phase.Identification.value + '_Utot.png'
        #    name_plot = phase.Identification.value + '_Utot.png'
            if brukerdefinert_zoom:
                newest_plot.zoom(x1, y1, x2, y2)

            newest_plot.export(name_plot, 1200, 800)
            st.image(phase.Identification.value + '_Utot.png')
            #st.image(name_plot)


    if 'U_inc' in type_plot:
        for phase in phases[0:]:
            newest_plot = g_o.Plots[-1]
            newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
            newest_plot.ResultType = g_o.ResultTypes.Soil.dUtot
            newest_plot.PlotType = 'shadings'
            max_disp = max(g_o.getresults(phase, g_o.ResultTypes.Soil.dUtot, 'node'))
            newest_plot.LegendSettings.MaxValue = max_disp
            name_plot = save_location + '''//''' + phase.Identification.value + '_Uinc.png'
        #    name_plot = phase.Identification.value + '_Utot.png'
            if brukerdefinert_zoom:
                newest_plot.zoom(x1, y1, x2, y2)
            newest_plot.export(name_plot, 1200, 800)
            st.image(phase.Identification.value + '_Uinc.png')
            #st.image(name_plot)


    if 'delta_y_s' in type_plot:
        for phase in phases[0:]:
            newest_plot = g_o.Plots[-1]
            newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
            newest_plot.ResultType = g_o.ResultTypes.Soil.IncrementalDeviatoricStrain
            newest_plot.PlotType = 'shadings'
            max_disp = max(g_o.getresults(phase, g_o.ResultTypes.Soil.IncrementalDeviatoricStrain, 'node'))
            newest_plot.LegendSettings.MaxValue = max_disp
            name_plot = save_location + '''//''' + phase.Identification.value + '_delta_y_s.png'
        #    name_plot = phase.Identification.value + '_Utot.png'
            if brukerdefinert_zoom:
                newest_plot.zoom(x1, y1, x2, y2)
            newest_plot.export(name_plot, 1200, 800)
            st.image(phase.Identification.value + '_delta_y_s.png')
            #st.image(name_plot)

    if 'tot_y_s' in type_plot:
        for phase in phases[0:]:
            newest_plot = g_o.Plots[-1]
            newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
            newest_plot.ResultType = g_o.ResultTypes.Soil.TotalDeviatoricStrain
            newest_plot.PlotType = 'shadings'
            max_disp = max(g_o.getresults(phase, g_o.ResultTypes.Soil.TotalDeviatoricStrain, 'node'))
            newest_plot.LegendSettings.MaxValue = max_disp
            name_plot = save_location + '''//''' + phase.Identification.value + '_tot_y_s.png'
        #    name_plot = phase.Identification.value + '_Utot.png'
            if brukerdefinert_zoom:
                newest_plot.zoom(x1, y1, x2, y2)
            newest_plot.export(name_plot, 1200, 800)
            st.image(phase.Identification.value + '_tot_y_s.png')
            #st.image(name_plot)


with tab1:
    run_plaxis_model_plotter()

