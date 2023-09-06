# MainApp/views.py

import csv
import json
import asyncio
from django.shortcuts import render, HttpResponse
from .forms import CSVUploadForm
from .models import Candle

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            timeframe = form.cleaned_data['timeframe']
            # Store the CSV file on the server
            with open(f'media/{csv_file.name}', 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)
            # Process the CSV file and convert to JSON
            asyncio.run(process_csv_to_json(csv_file.name, timeframe))
            return HttpResponse("File uploaded and processed successfully. <a href='/download/'>Download JSON</a>")
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})

async def process_csv_to_json(filename, timeframe):
    # Read the CSV file and convert to Candle objects
    candles = []
    with open(f'media/{filename}', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            candle = Candle(
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                date=row['date']
            )
            candles.append(candle)

    # Convert to the given timeframe and store as JSON
    # Implement your timeframe conversion logic here

    # Store the JSON data
    json_data = [candle.__dict__ for candle in candles]
    with open(f'media/output.json', 'w') as json_file:
        json.dump(json_data, json_file)
