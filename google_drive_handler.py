#!/usr/bin/env python3
"""
Google Drive Handler - Dynamic CV editing and PDF conversion
Manages Google Docs manipulation for job-specific CV customization
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
    from google.oauth2 import service_account
    from googleapiclient.errors import HttpError
    import io
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

from config import Config

logger = logging.getLogger(__name__)

class GoogleDriveHandler:
    """Handles Google Drive operations for CV management"""
    
    def __init__(self):
        self.service = None
        self.docs_service = None
        self.credentials = None
        
        if not GOOGLE_API_AVAILABLE:
            logger.error("Google API libraries not installed. Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            return
            
        self._initialize_credentials()
        
    def _initialize_credentials(self):
        """Initialize Google Drive service account credentials"""
        try:
            # Get service account credentials from environment or file
            credentials_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH", "service_account.json")
            
            if os.path.exists(credentials_path):
                self.credentials = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
                )
            else:
                # Try to use environment variable with JSON content
                credentials_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
                if credentials_json:
                    credentials_info = json.loads(credentials_json)
                    self.credentials = service_account.Credentials.from_service_account_info(
                        credentials_info,
                        scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
                    )
                else:
                    logger.error("No Google Service Account credentials found")
                    return
            
            # Build services
            self.service = build('drive', 'v3', credentials=self.credentials)
            self.docs_service = build('docs', 'v1', credentials=self.credentials)
            
            logger.info("Google Drive services initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Google credentials: {e}")
            self.service = None
            self.docs_service = None
    
    def find_master_cv(self, cv_name: str = "Enas Ahmed - Master CV") -> Optional[str]:
        """Find the master CV document in Google Drive"""
        if not self.service:
            logger.error("Google Drive service not initialized")
            return None
            
        try:
            # Search for the CV document
            results = self.service.files().list(
                q=f"name='{cv_name}' and mimeType='application/vnd.google-apps.document'",
                fields="files(id, name, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            if not files:
                logger.error(f"Master CV '{cv_name}' not found")
                return None
            
            # Return the most recently modified file
            latest_file = max(files, key=lambda x: x.get('modifiedTime', ''))
            doc_id = latest_file['id']
            
            logger.info(f"Found master CV: {latest_file['name']} (ID: {doc_id})")
            return doc_id
            
        except HttpError as e:
            logger.error(f"Error searching for master CV: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error finding master CV: {e}")
            return None
    
    def get_document_content(self, doc_id: str) -> Optional[Dict]:
        """Get the content of a Google Doc"""
        if not self.docs_service:
            logger.error("Google Docs service not initialized")
            return None
            
        try:
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            return document
            
        except HttpError as e:
            logger.error(f"Error getting document content: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting document content: {e}")
            return None
    
    def customize_cv_for_job(self, doc_id: str, job_keywords: List[str], job_location: str = "") -> Optional[str]:
        """Customize CV content based on job keywords and location"""
        if not self.docs_service:
            logger.error("Google Docs service not initialized")
            return None
            
        try:
            # Get current document content
            document = self.get_document_content(doc_id)
            if not document:
                return None
            
            # Create a copy of the document for customization
            copy_title = f"Enas Ahmed CV - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            copy_request = {
                'name': copy_title
            }
            
            copy_response = self.service.files().copy(
                fileId=doc_id,
                body=copy_request
            ).execute()
            
            customized_doc_id = copy_response['id']
            logger.info(f"Created customized CV copy: {copy_title} (ID: {customized_doc_id})")
            
            # Get the content of the copied document
            customized_doc = self.get_document_content(customized_doc_id)
            
            # Analyze and enhance content based on keywords
            requests = self._generate_customization_requests(customized_doc, job_keywords, job_location)
            
            if requests:
                # Apply the customizations
                self.docs_service.documents().batchUpdate(
                    documentId=customized_doc_id,
                    body={'requests': requests}
                ).execute()
                
                logger.info(f"Applied {len(requests)} customizations to CV")
            
            return customized_doc_id
            
        except HttpError as e:
            logger.error(f"Error customizing CV: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error customizing CV: {e}")
            return None
    
    def _generate_customization_requests(self, document: Dict, job_keywords: List[str], job_location: str) -> List[Dict]:
        """Generate requests to customize document based on job keywords"""
        requests = []
        
        try:
            content = document.get('body', {}).get('content', [])
            
            # Extract text from document
            full_text = ""
            for element in content:
                if 'paragraph' in element:
                    for paragraph_element in element['paragraph'].get('elements', []):
                        if 'textRun' in paragraph_element:
                            full_text += paragraph_element['textRun'].get('content', '')
            
            # Find strategic locations to insert keyword highlights
            keyword_insertions = self._plan_keyword_insertions(job_keywords, job_location, full_text)
            
            # Generate replacement requests
            for insertion in keyword_insertions:
                requests.append({
                    'replaceAllText': {
                        'containsText': {
                            'text': insertion['target'],
                            'matchCase': False
                        },
                        'replaceText': insertion['replacement']
                    }
                })
            
            # Add location-specific enhancements
            if job_location:
                location_enhancements = self._get_location_enhancements(job_location)
                for enhancement in location_enhancements:
                    requests.append({
                        'insertText': {
                            'location': {
                                'index': 1  # Insert at beginning
                            },
                            'text': enhancement
                        }
                    })
            
        except Exception as e:
            logger.error(f"Error generating customization requests: {e}")
        
        return requests
    
    def _plan_keyword_insertions(self, job_keywords: List[str], job_location: str, current_text: str) -> List[Dict]:
        """Plan where to insert keyword enhancements"""
        insertions = []
        
        # Priority keywords for different regions/technologies
        keyword_mapping = {
            'ZATCA': ['ZATCA Phase II', 'Saudi Arabian compliance', 'E-invoicing'],
            'FinTech': ['Financial Technology', 'Payment Systems', 'Banking Solutions'],
            'Microservices': ['Microservices Architecture', 'Distributed Systems', 'API Design'],
            'Node.js': ['Node.js', 'JavaScript', 'Backend Development'],
            'Python': ['Python', 'Backend Development', 'API Development'],
            'AI': ['Artificial Intelligence', 'Machine Learning', 'AI Integration'],
            'Cloud': ['Cloud Architecture', 'AWS', 'Azure', 'GCP']
        }
        
        # Check which keywords are relevant
        relevant_keywords = []
        for keyword in job_keywords:
            for key, variations in keyword_mapping.items():
                if key.lower() in keyword.lower() or any(var.lower() in keyword.lower() for var in variations):
                    relevant_keywords.extend(variations)
        
        # Plan insertions based on current content
        if 'ZATCA' in relevant_keywords and job_location.upper() in ['KSA', 'SAUDI']:
            insertions.append({
                'target': 'TECHNICAL EXPERTISE',
                'replacement': 'TECHNICAL EXPERTISE\n- ZATCA Phase II Compliance Specialist\n- Saudi Arabian E-invoicing Expert'
            })
        
        if 'FinTech' in relevant_keywords:
            insertions.append({
                'target': 'KEY ACHIEVEMENTS',
                'replacement': 'KEY ACHIEVEMENTS\n- FinTech Payment Systems Architect\n- Regulatory Compliance Implementation'
            })
        
        return insertions
    
    def _get_location_enhancements(self, job_location: str) -> List[str]:
        """Get location-specific CV enhancements"""
        enhancements = []
        
        location_mapping = {
            'KSA': ['\nSaudi Arabian Market Experience\nZATCA Phase II Compliance Expert\n'],
            'SAUDI': ['\nSaudi Arabian Market Experience\nZATCA Phase II Compliance Expert\n'],
            'UAE': ['\nUAE Market Experience\nRegional Compliance Knowledge\n'],
            'EGYPT': ['\nEgyptian Market Experience\nRegional Technology Leadership\n'],
            'EU': ['\nEuropean Market Experience\nGDPR Compliance Knowledge\n']
        }
        
        for key, enhancement in location_mapping.items():
            if key.upper() in job_location.upper():
                enhancements.extend(enhancement)
                break
        
        return enhancements
    
    def export_to_pdf(self, doc_id: str, output_path: Optional[str] = None) -> Optional[str]:
        """Export Google Doc to PDF format"""
        if not self.service:
            logger.error("Google Drive service not initialized")
            return None
            
        try:
            # Get document info for filename
            doc_info = self.service.files().get(
                fileId=doc_id,
                fields='name'
            ).execute()
            
            # Generate output path if not provided
            if not output_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                doc_name = doc_info.get('name', 'CV').replace(' ', '_')
                output_path = f"{doc_name}_{timestamp}.pdf"
            
            # Use Windows absolute path if on Windows
            if os.name == 'nt':
                output_path = os.path.abspath(output_path)
            
            # Export as PDF
            request = self.service.files().export_media(
                fileId=doc_id,
                mimeType='application/pdf'
            )
            
            # Download the PDF
            with io.BytesIO() as file_io:
                downloader = MediaIoBaseDownload(file_io, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    logger.debug(f"PDF Download {int(status.progress() * 100)}%")
                
                # Save to file
                with open(output_path, 'wb') as f:
                    f.write(file_io.getvalue())
            
            logger.info(f"PDF exported successfully: {output_path}")
            return output_path
            
        except HttpError as e:
            logger.error(f"Error exporting to PDF: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error exporting to PDF: {e}")
            return None
    
    def cleanup_temp_documents(self, max_age_hours: int = 24):
        """Clean up temporary CV documents older than specified hours"""
        if not self.service:
            logger.error("Google Drive service not initialized")
            return
            
        try:
            # Find all temporary CV documents
            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
            
            results = self.service.files().list(
                q="name contains 'Enas Ahmed CV -' and mimeType='application/vnd.google-apps.document'",
                fields="files(id, name, createdTime)"
            ).execute()
            
            files = results.get('files', [])
            deleted_count = 0
            
            for file in files:
                try:
                    created_time = datetime.fromisoformat(
                        file['createdTime'].replace('Z', '+00:00')
                    ).timestamp()
                    
                    if created_time < cutoff_time:
                        self.service.files().delete(fileId=file['id']).execute()
                        deleted_count += 1
                        logger.info(f"Deleted old temporary document: {file['name']}")
                        
                except Exception as e:
                    logger.error(f"Error deleting document {file['name']}: {e}")
            
            logger.info(f"Cleanup completed. Deleted {deleted_count} old documents")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get the current status of Google Drive services"""
        return {
            'credentials_loaded': self.credentials is not None,
            'drive_service_available': self.service is not None,
            'docs_service_available': self.docs_service is not None,
            'google_api_available': GOOGLE_API_AVAILABLE
        }
