import librosa
import math
import numpy as np
import json
import os

class ProcessAudio():
    def __init__(self,audio,sa_freq,i):
        self.freq=self.plot_pitch(audio,i)
        self.sa_freq=self.plot_pitch(sa_freq)

        with open('C:/Users/anees/Documents/BlueLight/proj/final 2/raga_identifier-main/raga/raga_app/processing/shruti_data.json', 'r') as file:
            self.shruti = json.load(file)

        with open('C:/Users/anees/Documents/BlueLight/proj/final 2/raga_identifier-main/raga/raga_app/processing/swara_ratio_data.json', 'r') as file:
            self.final_ratio = json.load(file)

        with open('C:/Users/anees/Documents/BlueLight/proj/final 2/raga_identifier-main/raga/raga_app/processing/ragas.json', 'r') as file:
            self.ragas = json.load(file)

        self.final_ratio['sa1']=2.0

    def segment_stepwise_increase(self,points):
        segments = []
        thresh=1
        # print(points)
        points.sort()
        # print(points)
        for i in range(len(points)):
            if not (math.isnan(points[i])):
                points[i]=round(points[i],4)
                if len(segments)==0:
                    segments.append([points[i]])
                    continue
                max=[5,0]  #highest max,index
                for ind,seg in enumerate(segments):
                    max1=0
                    if abs(points[i] - np.mean(seg))<thresh:
                        max1=abs(points[i] - seg[0])
                        if max1<max[0]:
                            max[0]=max1
                            max[1]=ind
                if max[0]==5:
                    segments.append([points[i]])

                else:
                    segments[max[1]].append(points[i])
                    segments[max[1]].sort()
        
        # print('After mking groups',segments)

        while True:
            # med=[np.mean(x) for x in segments]
            # mea=[np.median(x) for x in segments]
            # print("Mean: ",med)
            # print("Median: ",mea)
            flag=0
            for ind,seg in enumerate(segments):
                for ind1,i in enumerate(seg):
                    # print('\n i=',i)
                    max=[5,ind,ind]                                  #max, from, to
                    for ind2,seg1 in enumerate(segments):
                        # print("initial max considered",abs(i - med[ind2]))
                        if abs(i - np.mean(seg1))<(thresh):
                            max1=abs(i - np.mean(seg1))
                            # print("max changed to ",max1)
                            if max1<max[0]:
                                max[0]=max1
                                max[2]=ind2
                                # print(max)
                    if max[0]==5:
                        segments.append([i])
                        del segments[ind][ind1]
                        flag=1
                        # print('no match')
                        break
                    elif max[1]==max[2]:
                        # print("no change")
                        continue
                    else:
                        segments[max[2]].append(i)
                        del segments[ind][ind1]
                        flag=1
                        # print('some match')
                        # print(segments)
                        break
                if flag==1:
                    segments=[sorted(x) for x in segments]
                    # print(segments)
                    segments.sort()
                    # print(segments)
                    break
            if flag==0:
                break
                
        # print('After Loop',segments)
        ln=[]
        for i in range(len(segments)):
            ln.append(len(segments[i]))
            mean_curr=np.mean(segments[i])
            # print(mean_curr,len(segments[i]))
            segments[i] = mean_curr
        # print(segments,ln)
        
        segments=np.average(segments,weights=ln)

        return segments

    def plot_pitch(self,audio_file,full=0):
        # Load audio file
        y, sr = librosa.load(audio_file)

        # Estimate pitch
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))


        # Create time axis
        hop_length = 512  # Adjust according to your preference
        t = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=hop_length)

        if full==1:
            return [x for x in f0 if not (math.isnan(x))]

        # print(f0)
        segments = self.segment_stepwise_increase(f0)
        # print(segments)       

        return segments
    
    def compare(self):
        Responce={}
        max=999999999
        indexPitch=-1
        for key in self.shruti.keys():
            if abs(self.shruti[key]-self.sa_freq)<max or abs((self.shruti[key]*2)-self.sa_freq)<max or abs((self.shruti[key]/2)-self.sa_freq)<1:
                max=abs(self.shruti[key]-self.sa_freq)
                indexPitch=key
        Responce['Pitch']=indexPitch

        count={}
        totCount=0
        for i in self.freq:
            max=999999999
            index=-1
            for key in self.final_ratio.keys():
                if abs((self.final_ratio[key]*self.sa_freq)-i)<max:
                        max=abs((self.final_ratio[key]*self.sa_freq)-i)
                        index=key
                        
        #     print(f"Swara is: {index}, actual: {i}, expected: {final_ratio[index]*sa_frq}, diff={abs((final_ratio[index]*sa_frq)-i)} ")
            if index not in count.keys():
                count[index]=1
                totCount+=1
            else:
                count[index]+=1
                totCount+=1

        Responce['Ragas']={}
        for key in self.ragas.keys():
            percentCount=0
            for sw in self.ragas[key]:
                if sw in count.keys():
                    percentCount+=count[sw]
            Responce["Ragas"][key]=round(((percentCount/totCount)*100),4)

        print(count)
        keys = list(Responce["Ragas"].keys())
        values = list(Responce["Ragas"].values())
        sorted_value_index = np.argsort(values)[::-1]
        Responce["Ragas"] = {keys[i]: values[i] for i in sorted_value_index}
        return Responce
    
    def compareSwara(self):
        Responce={}
        max=np.inf
        indexPitch=-1
        for key in self.shruti.keys():
            if abs(self.shruti[key]-self.sa_freq)<max or abs((self.shruti[key]*2)-self.sa_freq)<max or abs((self.shruti[key]/2)-self.sa_freq)<1:
                max=abs(self.shruti[key]-self.sa_freq)
                indexPitch=key
        Responce['Pitch']=indexPitch

        max=np.inf
        index=-1
        for key in self.final_ratio.keys():
            if abs((self.final_ratio[key]*self.sa_freq)-self.freq)<max:
                    max=abs((self.final_ratio[key]*self.sa_freq)-self.freq)
                    index=key
        Responce['Swara']=index
        return Responce

    def get_dict(self):
        self.response=self.compare()
        return self.response

    def get_dict1(self):
        self.response=self.compareSwara()
        return self.response


            