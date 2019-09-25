from flask import render_template, Flask, request
from flask import send_from_directory,url_for
import os
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import json
import pickle
app = Flask(__name__)  

def build_graph(x_coordinates, y_coordinates):
    
    img = io.BytesIO()
    plt.plot(x_coordinates, y_coordinates)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

def make_dict(filename):
    
    path = "Session2/dialog/transcriptions/%s.txt"%filename[0:14]
    d = open(path)
    text = d.readlines()
    li_ = []
    for i in text:
        li_.append((i.split(" ")[0], i[41:]))
    path_ = "Session2/dialog/EmoEvaluation/Categorical/%s_e2_cat.txt"%filename[0:14]
    d_ = open(path_)
    text_ = d_.readlines()
    dic = {}
    for i in text_:
        dic[i.split(":")[0].strip()] = i.split(":")[1].split(";")[0]
    return (dic,li_)

def create_li(dic, li_):
    
    g = " "
    y_f = []
    y_m = []
    sess = []
    speaker_li = []
    emo_li = []
    text_li = []
    first = True
    for i in li_ :
        while first == True:
            first = False
            break
        sub_d = {}
        try:
            if i[0][15] == "F":
                g = "Female"
                y_f.append(dic[i[0]])
            elif i[0][15] == "M":
                g = "Male"
                y_m.append(dic[i[0]])
            sub_d["Speaker"] = g
            speaker_li.append(g)
            sub_d["Emo"] = dic[i[0]]
            emo_li.append(dic[i[0]])
            sub_d["Text"] = i[1]
            text_li.append(i[1])
            sess.append(sub_d)
            
            del(sub_d)
        except Exception as e:
            print(e)
            pass
    np.save("f_1.npy",y_f)
    np.save("m_1.npy",y_m)
    return(speaker_li,emo_li,text_li)
    
def load_obj(name ):
    
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
def save_obj(obj, name ):
    
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
@app.route('/')  
def upload():  
    
    return render_template("file.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    
    if request.method == 'POST':  
        f = request.files['file']
        f.save("C:\\Users\\AkhileshPatil\\Desktop\\AudioEmo\\Flask_V1\\static\\mp3\\"+f.filename)
        sess_dic = make_dict(f.filename)
        li = create_li(sess_dic[0], sess_dic[1])
        return render_template("success.html", name = f.filename, emo = li[1], speaker = li[0], text = li[2])  
    
@app.route('/foo', methods=['GET', 'POST'])
def foo(x=None, y=None):
    
    y1 = np.load("m_1.npy")
    y2 = np.load("f_1.npy")
    x1 = []
    x2 = []
    for i in range(len(y1)):
        x1.append(i)
    for j in range(len(y2)):
        x2.append(j)
    graph1_url = build_graph(x1,y1);
    graph2_url = build_graph(x2,y2);
    return render_template("stop.html",graph1=graph1_url,graph2=graph2_url)

if __name__ == "__main__":
    app.run(debug=True,use_reloader = False)