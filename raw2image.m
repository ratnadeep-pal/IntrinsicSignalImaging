clear; clc;
width  = 348*2;
height = 260*2;
exp_name = '20221026_140422';
image_dir = '\Camera #1\ManualRecording';
Files=dir(strcat(exp_name,image_dir,'\*.*'));
base=zeros(height,width,'uint32');
basenum=0;
final=zeros(height,width,'uint32');
finalnum=0;
Files = Files(3:end);
filename = strings(1,length(Files));
min_pixel = 100;
%final_result=zeros(9,height,width,'uint16');
%% 

for i=1:length(filename) %Image file names in the directory
    filename(i)=Files(i).name;
end

filename = sort(filename); %sorted file names
raw_image = zeros(length(filename),height,width,'uint16');
avg_pixel = zeros(1,length(filename));

for i=1:length(filename)
    [fid,msg] = fopen(strcat(exp_name,image_dir,'\',filename(i)),'r');
    A = fread(fid,[width,height],'uint16=>uint16');
    raw_image(i,:,:)= A.'; %1500 image in a 3d matrix
    avg_pixel(i) = sum(A,'all')/(height*width);
    fclose(fid);
end

%% 

%Create a datetime database of all the frames
dt = NaT(1,length(filename));
for i=1:length(filename)
    dt_str = split(filename(i),'_');
    dt_str = dt_str(2);
    dt(i)  = datetime(dt_str,'InputFormat','HHmmssSSS');
end


%Extract trigger time from EventLog.txt 
%This function is likely to break once Mightex changes its file format.
%Watch out.


log=readlines(strcat(exp_name,'\EventLog.txt'));
%trig_1 = datetime('13:49:15','InputFormat','HH:mm:ss');
%trig_time=NaT(1,10);
trig_count = 0;
prev_count=0;
trig_time_st = [];
for i=1:length(log)
    l = split(log(i),' ');
    if (length(l)>3)
        if strcmp(l(3),'HardwareTrigger')
            
                trig_count = split(l(13),"=");
                trig_count = trig_count(2);
                trig_count = str2num(trig_count);
                if (trig_count>prev_count)
                    trig_time_st = [trig_time_st l(2)];
                    prev_count = trig_count; %No repitition 
                end
                
                
        end
    end
end

%Create a datetime database of all triggers

dt_trig = NaT(1,length(trig_time_st));
for i=1:length(trig_time_st)
    dt_trig(i)= datetime(trig_time_st(i),'InputFormat','HH:mm:ss.SSS');
end
%% 
temporal
%%

%Create baseline across all frames
current_trigger = 1;
next_trigger = 2;
for i=1:trig_count
    if (dt(1)-dt_trig(next_trigger)>0)
        current_trigger = current_trigger + 1;
        next_trigger = next_trigger + 1;
    else
        break;
    end
end

for i=1:(length(filename)-1)
    if (dt(i)-dt_trig(current_trigger)>0)
        if (next_trigger <= trig_count)
            if(dt(i)-dt_trig(next_trigger)>0)
                current_trigger = current_trigger + 1;
                next_trigger = next_trigger + 1;
            end
        end
        dur = dt(i)-dt_trig(current_trigger);  
           if((dur<duration('00:00:05'))&&(dur>=duration('00:00:02')))
                if(avg_pixel(i)>min_pixel) % There are some dark images
                    %if (mod(i,2)==0)
                        im = uint32(squeeze(raw_image(i,:,:)));
                        %roi = imcrop (im,[297 290 29 30])
                        im = imgaussfilt(im,0.5);
                        base = base + im;
                        basenum = basenum + 1;
                    %end
                end
           elseif ((dur<duration('00:00:11'))&&(dur>=duration('00:00:08')))
                if(avg_pixel(i)>min_pixel) % There are some dark images
                    %if (mod(i,2)==0)
                        im = uint32(squeeze(raw_image(i,:,:)));
                        im = imgaussfilt(im,0.5);                      
                        final = final + im;
                        finalnum = finalnum + 1;
                    %end
                end
            end
    end
end


% % h = fspecial('laplacian',0.2);
% % C = imfilter(B,h)
result = base/basenum - final/finalnum;
result=uint16(result);
%final_result(exp_name,:,:)=result;
% %imshow(final)
% %imshow(base)
figure,imshow(result*15)
figure, imshow(squeeze(raw_image(25,:,:)))