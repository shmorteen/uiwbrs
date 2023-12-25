import json
from django.http import HttpResponse, JsonResponse
import networkx as nx
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from .forms import SignUpForm
from .models import UserRecord, Item, Venue
import osmnx as ox
import io
import requests
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# def retrieve_street_network(request):
    # lat = 7.4477245  # Latitude of your AOI
    # lon = 3.8967116  # Longitude of your AOI
    # G = ox.graph_from_point((lat, lon), network_type='driving')
    # print(G)
	
	# # Convert the MultiDiGraph to a JSON-serializable format (e.g., dictionary)
    # G_dict = nx.readwrite.json_graph.node_link_data(G)

    # return JsonResponse({'street_network_data': G})

def routing(request):
	# Define the coordinates for the starting and ending points
	latitude_start, longitude_start = 7.4416532, 3.9062510  # Replace with actual coordinates
	latitude_end, longitude_end = 7.4427070, 3.9006930  # Replace with actual coordinates

	# Define the coordinates (latitude and longitude) for the center point.
	latitude = 7.4477245
	longitude = 3.8967116 
	# Fetch OSM data within a specified distance (e.g., 1 km) from the center point.
	distanc = 1500  # 1 kilometer
	graph = ox.graph_from_point((latitude, longitude), dist=distanc, network_type="all")

	# Find the nearest network nodes to the starting and ending points
	start_node = ox.distance.nearest_nodes(graph, X=longitude_start, Y=latitude_start)
	end_node = ox.distance.nearest_nodes(graph, X=longitude_end, Y=latitude_end)

	# Calculate the shortest path using Dijkstra's algorithm
	shortest_path = nx.shortest_path(graph, source=start_node, target=end_node, weight="length")


	# Calculate basic network statistics
	basic_stats = ox.basic_stats(graph)

	# Extract edge attributes from the network graph
	edge_attributes = ox.graph_to_gdfs(graph, nodes=False).columns

	
	# Visualize the shortest path on the map
	# fig, ax = ox.plot_graph_route(graph, shortest_path, route_linewidth=6, node_size=0, bgcolor='k')
		# plt.show()
	# coordinates = [graph.nodes[node_id] for node_id in shortest_path]
	# x_coordinates = [coord['x'] for coord in coordinates]
	# y_coordinates = [coord['y'] for coord in coordinates]
	
	# print("X (Longitude) Coordinates:", x_coordinates)
	# print("Y (Latitude) Coordinates:", y_coordinates)

	coordinates = [(graph.nodes[node_id]['y'], graph.nodes[node_id]['x']) for node_id in shortest_path]
	# print(coordinates)

	# print("Shortest Path:", shortest_path)
	# print("Context",context)
	# print("Basic Network Statistics:", basic_stats)
	# print("Edge Attributes:", edge_attributes)
	# print("start_node:", start_node)
	# return HttpResponse("Shortest Path")
	context = {
        'latitude_start': latitude_start,
        'longitude_start': longitude_start,
        'latitude_end': latitude_end,
        'longitude_end': longitude_end,
        'shortest_path': shortest_path,
		'coordinates' : coordinates,
    }
	return render(request, 'route.html', context)
    
def retrieve_street_network(request):
	# Define the coordinates (latitude and longitude) for the center point.
	latitude = 7.4477245
	longitude = 3.8967116  
	# Fetch OSM data within a specified distance (e.g., 1 km) from the center point.
	distance = 1500  # 1.5 kilometer
	graph = ox.graph_from_point((latitude, longitude), dist=distance, network_type="all")

	# Visualize the data (optional).
	ox.plot_graph(ox.project_graph(graph))
	return HttpResponse("OSM data import completed successfully.")

# def retrieve_street_network(request):
# 	# lat = 7.4477245  # Latitude of your AOI
#     # lon = 3.8967116  # Longitude of your AOI
#     ox.settings.use_cache = True

#     # download street network data from OSM and construct a MultiDiGraph model
#     G = ox.graph.graph_from_point((7.4477245, 3.8967116), dist=750, network_type="drive")

#     # impute edge (driving) speeds and calculate edge travel times
#     G = ox.speed.add_edge_speeds(G)
#     G = ox.speed.add_edge_travel_times(G)

#     # you can convert MultiDiGraph to/from GeoPandas GeoDataFrames
#     gdf_nodes, gdf_edges = ox.utils_graph.graph_to_gdfs(G)
#     G = ox.utils_graph.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs=G.graph)

#     # convert MultiDiGraph to DiGraph to use nx.betweenness_centrality function
#     # choose between parallel edges by minimizing travel_time attribute value
#     D = ox.utils_graph.get_digraph(G, weight="travel_time")

#     # calculate node betweenness centrality, weighted by travel time
#     bc = nx.betweenness_centrality(D, weight="travel_time", normalized=True)
#     nx.set_node_attributes(G, values=bc, name="bc")

#     # plot the graph, coloring nodes by betweenness centrality
#     nc = ox.plot.get_node_colors_by_attr(G, "bc", cmap="plasma")
#     fig, ax = ox.plot.plot_graph(
#         G, bgcolor="k", node_color=nc, node_size=50, edge_linewidth=2, edge_color="#333333"
#     )

#     # save graph as a geopackage or graphml file
#     ox.io.save_graph_geopackage(G, filepath="./graph.gpkg")
#     ox.io.save_graphml(G, filepath="./graph.graphml")

#     return HttpResponse("Your view is working!")

# def retrieve_street_network(request):
#     G = ox.graph.graph_from_point((7.4477245, 3.8967116), dist=750, network_type="drive")
#     # Your other code for processing the network

#     # Plot the graph and save it as an image
#     fig, ax = ox.plot.plot_graph(
#         G, bgcolor="k", node_size=50, edge_linewidth=2, edge_color="#333333"
#     )

#     img_buffer = io.BytesIO()
#     plt.savefig(img_buffer, format="png")
#     img_buffer.seek(0)

#     response = HttpResponse(content_type="image/png")
#     response.write(img_buffer.read())
#     return response
	
# Create your views here.
def index(request):
	records = UserRecord.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('index')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('index')
	else:
		return render(request, 'index.html', {'records':records})
	
def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('index')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('index')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

class ItemSearchView(View):
    def get(self, request, *args, **kwargs):
        try:
            query = request.GET.get('query', '')
            results = Item.objects.filter(namee__icontains=query)[:5]
            suggestions = [{'id': item.id, 'namee': item.namee} for item in results]
            return JsonResponse({'suggestions': suggestions},)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
		
def GetSearchLocation(request):
	name = Item.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		name = request.POST['name']
	try:
		# Assuming 'name' is a unique field in your Item model
		item = Item.objects.get(namee=name)
		return render({'id': item.id, 'name': item.namee, 'lat': item.lat, 'lon': item.lon})
	except Item.DoesNotExist:
		return JsonResponse({'error': 'Location Not Found'}, status=404)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)
#     # Render your Django template or return a JSON response
# 	response_data = '\n'.join([f"{venue.name}: {venue.address} ({venue.latitude}, {venue.longitude})" for venue in venues])
# 	return HttpResponse(response_data)