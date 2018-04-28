import skfmm 
import numpy as np 
import pylab as plt 
import os

from flask import Flask, request, render_template 


app = Flask(__name__)

@app.route("/") 
def api290I():
	date = request.args.get('date')
	n = int(request.args.get('n'))
	r = requests.get('https://ce290-hw5-weather-report.appspot.com/', params={'date': date}) dict = r.json()
	centroid_x=dict['centroid_x']
	centroid_y=dict['centroid_y']
	radius=dict['radius']
	result=shortpath(centroid_x,centroid_y,radius,n)
	img_path = 'static/path.png'
	return render_template('index.html', img_path = img_path, shortest_dist = result)

def shortpath(centroid_x,centroid_y,radius,n): 
	phi=np.ones((n+1,n+1))
	phi[0,0]=0
	X, Y = np.meshgrid(np.linspace(0,20,n+1), np.linspace(0,20,n+1)) mask = (X-centroid_x)**2+(Y-centroid_y)**2<=radius**2
	phi = np.ma.MaskedArray(phi, mask) d1=skfmm.distance(phi,dx=20/n) phi[0,0]=1
	phi[n,n]=0 d2=skfmm.distance(phi,dx=20/n) d=d1+d2
	i=0
	j=0
	step=20/n
	x_path=[0]
	y_path=[0]
	x=0
	y=0
	plt.title('Shortest path from A to B')

	while i!=n and j!=n:
		m=min(d[i][j+1],d[i+1][j],d[i+1][j+1]) 
		if m==d[i+1][j]:
			i+=1
		    x+=step
		    x_path.append(x) 
		    y_path.append(y)
	    elif m==d[i+1][j+1]:
		    i+=1 
		    j+=1 
		    x+=step 
		    y+=step
		    x_path.append(x) 
		    y_path.append(y)
	    else: 
		    j+=1
		    y+=step 
		    x_path.append(x) 
		    y_path.append(y)
     plt.contour(X, Y, d1, 40)
     plt.colorbar()
     plt.plot(y_path,x_path,'r')

img_path = 'static/path.png'
if os.path.isfile(img_path):
os.remove(img_path) 
plt.savefig(img_path) 
plt.close('all')
return (d1[n][n])

if __name__ == '__main__': 
	app.run(host="0.0.0.0",port=5000)