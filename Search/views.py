from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from _collections import deque
from .engine import NewResult
#Begin-------------------------------------Server-Initialization------------------------------------Begin#
g_memory_pointer = 0
g_runtime_memory = []

class Search_Scene:
	def __init__(self,usrid):
		self.page = 0
		self.twitter_sid = 1
		self.query = ""
		self.usr_id = usrid
		self.search_results = []

for g_memory_pointer in range(0,100):
	new_scene = Search_Scene(-1)
	g_runtime_memory.append(new_scene)
#End---------------------------------------Server-Initialization--------------------------------------End#
def home_page(request):
	return render(request,'Search/home_page.html')

def find(request):
	if (request.method == 'GET'):
		return_uid = AllocateNewMemory(request.GET['query'])
		(page,search_results) = UsrReqPro(return_uid, 0)
	else:
		return_uid = request.session.get('visitor_id')
		if('P' in request.POST):
			action = -1
		else:
			action = 0
		(page,search_results) = UsrReqPro(return_uid, action)
	request.session['visitor_id'] = return_uid
	return render(request,'Search/find.html',{'result_list':search_results, 'page':page})


def UsrReqPro(return_id, action):
	# action == 1 : next, action == 0 : previous
	global g_runtime_memory
	for usr in range(0,100):
		if(return_id == g_runtime_memory[usr].usr_id):#find the user
			if(action == -1):#previous page, no more search here
				g_runtime_memory[usr].page -= 1
				return (g_runtime_memory[usr].page, g_runtime_memory[usr].search_results[((g_runtime_memory[usr].page - 1)* 20) : (g_runtime_memory[usr].page * 20)])	
			else:
				if(len(g_runtime_memory[usr].search_results) < 20 * (g_runtime_memory[usr].page + 1)):
					(new_result, g_runtime_memory[usr].twitter_sid) = NewResult(g_runtime_memory[usr].query, g_runtime_memory[usr].twitter_sid)#if there's a need to search
					g_runtime_memory[usr].search_results += new_result
				g_runtime_memory[usr].page += 1
				return (g_runtime_memory[usr].page, g_runtime_memory[usr].search_results[((g_runtime_memory[usr].page - 1)* 20) : (g_runtime_memory[usr].page * 20)])
	return None

def AllocateNewMemory(query):
	global g_runtime_memory
	global g_memory_pointer
	g_runtime_memory[(g_memory_pointer % 100)].usr_id = g_runtime_memory[((g_memory_pointer - 1) % 100)].usr_id + 100
	g_runtime_memory[(g_memory_pointer % 100)].page = 0
	g_runtime_memory[(g_memory_pointer % 100)].query = query
	g_runtime_memory[(g_memory_pointer % 100)].search_results = []
	g_memory_pointer += 1
	return g_runtime_memory[((g_memory_pointer - 1) % 100)].usr_id