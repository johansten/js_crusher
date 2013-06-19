
import js_crusher

#-------------------------------------------------------------------------------

script ="\
	c.width=400;\
	c.height=300;\
	var d=new Image;\
	d.src='disturb.jpg';\
	d.addEventListener('load',function(){\
		e=document.createElement('canvas');\
		e.width=this.width;\
		e.height=this.height;\
		f=e.getContext('2d');\
		f.drawImage(this,0,0);\
		e=f.getImageData(0,0,this.width,this.height);\
		f=a.getImageData(0,0,c.width,c.height);\
		for(var i=0,y=c.height;y--;)\
			for(var x=c.width;x--;)\
				v=k[i++],\
				f.data[4*i-4]=e.data[4*v+0],\
				f.data[4*i-3]=e.data[4*v+1],\
				f.data[4*i-2]=e.data[4*v+2],\
				f.data[4*i-1]=e.data[4*v+3];\
		a.putImageData(f,0,0);\
	},!1);\
	var k=Array(c.width*c.height);\
	for(var i=0,y=c.height;y--;)\
		for(var x=c.width;x--;)\
			k[i++]=(5120/Math.sqrt((x-200)*(x-200)+(y-150)*(y-150))&255)<<8|(128*(Math.atan2(y-150,x-200)/Math.PI)&255);"

#-------------------------------------------------------------------------------

def preprocess(script):

	script = ' '.join(script.split())
	script = script.replace("; ", ";")
	script = script.replace("} ", "}")
	script = script.replace("{ ", "{")
	script = script.replace(", ", ",")
	script = script.replace(") ", ")")
#	script = script.replace(";)", ")")

	return script

#-------------------------------------------------------------------------------

def main():

	global script

	script = preprocess(script)
	length = len(script)
	script = js_crusher.crush(script)

	print script
	print "----"
	print "%d/%d" % (len(script), length)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
	main()

#-------------------------------------------------------------------------------
