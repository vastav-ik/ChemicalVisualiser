from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import AnalysisRecord
import pandas as pd
import json
from django.http import HttpResponse, FileResponse
from rest_framework.permissions import IsAuthenticated
from .utils import generate_pdf_report

class UploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

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
            oldest = AnalysisRecord.objects.order_by('uploaded_at').first()
            if oldest:
                oldest.file.delete()
                oldest.delete()      

        record = AnalysisRecord.objects.create(
            file=file_obj,
            summary_data=analysis_result
        )

        return Response({
            "id": record.id,
            "uploaded_at": record.uploaded_at,
            "summary": analysis_result
        })

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = AnalysisRecord.objects.order_by('-uploaded_at')[:5]
        data = []
        for record in records:
            data.append({
                "id": record.id,
                "uploaded_at": record.uploaded_at,
                "summary": record.summary_data
            })
        return Response(data)

class AnalysisDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            record = AnalysisRecord.objects.get(pk=pk)
        except AnalysisRecord.DoesNotExist:
            return Response({"error": "Record not found"}, status=404)
        
        try:
            df = pd.read_csv(record.file.path)
            data = df.to_dict(orient='records')
            return Response(data)
        except Exception as e:
            return Response({"error": f"Error reading file: {str(e)}"}, status=500)

class PDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            record = AnalysisRecord.objects.get(pk=pk)
        except AnalysisRecord.DoesNotExist:
            return Response({"error": "Record not found"}, status=404)
            
        pdf_buffer = generate_pdf_report(record)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f'analysis_report_{pk}.pdf')
