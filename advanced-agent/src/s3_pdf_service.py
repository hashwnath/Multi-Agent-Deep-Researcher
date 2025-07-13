import boto3
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import PyPDF2
import pdfplumber
from io import BytesIO
from dotenv import load_dotenv
from .models import PDFDocument

load_dotenv()


class S3PDFService:
    """Service for handling PDF documents stored in S3"""
    
    def __init__(self, bucket_name: str = "athena-output-spotify11", region: str = "us-east-2"):
        self.bucket_name = bucket_name
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
    
    def list_pdfs(self, prefix: str = "Unsaved/2025/05/28/") -> List[Dict[str, Any]]:
        """List PDF files in S3 bucket with given prefix"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=50
            )
            
            pdf_files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    if obj['Key'].lower().endswith('.pdf'):
                        pdf_files.append({
                            'key': obj['Key'],
                            'size': obj['Size'],
                            'last_modified': obj['LastModified'],
                            'filename': obj['Key'].split('/')[-1]
                        })
            
            return pdf_files
        except Exception as e:
            print(f"Error listing PDFs: {e}")
            return []
    
    def download_pdf(self, s3_key: str) -> Optional[bytes]:
        """Download PDF file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response['Body'].read()
        except Exception as e:
            print(f"Error downloading PDF {s3_key}: {e}")
            return None
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract text content from PDF bytes"""
        try:
            # Try pdfplumber first (better for complex layouts)
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except Exception as e:
            print(f"pdfplumber failed, trying PyPDF2: {e}")
            try:
                # Fallback to PyPDF2
                pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
            except Exception as e2:
                print(f"PyPDF2 also failed: {e2}")
                return ""
    
    def get_pdf_metadata(self, s3_key: str) -> Dict[str, Any]:
        """Get metadata for a PDF file"""
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return {
                'content_type': response.get('ContentType', ''),
                'content_length': response.get('ContentLength', 0),
                'last_modified': response.get('LastModified'),
                'etag': response.get('ETag', ''),
                'metadata': response.get('Metadata', {})
            }
        except Exception as e:
            print(f"Error getting metadata for {s3_key}: {e}")
            return {}
    
    def process_pdf(self, s3_key: str) -> Optional[PDFDocument]:
        """Process a single PDF file from S3"""
        try:
            # Download PDF
            pdf_bytes = self.download_pdf(s3_key)
            if not pdf_bytes:
                return None
            
            # Extract text
            content = self.extract_text_from_pdf(pdf_bytes)
            if not content:
                print(f"No text extracted from {s3_key}")
                return None
            
            # Get metadata
            metadata = self.get_pdf_metadata(s3_key)
            
            # Create PDFDocument
            pdf_doc = PDFDocument(
                s3_key=s3_key,
                filename=s3_key.split('/')[-1],
                content=content,
                metadata=metadata,
                processed_at=datetime.now()
            )
            
            return pdf_doc
            
        except Exception as e:
            print(f"Error processing PDF {s3_key}: {e}")
            return None
    
    def find_relevant_pdfs(self, query: str, max_pdfs: int = 5) -> List[PDFDocument]:
        """Find and process PDFs relevant to the query"""
        try:
            # List all PDFs
            pdf_files = self.list_pdfs()
            
            if not pdf_files:
                print("No PDF files found in S3 bucket")
                return []
            
            print(f"Found {len(pdf_files)} PDF files in S3")
            
            # Process PDFs (for now, process all found PDFs)
            # In the future, we could add relevance scoring
            processed_pdfs = []
            for pdf_file in pdf_files[:max_pdfs]:
                print(f"Processing PDF: {pdf_file['filename']}")
                pdf_doc = self.process_pdf(pdf_file['key'])
                if pdf_doc:
                    processed_pdfs.append(pdf_doc)
                    print(f"✅ Successfully processed {pdf_file['filename']}")
                else:
                    print(f"❌ Failed to process {pdf_file['filename']}")
            
            return processed_pdfs
            
        except Exception as e:
            print(f"Error finding relevant PDFs: {e}")
            return [] 

    def list_available_pdfs(self) -> List[Dict[str, Any]]:
        """List all available PDFs with metadata for user selection"""
        try:
            pdf_files = self.list_pdfs()
            
            available_pdfs = []
            for pdf_file in pdf_files:
                # Get additional metadata
                metadata = self.get_pdf_metadata(pdf_file['key'])
                
                pdf_info = {
                    's3_key': pdf_file['key'],
                    'filename': pdf_file['filename'],
                    'size_mb': round(pdf_file['size'] / (1024 * 1024), 2),
                    'last_modified': pdf_file['last_modified'].strftime('%Y-%m-%d %H:%M'),
                    'content_length': metadata.get('content_length', 0),
                    'content_type': metadata.get('content_type', ''),
                    'user_metadata': metadata.get('metadata', {})
                }
                available_pdfs.append(pdf_info)
            
            return available_pdfs
            
        except Exception as e:
            print(f"Error listing available PDFs: {e}")
            return []
    
    def get_pdf_by_key(self, s3_key: str) -> Optional[PDFDocument]:
        """Get a specific PDF by S3 key"""
        return self.process_pdf(s3_key)
    
    def get_pdfs_by_keys(self, s3_keys: List[str]) -> List[PDFDocument]:
        """Get multiple PDFs by S3 keys"""
        pdf_documents = []
        for s3_key in s3_keys:
            pdf_doc = self.get_pdf_by_key(s3_key)
            if pdf_doc:
                pdf_documents.append(pdf_doc)
        return pdf_documents
    
    def filter_pdfs_by_relevance(self, pdf_documents: List[PDFDocument], query: str, min_relevance: float = 0.3) -> List[PDFDocument]:
        """Filter PDFs based on relevance to query"""
        # Simple keyword-based relevance scoring
        query_terms = query.lower().split()
        
        relevant_pdfs = []
        for pdf_doc in pdf_documents:
            content_lower = pdf_doc.content.lower()
            
            # Calculate relevance score based on keyword matches
            matches = sum(1 for term in query_terms if term in content_lower)
            relevance_score = matches / len(query_terms) if query_terms else 0
            
            if relevance_score >= min_relevance:
                pdf_doc.relevance_score = relevance_score
                relevant_pdfs.append(pdf_doc)
        
        # Sort by relevance score
        relevant_pdfs.sort(key=lambda x: x.relevance_score, reverse=True)
        return relevant_pdfs 