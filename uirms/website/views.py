import json
from django.http import HttpResponse, JsonResponse
import networkx as nx
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from .forms import SignUpForm
from .models import UserRecord, POI, User
import osmnx as ox
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
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
    # Fetch all POI objects for initial rendering
    name = POI.objects.all()

    # Check if the form is submitted
    if request.method == 'POST':
        # Get the names of start and destination from the form
        start_location_name = request.POST.get('start_location', '')
        destination_location_name = request.POST.get('destination_location', '')
        net_type = request.POST.get('network_type', '')

        # Check if the checkbox is checked
        if request.POST.get('start_location_latitude') == '':
            try:
                # Fetch POI object for the start location based on the name
                start_venue = get_object_or_404(POI, name=start_location_name)

                # Use the latitude and longitude from the database for the start location
                latitude_start, longitude_start = start_venue.latitude, start_venue.longitude

                # Fetch POI object for the destination location based on the name
                destination_venue = get_object_or_404(POI, name=destination_location_name)

                # Use the latitude and longitude from the database for the destination location
                latitude_end, longitude_end = destination_venue.latitude, destination_venue.longitude
                
                latitude = 7.4477245
                longitude = 3.8967116 
                nt = net_type
                
                distanc = 2500  # 1 kilometer
                graph = ox.graph_from_point((latitude, longitude), dist=distanc, network_type=nt)

                # Find the nearest network nodes to the starting and ending points
                start_node = ox.distance.nearest_nodes(graph, X=longitude_start, Y=latitude_start)
                end_node = ox.distance.nearest_nodes(graph, X=longitude_end, Y=latitude_end)

                # Calculate the shortest path using Dijkstra's algorithm
                shortest_path = nx.shortest_path(graph, source=start_node, target=end_node, weight="length")


                # Calculate basic network statistics
                basic_stats = ox.basic_stats(graph)

                # Extract edge attributes from the network graph
                edge_attributes = ox.graph_to_gdfs(graph, nodes=False).columns

                coordinates = [(graph.nodes[node_id]['y'], graph.nodes[node_id]['x']) for node_id in shortest_path]

                # Construct the context
                context = {
                    'network_type': nt,
                    # 'latitude_start': latitude_start,
                    # 'longitude_start': longitude_start,
                    # 'latitude_end': latitude_end,
                    # 'longitude_end': longitude_end,
                    # 'shortest_path': shortest_path,
                    'coordinates': coordinates,
                }
                
                print(context)
                
            except POI.DoesNotExist:
                return JsonResponse({'error': 'Location Not Found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            # If the checkbox is checked, retrieve location data directly
            lat = request.POST.get('start_location_latitude', '')
            lon = request.POST.get('start_location_longitude', '')
            network_type = request.POST.get('network_type', '')
            
            longitude_start = float(lon)
            latitude_start = float(lat)

            # Fetch POI object for the destination location based on the name
            destination_venue = get_object_or_404(POI, name=destination_location_name)
            
            # Use the latitude and longitude from the database for the start location

            # Use the latitude and longitude from the database for the destination location
            latitude_end, longitude_end = destination_venue.latitude, destination_venue.longitude

            latitude = 7.4477245
            longitude = 3.8967116 
            nt = net_type
            print(nt)
            
            distanc = 2500  # 1 kilometer
            graph = ox.graph_from_point((latitude, longitude), dist=distanc, network_type=nt)

            # Find the nearest network nodes to the starting and ending points
            start_node = ox.distance.nearest_nodes(graph, X=longitude_start, Y=latitude_start)
            end_node = ox.distance.nearest_nodes(graph, X=longitude_end, Y=latitude_end)

            # Calculate the shortest path using Dijkstra's algorithm
            shortest_path = nx.shortest_path(graph, source=start_node, target=end_node, weight="length")


            # Calculate basic network statistics
            basic_stats = ox.basic_stats(graph)

            # Extract edge attributes from the network graph
            edge_attributes = ox.graph_to_gdfs(graph, nodes=False).columns

            coordinates = [(graph.nodes[node_id]['y'], graph.nodes[node_id]['x']) for node_id in shortest_path]

            # Construct the context
            context = {
                'network_type': nt,
                # 'latitude_start': latitude_start,
                # 'longitude_start': longitude_start,
                # 'latitude_end': latitude_end,
                # 'longitude_end': longitude_end,
                # 'shortest_path': shortest_path,
                'coordinates': coordinates,
            }
            
            print(context, 'currentloc')

    return render(request, 'route.html', context)


def recrouting(request):
    if request.method == 'POST':
        lon_end = request.POST.get('end_location_longitude', '')
        lat_end = request.POST.get('end_location_latitude', '')
        lon = request.POST.get('start_location_longitude', '')
        lat = request.POST.get('start_location_latitude', '')

        # Check if start_location_latitude and start_location_longitude are not empty
        if lon and lat:
            try:
                lon_start = float(lon)
                lat_start = float(lat)

                latitude_start, longitude_start = lat_start, lon_start
                latitude_end, longitude_end = float(lat_end), float(lon_end)

                latitude = 7.4477245
                longitude = 3.8967116
                distance = 2500  # 1 kilometer
                graph = ox.graph_from_point((latitude, longitude), dist=distance, network_type="all")

                # Find the nearest network nodes to the starting and ending points
                start_node = ox.distance.nearest_nodes(graph, X=longitude_start, Y=latitude_start)
                end_node = ox.distance.nearest_nodes(graph, X=longitude_end, Y=latitude_end)

                # Calculate the shortest path using Dijkstra's algorithm
                shortest_path = nx.shortest_path(graph, source=start_node, target=end_node, weight="length")

                # Calculate basic network statistics
                basic_stats = ox.basic_stats(graph)

                # Extract edge attributes from the network graph
                edge_attributes = ox.graph_to_gdfs(graph, nodes=False).columns

                coordinates = [(graph.nodes[node_id]['y'], graph.nodes[node_id]['x']) for node_id in shortest_path]

                # Construct the context
                context = {
                    'coordinates': coordinates,
                }

                return render(request, 'route.html', context)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            # Handle the case where start_location_latitude or start_location_longitude is empty
            return JsonResponse({'error': 'Start location data missing'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

         

    
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
	categories = {'Dining': 'fork', 'Sports': 'trophy', 'ATM & Bank': 'cash', 'Parks and Recreation': 'tree', 'Events': 'bank'}
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
		return render(request, 'index.html', {'records':records, 'categories':categories})
	
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

class LocationSearchView(View):
	def get(self, request, *args, **kwargs):
		try:
			query = request.GET.get('query', '')
			results = POI.objects.filter(name__icontains=query)[:5]
			suggestions = [{'id': venue.id, 'name': venue.name} for venue in results]
			return JsonResponse({'suggestions': suggestions})
		except Exception as e:
			return JsonResponse({'error': str(e)}, status=500)

def GetSearchLocationA(request, name, latitude, longitude):
    
    return render(request, 'search.html', {'latitude': latitude, 'longitude': longitude, 'name': name})

def GetSearchLocation(request):
	name = POI.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		name = request.POST['name']
	try:
	# Assuming 'name' is a unique field in your Item model
		venue = POI.objects.get(name=name)
		context = {'id': venue.id, 'name': venue.name, 'latitude': venue.latitude, 'longitude': venue.longitude}
		return render(request, 'search.html', context)
	except POI.DoesNotExist:
		return JsonResponse({'error': 'Location Not Found'}, status=404)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)
#     # Render your Django template or return a JSON response
# 	response_data = '\n'.join([f"{venue.name}: {venue.address} ({venue.latitude}, {venue.longitude})" for venue in venues])
# 	return HttpResponse(response_data)
# def get_category_icon(category):
#     # Implement a function to map categories to icons
#     icon_mapping = {
#         'Dining': 'utensils',
#         'Library': 'book',
#         'Parks & Recreation': 'tree',
#         'Theater': 'bank',
#         'Sports': 'trophy',
#         'Admin': 'briefcase',
#         'Bustop': 'bus-front',
#         'ATM & Bank': 'cash'
#         # Add more categories and icons as needed
#     }
#     return icon_mapping.get(category, 'question')  # Default to a question mark if category not found

def haversine(lat1, lon1, lat2, lon2):
    # Function to calculate Haversine distance
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (pow(sin(dlat / 2), 2) + cos(lat1) * cos(lat2) * pow(sin(dlon / 2), 2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def spatial_similarity(lat1, lon1, lat2, lon2):
    # Calculate spatial similarity based on Haversine distance
    distance = haversine(lat1, lon1, lat2, lon2)
    return 1 / (1 + distance)

def calculate_expected_location_score(target_user, location):
    # Function to calculate Expected Location Score (u, i)
    spatial_sim = spatial_similarity(target_user['latitude_x'], target_user['longitude_x'], location['latitude_y'], location['longitude_y'])
    distance_pref = location['pr']

    # Adjust as needed based on Distance Preference (u, v, i)
    if distance_pref == 0:  # No preference
        distance_pref_factor = 0.2
    elif distance_pref == 1:  # Shortcuts
        distance_pref_factor = 0.1  # Adjust the weight based on preference
    elif distance_pref == 2:  # Scenic routes
        distance_pref_factor = 0.4  # Adjust the weight based on preference
    else:
        distance_pref_factor = 0.2  # Default to no preference

    numerator = spatial_sim * distance_pref_factor
    denominator = spatial_sim

    return numerator / denominator if denominator != 0 else 0  # Avoid division by zero

def recommend_locations(request):
    
     if request.method == 'POST':
        # Get the selected category from the form
        cat_preference = request.POST.get('selected_category', '')
	# Load user and venue data from the PostgreSQL database
        user_data = User.objects.all().values('id', 'latitude', 'longitude', 'pr')
        venue_data = POI.objects.all().values('id','name', 'latitude', 'longitude', 'category', 'image')

        # Convert querysets to Pandas DataFrames
        user_data = pd.DataFrame.from_records(user_data)
        venue_data = pd.DataFrame.from_records(venue_data)
        # Check data types of columns
        # print(user_data.dtypes)
        # print(venue_data.dtypes)


        # Merge datasets based on latitude and longitude
        merged_data = pd.merge(user_data, venue_data, left_on='id', right_on='id', how='inner')
        # print(merged_data)


        # Specify the target user ID and location
        target_user_id = 33
        target_user_location = merged_data[merged_data['id'] == target_user_id].iloc[0]
        
        print(target_user_location)

        # Filter by category preference
        category_preference = cat_preference
        category_recommendations = merged_data[merged_data['category'] == category_preference]

        # Generate recommendations
        recommendations = []
        for index, row in category_recommendations.iterrows():
            location_score = calculate_expected_location_score(target_user_location, row)
            venue_name = row['name']
            latitude = row['latitude_y']
            longitude = row['longitude_y']
            image = row['image']
            recommendations.append({'name': venue_name, 'latitude': latitude, 'longitude': longitude, 'score': location_score, 'image': image})

        # Sort locations by expected location score
        sorted_recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)
            # Get the top recommendations
        top_recommendations = sorted_recommendations[:5]
        

        # Pass the recommendations to the template
        print(top_recommendations)
        print(category_preference)
        context = {'top_recommendations': top_recommendations, 'category': category_preference}
        return render(request, 'recommend.html', context)

def sl(request, latitude, longitude, name):
    # Your view logic here
    return render(request, 'sl.html', {'latitude': latitude, 'longitude': longitude, 'name': name})


def GoToLocation(request):
    if request.method == 'POST':
     lon_end = request.POST.get('end_location_longitude', '')
     lat_end = request.POST.get('end_location_latitude', '')
     name = request.POST.get('search_name', '')
     
     context = {'name': name, 'latitude': lat_end, 'longitude': lon_end}
     
     return render(request, 'search.html', context)