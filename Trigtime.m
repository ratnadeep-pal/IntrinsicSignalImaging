%Extract trigger time from EventLog.txt 
%This function is likely to break once Mightex changes its file format.
%Watch out.


log=readlines('EventLog.txt');
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