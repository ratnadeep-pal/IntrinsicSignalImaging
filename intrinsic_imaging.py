import os
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
from datetime import datetime
from datetime import timedelta
from collections import defaultdict
import PySimpleGUI as sg

def intrinsic_imaging(target_folder = 'C:/Users/rpal/Documents/MATLAB/20221219_145219',row = 520,column = 696,cutoff_time = 10,MAX_FRAMES = 500,baseline_start=0,baseline_stop=2,
stimuli_start=3,stimuli_stop=5,filtering=True,filter_size=5):

    cutoff_delta = timedelta(seconds = cutoff_time)
    

    #Extract the event triggers from EventLog.txt
    trigger_timestamp=defaultdict(int)
    e_f = open(target_folder+'/EventLog.txt','r')
    for line in e_f.readlines():
        if 'Trigger Count=' in line:
            l_split = line.split(' ') #Delimiter space
            num_trigger = l_split[-1].split('=')
            num_trigger = int(num_trigger[1])
            trigger_timestamp[num_trigger-1] = datetime.strptime(l_split[1],'%H:%M:%S.%f')

    NUM_TRIGGER = len(trigger_timestamp)
    #NUM_TRIGGER = 1

    trigger = 0
    frame = 0 
    frames_s_w = np.zeros((NUM_TRIGGER,cutoff_time, MAX_FRAMES, row,column),dtype = np.uint8 )
    image_file_list = sorted(os.listdir(target_folder+'/Camera #1/ManualRecording'))
    for image_file in image_file_list:
        im_f = image_file.split('_')
        im_f = im_f[1]
        im_f = datetime.strptime(im_f,'%H%M%S%f') 
        if im_f<trigger_timestamp[trigger]:
            continue
        else:
            delta = im_f - trigger_timestamp[trigger] 
            if delta > cutoff_delta:
                trigger = trigger + 1
                frame = 0
                if trigger >= NUM_TRIGGER:
                    break
                else:
                    continue
            with open(target_folder+'/Camera #1/ManualRecording/'+image_file,'rb') as f:
                image = np.fromfile(f, dtype = np.uint16, count = row*column)
                image = (image//257).astype(np.uint8)
                image = image.reshape(row,column)
                if (filtering):
                    image = cv.GaussianBlur(image,(filter_size,filter_size),0)
                frames_s_w[trigger][delta.seconds][frame] = image
                frame += 1
                f.close()


    baseline = frames_s_w[:,baseline_start:baseline_stop] 
    stimuli  = frames_s_w[:,stimuli_start:stimuli_stop]


    baseline_mean = np.mean(baseline[np.where(np.mean(baseline,axis=(3,4))>1)],axis=0)
    stimuli_mean  = np.mean(stimuli[np.where(np.mean(stimuli,axis=(3,4))>1)],axis=0)


    result = np.divide(baseline_mean - stimuli_mean,baseline_mean)

    #baseline_fft = np.fft.fft2(baseline_mean)
    #baseline_fft= np.fft.fftshift(baseline_fft)

    plt.figure()
    plt.title("Difference")
    plt.imshow(result) 
    plt.figure()
    plt.title("Baseline")
    plt.imshow(baseline_mean,cmap='gray')
    plt.figure()
    plt.title("Stimuli")
    plt.imshow(stimuli_mean,cmap='gray')
    plt.show()
    # plt.figure()
    # plt.title("FFT")
    # plt.imshow(20*np.log(np.abs(baseline_fft)),cmap='gray')
    # plt.show()

def main():
    sg.theme('BluePurple')

    layout = [[sg.Text('Select Image Folder'),sg.In(key='-in_folder-')],
            [sg.FolderBrowse(target='-in_folder-'), sg.OK()],
            [sg.Text('Row'),sg.Input(default_text='520',s=4,key='-in_row-'),sg.Text('Column'),sg.Input(default_text='696',s=4,key='-in_col-'),
            sg.Text('Cutoff'), sg.Input(default_text='10',s=4,key='-in_cutoff-'),sg.Text('Max Frame'), sg.Input(default_text='350',s=4,key='-in_mf-')],
            [sg.Text('Baseline'), sg.Input(default_text='0',s=2,key='-in_bl_sa-'),sg.Text('to'), sg.Input(default_text='2',s=2,key='-in_bl_so-'),
            sg.Text('Stimuli'), sg.Input(default_text='3',s=2,key='-in_st_sa-'),sg.Text('to'), sg.Input(default_text='5',s=2,key='-in_st_so-'),
            sg.Checkbox('Filter', default=True, key="-in_filter-"),sg.Input(default_text='5',s=2,key='-in_filter_size-')],
            [sg.Text(key='-OUTPUT-')],
            [sg.Button('Run'), sg.Button('Exit')]]

    window = sg.Window('Intrinsic Signal Imaging', layout)

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        all_fields = 1
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Run':
            # Update the "output" text element to be the value of "input" element

            for key in values:
              if values[key] == '':
                window['-OUTPUT-'].update(f"Some key values are missing!!")
                all_fields = 0
            if (all_fields):
                folder = values['-in_folder-']
                row = int(values['-in_row-'])
                column = int(values['-in_col-'])
                cutoff = int(values['-in_cutoff-'])
                max_frame = int(values['-in_mf-'])
                baseline_start=int(values['-in_bl_sa-'])
                baseline_stop=int(values['-in_bl_so-'])
                stimuli_start=int(values['-in_st_sa-'])
                stimuli_stop=int(values['-in_st_so-'])
                filtering = bool(values['-in_filter-'])
                filter_size = int(values['-in_filter_size-'])
                intrinsic_imaging(target_folder=folder, row=row, column=column, cutoff_time=cutoff, MAX_FRAMES=max_frame,baseline_start=baseline_start,baseline_stop=baseline_stop,
    stimuli_start=stimuli_start,stimuli_stop=stimuli_stop,filtering=filtering,filter_size=filter_size)
                window['-OUTPUT-'].update(f"SUCCESS!!")
            else:
                continue
    window.close()
    

if __name__ == "__main__":
    main()




    