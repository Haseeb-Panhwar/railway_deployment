from django.shortcuts import render,redirect
from speechtool.forms import audioForm
from speechreview.settings import MEDIA_DIR,STATIC_DIR
import assemblyai as aai
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
aai.settings.api_key = os.environ['API']

# Create your views here.
sentiment_list = []
sentiment_dict = {'text':'','sentiment':'','confidence':0,'index':0}
context_results = {'sentiment_list':sentiment_list,'overall_confidence':0}
def index(request):
    form = audioForm()
    context_results['sentiment_list']=[]
    sentiment_list=[]
    if request.method == 'POST':
        aud_form = audioForm(data=request.POST)
        
        if aud_form.is_valid():
            aud_f = aud_form.save(commit=False)
            if 'audio_file' in request.FILES:
                aud_f.audio_file = request.FILES['audio_file']
                print("TestTTTTTTTTTTTTTTTTTT")
                aud_f.save()
                aud_f.audio_name = str(aud_f.pk)+"_"+str(aud_f.audio_file.name)
                audio_url = os.path.join(MEDIA_DIR,aud_f.audio_file.name)
                config = aai.TranscriptionConfig(sentiment_analysis=True)
                transcript = aai.Transcriber().transcribe(audio_url, config)
                overall_confidence = 0
                count = pos= neg = neu=0
                os.remove(audio_url)
                
                for sentiment_result in transcript.sentiment_analysis:
                    print(sentiment_result.text)
                    sentiment_dict['text'] = sentiment_result.text
                    print(sentiment_result.sentiment)  # POSITIVE, NEUTRAL, or NEGATIVE
                    sentiment_dict['sentiment'] = (sentiment_result.sentiment).lstrip('SentimentType.')
                    if sentiment_dict['sentiment'].lower() == 'positive':
                        pos+=1
                    elif sentiment_dict['sentiment'].lower() == 'negative':
                        neg+=1
                    else:
                        neu+=1
                    print(sentiment_result.confidence)
                    sentiment_dict['confidence'] = round(sentiment_result.confidence,2)
                    overall_confidence+=sentiment_result.confidence
                    print(f"Timestamp: {sentiment_result.start} - {sentiment_result.end}")
                    count+=1
                    sentiment_dict['index'] = count
                    sentiment_list.append(sentiment_dict.copy())
                    aud_f.positive = pos
                    aud_f.negative = neg
                    aud_f.neutral = neu
                context_results['sentiment_list']=sentiment_list
                oc = round(overall_confidence/len(transcript.sentiment_analysis),2)
                context_results['overall_confidence'] = oc
                aud_f.confidence = oc
                aud_f.save()
                print("Overall Confidence Score: ",oc)
                return redirect(results) 
                
        else:
            print(aud_form.errors)
    else:
        aud_form = audioForm()
    context = {"form":form}
    return render(request,"speechtool/index.html",context=context)

def results(request):
    df = pd.DataFrame(context_results['sentiment_list'],columns=['index','text','sentiment','confidence'])
    sns.set_palette('RdGy')
    print(df.head())
    catplot = os.path.join(os.path.join(STATIC_DIR,'images'),'catplot.png')
    relplot = os.path.join(os.path.join(STATIC_DIR,'images'),'relplot.png')
    
    if os.path.exists(catplot) and os.path.exists(relplot):
        os.remove(catplot)
        os.remove(relplot)

    count_plot = sns.catplot(data=df,kind='count',x='sentiment')
    count_plot.savefig(catplot)
    line_plot = sns.relplot(data=df,kind='line',x='index',y='confidence')
    line_plot.savefig(relplot)
    
    return render(request,"speechtool/results.html",context_results)