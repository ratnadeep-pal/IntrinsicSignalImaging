%Create baseline across all frames
illuminance = zeros(45*10,'double');
il_num = zeros(45*10);
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
        index = ceil(dur*10 / duration('00:00:01'));
            if(avg_pixel(i)>min_pixel) % There are some dark images
                    %if (mod(i,2)==0)
                        im = uint32(squeeze(raw_image(i,:,:)));
                        roi = imcrop (im,[246 245 19 27]);
                        mean_roi = mean (roi,'all');
                        illuminance(index) = illuminance(index)+ mean_roi;
                        il_num (index) = il_num(index)+1;
                        %im = imgaussfilt(im,0.4);
                    %end
            end
    end
end
for i=1:length(illuminance)
    if illuminance(i)>0
        illuminance(i) = illuminance(i)/il_num(i);
    end
end

plot(-log10(illuminance(1:length(illuminance))))