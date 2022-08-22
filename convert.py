#this script converts "10:43: text" formatted transcripts to srt format
#cannot handle hours yet (only mm:ss)s
import sys
import string
import re

def parse_timestamps(t: str, tm: str, d: list, l: str):
    '''
    input args are t (timestamp format in HH:MM:SS/etc.), a typemap (a string with digits replacing HH, etc. like so 00:00:00/etc), d (delimiter) and l (a piece of text to be parsed for t)
    '''
    #def detect_timestamp():
    #    for x in timestamp_format.split(d):
    #        pass
    
    for i,c in enumerate(tm):
        #print(c, l[i])
        if (c.isdecimal() & l[i].isdecimal()):
            continue
        elif (c.isalpha() & l[i].isalpha()):
            continue
        elif ((c in string.punctuation) & (l[i] in string.punctuation)):
            if c == l[i]:
                continue
            else:
                return False
        else:
            return False
    return l

def to_list_rm_punctuation(d,f):
    f = ''.join([":" if x in d else x for x in f])
    f = f.split(":")
    f = [x for x in f if x is not '']
    #print(f)
    return(f)

def format_timestamp(t: str,f: str,d: list):
    '''
    t: timestamp, f: timestamp format (HH:MM, etc.), d: delimiters
    '''
    #hi = [x += 'HI' for x in d if x in ['.', '\\', '+', '*', '?', '[', '^', ']', '$', '(', ')', '{', '}', '=', '!', '|', ':', '-']]
    #print(d)
    
    #for i,x in enumerate(timestamp_format):
    #if x in ("H","M","S","#"):
    
    #for i,c in enumerate(f):
    
    #print(t)
    #print(f)
    #print(d)
    
    f = to_list_rm_punctuation(d,f)
    f = [x.upper() for x in f]
    t = to_list_rm_punctuation(d,t)
    
    #map old timestamp to new formatted timestamp
    formatted_timestamp = ''
    convention = ['HH','MM','SS','###']
    for e in convention:
        #print('e ',e)
        #print('f ',f)
        if e in f:
            #print('e ',e)
            i = f.index(e)
            formatted_timestamp += t[i]
        else:
            for c in e:
                formatted_timestamp += '0'
        formatted_timestamp += ':'
    formatted_timestamp = formatted_timestamp[:-1]
    formatted_timestamp = formatted_timestamp[:8] + '.' + formatted_timestamp[9:]
    print(formatted_timestamp)
    
    return formatted_timestamp
        
def convert(filename):
    timestamp_format = input("Enter the timestamp format contained in the input text as well as any relevant delimiters (:,;,.) or parentheses ([],(),{}), and use the following characters: hours (HH), minutes (MM), seconds (SS), milliseconds (00..). For example, if your timestamps look like '[01:51:12]', then enter [HH:MM:SS], other formats could include MM:SS, (H:MM:SS.##), H:MM:SS.### etc.), according to https://momentjs.com/docs/#/displaying/format/")
    
    delimiters = []
    for c in timestamp_format.strip():
        #print(c)
        if c in string.punctuation:
            delimiters.extend(c)
    delimiters = [x for x in delimiters if x is not '#']
    #print('delimiters ',delimiters)
    
    #check where the first digit is
    for i,x in enumerate(timestamp_format):
        if x in ("H","M","S","#"):
            num_pos = i
            #print(i)
            break
            
    #create typemap
    timestamp_typemap = ""
    for i,x in enumerate(timestamp_format):
        if x in ("H","M","S","#"):
            timestamp_typemap += "0"
        else:
            timestamp_typemap += x
    #print(timestamp_typemap)
        
        #print(t)
        #print(d)
        #print(l)
            
    
    with open(filename, mode='r',encoding='UTF-8') as myfile:
        try:
            text = myfile.readlines()
        except Exception as e:
            print(e)
            print('No such readable file: ',filename)
        j = 0
        subtitles = {}
        
        for i,line in enumerate(text):
            print("line ",i,": ",line)
            line_contains_timestamp = False
            for k,c in enumerate(line):
                try:
                    if line[k+num_pos].isdigit():
                        possible_timestamp = line[k:k+len(timestamp_format)]
                        timestamp = parse_timestamps(timestamp_format, timestamp_typemap, delimiters, possible_timestamp)
                        if timestamp:
                            print('timestamp found!')
                            j+=1
                            remaining_text = line[k+len(timestamp_format):]
                            if remaining_text.strip() is not '':
                                subtitles[j] = [timestamp, remaining_text.strip()]
                            else:
                                subtitles[j] = [timestamp]
                            line_contains_timestamp = True
                            continue
                except IndexError as e:
                    pass
            else:
                if line_contains_timestamp:
                    pass
                else:
                    try:
                        if isinstance(subtitles[j], list):
                            if line.strip() is not '':
                                subtitles[j].append(line.strip())
                    except KeyError:
                        pass    

            '''
            try:
                if line[0].isdigit() & (line[1] == ":") & line[2].isdigit():
                    j+=1
                    timestamp = "00:0" + line[0:4] + ".000"
                    print(timestamp)
                    
                    remaining_text = line[5:]
                    subtitles[j] = [timestamp, remaining_text.strip()]
                    
                elif line[0].isdigit() & line[1].isdigit() & (line[2] == ":") & line[3].isdigit():
                    j+=1
                    timestamp = "00:" + line[0:5] + ".000"
                    print(timestamp)
                    
                    remaining_text = line[6:]
                    subtitles[j] = [timestamp, remaining_text.strip()]
                else:
                    try:
                        if isinstance(subtitles[j], list):
                            subtitles[j].append(line.strip())
                    except KeyError:
                        pass
                    #newfile.write(line)
            except IndexError as e:
                print(e)
                
            '''
        #print('printing subtitles ',subtitles)
        for k,v in subtitles.items():
            v[0] = format_timestamp(v[0], timestamp_format, delimiters)
        print(subtitles)
        #print('delimiters ',delimiters)
    return subtitles
    
def print_to_file(filename: str, subtitles: dict, ext: str):
    print('Printing to file')
    with open(filename + "_new" + ext, 'w', encoding='UTF-8') as newfile:
        if ext == '.srt':
            for k,v in subtitles.items():
                newfile.write(str(k))
                newfile.write('\n')
                try:
                    newfile.write(v[0] + " --> " + subtitles[k+1][0])
                except KeyError:
                    newfile.write(v[0] + " --> " + subtitles[k][0])
                newfile.write('\n')
                try:
                    [newfile.write(t+'\n') for t in v[1:]]
                except UnicodeEncodeError as e:
                    print(e)
                    print('Unprintable char is in: ',v[1:])
                                
                newfile.write('\n')
                newfile.write('\n')
        elif ext == '.vtt':
            pass
if __name__ == "__main__":
    if len(sys.argv) == 3:
        a = str(sys.argv[-2])
        b = str(sys.argv[-1])
        print_to_file(a, convert(a), b)
    else:
        print("2 args required: input filename and output subtitle extension type. Example: 'python convert_custom.py text.txt .vtt'")
'''
import sys

def s_to_hms(seconds):
    m, sec = divmod(seconds, 60)
    h, m = divmod(m, 60)    
    #print str(int(h)) + ":" + str(int(m)) + ":" + str(int(s))
    return str(int(h)) + ":" + str(int(m)) + ":" + str(int(sec))

def conform_to_srt(s,d):
    s = s.split(':')
    for i,x in enumerate(s):
        if len(x) < 2:
            s[i] = '0'+s[i]
    s = ':'.join(s)
    if len(d) < 3:
        d+=((3-len(d))*'0')
    s += ('.'+d)
    return s
    
def convert_trs(filename):
    with open(filename, mode='r',encoding='latin-1') as myfile:
        try:
            text = myfile.readlines()
        except Exception as e:
            print(e)
        with open(filename.replace('.trs','.srt'), 'w') as newfile:
            i = 1
            for t in text:
                if t[1:5] == 'Turn':
                    
                    starttime = t[t.find('startTime=')+11:t.find('endTime=')-2]
                    starttime_digits = list(starttime)
                    
                    #conform to srt standards (3 decimal places)s
                    if starttime != '0':
                        [starttime_digits.append('0') for x in range(4 - len(starttime_digits[starttime_digits.index('.'):]))]
                    
                    starttime = ''.join(starttime_digits)
                    #preserve 3 decimal values since they will be lost in conversion function
                    starttime_decimals = starttime[-3:]
                    starttime_srt = s_to_hms(float(starttime))
                    starttime_srt = conform_to_srt(starttime_srt,starttime_decimals)
                    
                    #---
                    
                    endtime_digits = []
                    endtime_pos = t.find('endTime=')
                    endtime_str = t[endtime_pos+9:endtime_pos+17]
                    
                    ([endtime_digits.append(x) for x in endtime_str if ((x.isdigit() or x == '.') and (len(endtime_digits) < 7))])
                    
                    #conform to srt standards (3 decimal places)s
                    [endtime_digits.append('0') for x in range(4 - len(endtime_digits[endtime_digits.index('.'):]))]
                    
                    endtime = ''.join(endtime_digits)
                    #preserve 3 decimal values since they will be lost in conversion function
                    endtime_decimals = endtime[-3:]
                    endtime_srt = s_to_hms(float(endtime))
                    endtime_srt = conform_to_srt(endtime_srt,endtime_decimals)
                    
                    #---
                    
                    newfile.write('\n')
                    newfile.write(str(i)+'\n')
                    newfile.write(starttime_srt+' --> '+endtime_srt+'\n')
                    i += 1
                elif t[0] != '<':
                    newfile.write(t)
                
if __name__ == "__main__":
    i = str(sys.argv[-1])
    convert_trs(i)
    
'''