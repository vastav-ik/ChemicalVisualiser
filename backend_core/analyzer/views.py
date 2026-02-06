from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import AnalysisRecord
import pandas as pd
import json

class UploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.FILES['file']
        
        try:
            df = pd.read_csv(file_obj)
        except Exception as e:
            return Response({"error": "Invalid CSV file"}, status=400)

        required_cols = ['Type', 'Pressure', 'Temperature', 'Flowrate']
        if not all(col in df.columns for col in required_cols):
             return Response({"error": "CSV missing required columns"}, status=400)

        analysis_result = {
            "total_count": len(df),
            "avg_pressure": round(df['Pressure'].mean(), 2),
            "avg_temp": round(df['Temperature'].mean(), 2),
            "type_counts": df['Type'].value_counts().to_dict() 
        }

        if AnalysisRecord.objects.count() >= 5:
            oldest = AnalysisRecord.objects.order_by('created_at').first()
            oldest.file.delete()
            oldest.delete()      

        record = AnalysisRecord.objects.create(
            file=file_obj,
            summary_data=analysis_result
        )

        return Response(analysis_result)