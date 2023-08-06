from flask import json
from PyQt5 import QtWidgets
from collections import OrderedDict
import socketio,requests,functools
class socketController():
	sio = socketio.Client()
	monitorWidgets=OrderedDict()
	remoteAccessWidgetSetter = OrderedDict()
	monitorWidgetsCallbacks = {}
	parent = None
	activeroom = None
	autotransmit = False
	graphWidgetValues = {}
	graphConnections = [] #Signals to autoupdate graphs
	def __init__(self, parent):
		self.url = ''
		self.socketurl = ''
		self.parent  = parent
	
	def connect(self,homeurl, creds):
		self.url = homeurl
		self.socketurl = self.url.replace('https','wss')
		print('connecting to %s and sockets at %s'%(self.url, self.socketurl))
		session = requests.session()
		#creds.update({'myname':'j'})
		r = session.post(homeurl+'/login', creds, verify=False) #,headers={'User-Agent': 'Chrome'}
		if r.status_code == 200:
			token = 'remember_token='
			token += session.cookies['remember_token']
			token += '; session='
			token += session.cookies.get('session',domain = self.url.replace('https://',''))
			self.sio.connect(self.socketurl,headers={'Cookie': token}, namespaces=['/classroom'])
			print('connected to socket',self.socketurl)
			return self.sio
		else:
			print('invalid status code returned on login',r.status_code)

		return None

	def addHandler(self,event,function):
		self.sio.on(event, function, namespace='/classroom')

	def joinRoom(self,room,callback,**kwargs):
		data = {'room':room}
		data['widgets'] = self.monitorWidgets
		data.update(kwargs)
		self.sio.emit('join',data,namespace='/classroom',callback = functools.partial(callback,room) )

	def leaveRoom(self,room,callback,**kwargs):
		data = {'room':room}
		data['widgets'] = self.monitorWidgets
		data.update(kwargs)
		self.sio.emit('leave',data,namespace='/classroom',callback = functools.partial(callback,None) )


	def transmitWidgets(self,**kwargs):
		if not self.activeroom:return

		data = {'room':self.activeroom}
		data['widgets'] = self.monitorWidgets
		data.update(kwargs)
		self.sio.emit('widget list',data,namespace='/classroom')


	def set_device_id(self,devID):
		'''
		this will set the device ID(versio) in the database
		'''
		self.sio.emit('set device id',{'id':devID},namespace='/classroom')

	def sendInformation(self,info):
		'''
		this will be relayed to the owners of all the rooms this user is in
		'''
		self.sio.emit('chatter',info,namespace='/classroom')


	def addMonitors(self,widgets,**kwargs):
		'''
		Widgets which the teacher can monitor in real time
		'''
		for a in widgets:
			self.addMonitor(a,**kwargs)

	def setLabelText(self,label,data):
		label.setText(data['value'])
	def setCbxState(self,cbx,data):
		cbx.setChecked(data['value'])
	def setSliderValue(self,sldr,data):
		sldr.setValue(int(data['value']))
	def setComboState(self,combo,data):
		combo.setCurrentIndex(int(data['value']))
	def animateButtonClick(self,btn,data): #data param ignored for consistency
		btn.animateClick()
	def setDioState(self,dio,data):
		dio.setState(data['value'])

	def addMonitor(self,a,**kwargs):
		'''
		Widgets which the teacher can monitor in real time
		'''
		if (len(a.objectName())==0 ):
			return
		
		if isinstance(a,QtWidgets.QLabel):
			self.monitorWidgets[a.objectName()]={'widget':'label','text':a.text()}
			self.remoteAccessWidgetSetter[a.objectName()] = functools.partial(self.setLabelText,a)

		elif isinstance(a,QtWidgets.QCheckBox):
			self.monitorWidgets[a.objectName()]={'widget':'checkbox','text':a.text()}
			self.remoteAccessWidgetSetter[a.objectName()] = functools.partial(self.setCbxState,a)

		elif isinstance(a,QtWidgets.QSlider):
			self.monitorWidgets[a.objectName()]={'widget':'slider','value':a.value(),'min':a.minimum(),'max':a.maximum()}
			self.remoteAccessWidgetSetter[a.objectName()] = functools.partial(self.setSliderValue,a)

		elif isinstance(a,QtWidgets.QComboBox):
			self.monitorWidgets[a.objectName()]={'widget':'combobox','value':[a.itemText(i) for i in range(a.count())]}
			self.remoteAccessWidgetSetter[a.objectName()] = functools.partial(self.setComboState,a)

		elif isinstance(a,QtWidgets.QPushButton):
			self.monitorWidgets[a.objectName()]={'widget':'button','text':str(a.text())}	
			self.remoteAccessWidgetSetter[a.objectName()] = functools.partial(self.animateButtonClick,a)

		elif 'PlotWidget' in str(a.__class__):
			self.monitorWidgets[a.objectName()]={'widget':'graph','xlabel':a.plotItem.getAxis('bottom').labelText,'ylabel':a.plotItem.getAxis('left').labelText}	
			for b in a.plotItem.listDataItems():
				b.sigPlotChanged.connect(functools.partial(self.updatePlot,a.objectName(),b))
				self.graphConnections.append(b)
		elif ".DIO'" in str(a.__class__):			#DIO widget from KuttyPy
			self.monitorWidgets[a.objectName()]={'widget':'dio','value':a.getState()}	
			self.remoteAccessWidgetSetter[a.objectName()] = functools.partial(self.setDioState,a)
		elif ".DIOADC'" in str(a.__class__):			#DIO widget from KuttyPy
			self.monitorWidgets[a.objectName()]={'widget':'dioadc','value':a.getState()}	
			self.remoteAccessWidgetSetter[a.objectName()] = functools.partial(self.setDioState,a)
		elif ".DIOPWM'" in str(a.__class__):			#PWM widget from KuttyPy
			self.monitorWidgets[a.objectName()]={'widget':'diopwm','value':a.getState()}	
			self.remoteAccessWidgetSetter[a.objectName()] = functools.partial(self.setDioState,a)
		else:
			print(' UNKNOWN WIDGET: ',str(a.__class__))
			return False


		if a.property("remote"):
			self.monitorWidgets[a.objectName()].update({'remote':a.property("remote")})

		self.monitorWidgets[a.objectName()].update(kwargs) #Override with any keyword arguments

	def executeRemoteCallback(self,data):
		self.remoteAccessWidgetSetter[data['widget']](data)

	def disconnectGraphConnections(self):
		for a in self.graphConnections:
			print('disconnecting',a)
			a.sigPlotChanged.disconnect()
		self.graphConnections = []
		self.graphWidgetValues = {}


	def graphChanged(self,graph): #This function is called when the graph is altered (range) . It disconnects all signals, and new data items to signals.
		self.disconnectGraphConnections()
		for b in graph.plotItem.listDataItems():
			b.sigPlotChanged.connect(functools.partial(self.updatePlot,graph.objectName(),b, ))
			self.graphConnections.append(b)
		print('something changed with the graph',self.graphConnections)

	def truncateFloats(self,obj,decimals=2):
		return json.loads(json.dumps(obj), parse_float=lambda x: round(float(x), decimals) )

	def updatePlot(self,name,plotDataItem):
		if not self.parent.autographtransmit: return
		if 'PlotDataItem' in str(plotDataItem.__class__):
			if(len(plotDataItem.curve.xData)<=2): return
			self.graphWidgetValues = [self.truncateFloats(plotDataItem.curve.xData.tolist()),self.truncateFloats(plotDataItem.curve.yData.tolist())]
		elif 'PlotCurveItem' in str(plotDataItem.__class__):
			if(len(plotDataItem.xData)<=2): return
			self.graphWidgetValues = [self.truncateFloats(plotDataItem.xData.tolist()),self.truncateFloats(plotDataItem.yData.tolist())]
		self.parent.webhandler.sendData(json.dumps({name:{'widget':'graph','value':self.graphWidgetValues}}))

	def addMonitorSpacer(self,unique_name,classattr=''):
		self.monitorWidgets[unique_name]={'widget':'spacer','value':classattr}	

	def addMonitorVariable(self,unique_name,target,getDataFunction,**kwargs):
		self.monitorWidgets[unique_name]={'widget':target}
		self.monitorWidgets[unique_name].update(kwargs)
		self.monitorWidgetsCallbacks[unique_name] = getDataFunction

	def getWidgetValues(self):
		self.widgetValues = {}
		for a in self.monitorWidgets:
			widgetType = self.monitorWidgets[a]['widget']
			widget = self.parent.findChild(QtWidgets.QWidget, a)
			if widgetType == 'label':
				self.widgetValues[a] = {'widget':widgetType,'text':widget.text()}
			elif widgetType == 'checkbox':
				self.widgetValues[a] = {'widget':widgetType,'value':widget.isChecked(),'text':widget.text()}
			elif widgetType == 'combobox':
				self.widgetValues[a] = {'widget':widgetType,'value':widget.currentIndex(),'text':str(widget.currentText())}
			elif widgetType == 'slider':
				self.widgetValues[a] = {'widget':widgetType,'value':widget.value()}
			elif widgetType == 'button':
				self.widgetValues[a] = {'widget':widgetType,'text':widget.text()}
			elif widgetType == 'combobox':
				self.widgetValues[a] = {'widget':widgetType,'value':widget.currentIndex()}
			elif widgetType in ['dio','dioadc','diopwm']:			#DIO / DIOADC / DIOPWM widget from KuttyPy
				self.widgetValues[a] = {'widget':widgetType,'value':widget.getState()}
			elif widgetType == 'graph':
				graphvals = [] #dummy
				xlen = 0
				for b in widget.plotItem.listDataItems():
					if 'PlotDataItem' in str(b.__class__):
						if(len(b.curve.xData)<=2):
							continue #Invalid xdata. minimum 2 points required.
						if(not len(graphvals)):
							graphvals.append(self.truncateFloats(b.curve.xData.tolist()))
							xlen = len(graphvals[-1])
						graphvals.append(self.truncateFloats(b.curve.yData.tolist()))
						#tval = {"x":b.curve.xData.tolist(),"y":b.curve.yData.tolist()}
					elif 'PlotCurveItem' in str(b.__class__):
						if(len(b.xData)<=2):
							continue
						if(not len(graphvals)):
							graphvals.append(self.truncateFloats(b.xData.tolist()))
							xlen = len(graphvals[-1])
						graphvals.append(self.truncateFloats(b.yData.tolist()))
						#tval = {"x":b.xData.tolist(),"y":b.yData.tolist()}
				self.widgetValues[a] = {'widget':widgetType,'value':graphvals} # graphvals ...[x1,y1,y2,y3...]
			elif widgetType in ['combobox','button','spacer']:
				pass #widgetValues[a] = [widgetType,parent.findChild(QtWidgets.QSlider, a).value()]
			else:
				self.widgetValues[a] = {'widget':widgetType,'value':self.monitorWidgetsCallbacks[a]()} #widget in ['label']
		return self.widgetValues

	def transmitWidgetValues(self,widgetValues,**kwargs):
		if not self.activeroom:return

		data = {'room':self.activeroom}
		data.update(kwargs)

		data['widget values'] = widgetValues
		
		self.sio.emit('widget values',data,namespace='/classroom')

	def clearMonitors(self):
		self.monitorWidgets = OrderedDict()
		self.monitorWidgetsCallbacks = {}

	def getScriptList(self,url):
		#self.sio.emit('script list',{},setScriptList,namespace='/classroom')
		r = requests.get(url+'/getStaticData',{'data':'scripts'} ,verify=False)
		if r.status_code == 200:
			return r.json()
		else:
			print('invalid status code returned on login',r.status_code)
			return {}

