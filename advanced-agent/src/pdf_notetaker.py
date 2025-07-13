from typing import Dict, Any, List
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from .models import PDFDocument, PDFNotes, ResearchState
from .s3_pdf_service import S3PDFService
from .prompts import DeveloperToolsPrompts


class PDFNotetakerAgent:
    """Agent for processing PDF documents and generating structured notes"""
    
    def __init__(self, llm: ChatAnthropic):
        self.llm = llm
        self.s3_service = S3PDFService()
        self.prompts = DeveloperToolsPrompts()
    
    def analyze_pdf_content(self, pdf_doc: PDFDocument, query: str) -> PDFNotes:
        """Analyze PDF content and generate structured notes"""
        
        # Use structured output for consistent formatting
        structured_llm = self.llm.with_structured_output(PDFNotes)
        
        messages = [
            SystemMessage(content=self.prompts.PDF_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.pdf_analysis_user(query, pdf_doc.content))
        ]
        
        try:
            # Generate structured notes
            notes = structured_llm.invoke(messages)
            
            # Set document ID
            notes.document_id = pdf_doc.s3_key
            
            return notes
            
        except Exception as e:
            print(f"Error analyzing PDF {pdf_doc.filename}: {e}")
            # Return default notes on error
            return PDFNotes(
                document_id=pdf_doc.s3_key,
                summary=f"Failed to analyze {pdf_doc.filename}",
                key_points=[],
                technical_details=[],
                business_insights=[],
                recommendations=[],
                extracted_entities=[],
                relevance_score=0.0
            )
    
    def process_pdfs_for_query(self, query: str, state: ResearchState) -> Dict[str, Any]:
        """Process PDFs relevant to the query and update state"""
        
        print(f"📄 Processing PDFs for query: {query}")
        
        # Find and process relevant PDFs
        pdf_documents = self.s3_service.find_relevant_pdfs(query, max_pdfs=3)
        
        if not pdf_documents:
            print("No PDF documents found to process")
            return {"pdf_documents": [], "pdf_notes": []}
        
        print(f"Found {len(pdf_documents)} PDF documents to analyze")
        
        # Analyze each PDF and generate notes
        pdf_notes = []
        for pdf_doc in pdf_documents:
            print(f"🔍 Analyzing PDF: {pdf_doc.filename}")
            
            # Generate structured notes
            notes = self.analyze_pdf_content(pdf_doc, query)
            pdf_notes.append(notes)
            
            print(f"✅ Generated notes for {pdf_doc.filename}")
            print(f"   Summary: {notes.summary[:100]}...")
            print(f"   Key Points: {len(notes.key_points)}")
            print(f"   Relevance Score: {notes.relevance_score}")
        
        return {
            "pdf_documents": pdf_documents,
            "pdf_notes": pdf_notes
        }
    
    def get_pdf_insights_summary(self, pdf_notes: List[PDFNotes]) -> str:
        """Create a summary of insights from all PDF notes"""
        if not pdf_notes:
            return "No PDF documents analyzed."
        
        summary_parts = []
        for i, notes in enumerate(pdf_notes, 1):
            summary_parts.append(f"Document {i}:")
            summary_parts.append(f"  Summary: {notes.summary}")
            if notes.key_points:
                summary_parts.append(f"  Key Points: {', '.join(notes.key_points[:3])}")
            if notes.business_insights:
                summary_parts.append(f"  Business Insights: {', '.join(notes.business_insights[:3])}")
            summary_parts.append("")
        
        return "\n".join(summary_parts)
    
    def filter_relevant_pdfs(self, pdf_notes: List[PDFNotes], min_relevance: float = 0.3) -> List[PDFNotes]:
        """Filter PDF notes based on relevance score"""
        return [notes for notes in pdf_notes if notes.relevance_score and notes.relevance_score >= min_relevance] 
    
    def get_available_pdfs_for_selection(self) -> List[Dict[str, Any]]:
        """Get list of available PDFs for user selection"""
        return self.s3_service.list_available_pdfs()
    
    def process_user_selected_pdfs(self, selected_s3_keys: List[str], query: str) -> Dict[str, Any]:
        """Process user-selected PDFs for a specific query"""
        
        print(f"📄 Processing user-selected PDFs for query: {query}")
        print(f"Selected PDFs: {len(selected_s3_keys)}")
        
        # Get the selected PDFs
        pdf_documents = self.s3_service.get_pdfs_by_keys(selected_s3_keys)
        
        if not pdf_documents:
            print("No PDF documents found for selected keys")
            return {"pdf_documents": [], "pdf_notes": []}
        
        print(f"Successfully loaded {len(pdf_documents)} PDF documents")
        
        # Analyze each PDF and generate notes
        pdf_notes = []
        for pdf_doc in pdf_documents:
            print(f"🔍 Analyzing selected PDF: {pdf_doc.filename}")
            
            # Generate structured notes
            notes = self.analyze_pdf_content(pdf_doc, query)
            pdf_notes.append(notes)
            
            print(f"✅ Generated notes for {pdf_doc.filename}")
            print(f"   Summary: {notes.summary[:100]}...")
            print(f"   Key Points: {len(notes.key_points)}")
            print(f"   Relevance Score: {notes.relevance_score}")
        
        return {
            "pdf_documents": pdf_documents,
            "pdf_notes": pdf_notes
        }
    
    def filter_and_rank_pdfs(self, query: str, max_pdfs: int = 5) -> List[Dict[str, Any]]:
        """Filter and rank available PDFs by relevance to query"""
        
        # Get all available PDFs
        available_pdfs = self.get_available_pdfs_for_selection()
        
        if not available_pdfs:
            return []
        
        # Process PDFs to get content for relevance scoring
        pdf_documents = []
        for pdf_info in available_pdfs:
            pdf_doc = self.s3_service.get_pdf_by_key(pdf_info['s3_key'])
            if pdf_doc:
                pdf_documents.append(pdf_doc)
        
        # Filter by relevance
        relevant_pdfs = self.s3_service.filter_pdfs_by_relevance(pdf_documents, query)
        
        # Convert back to info format with relevance scores
        ranked_pdfs = []
        for pdf_doc in relevant_pdfs[:max_pdfs]:
            pdf_info = {
                's3_key': pdf_doc.s3_key,
                'filename': pdf_doc.filename,
                'relevance_score': pdf_doc.relevance_score,
                'summary': pdf_doc.content[:200] + "..." if len(pdf_doc.content) > 200 else pdf_doc.content
            }
            ranked_pdfs.append(pdf_info)
        
        return ranked_pdfs 