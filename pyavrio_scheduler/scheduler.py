from .session import Session
import requests
from enum import Enum
from .endpoints import SchedulerEndpoints

class JobType(Enum):
    DATA_QUALITY = "dsdq"
    PYTHON_NOTEBOOK = "python_notebook"
    SQL_NOTEBOOK = "sql_notebook"

class Scheduler:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self, selected_topic_name):
        """Call list scheduler API and return results."""
        try:
            endpoint = self.session.get_host().rstrip("/") + SchedulerEndpoints.LIST_API
        
            headers = {
                "Authorization": "Bearer " + self.session.user_state.access_token,
                "Content-Type": "application/json",
            }
            selected_topic_name = selected_topic_name.strip().upper()

            if selected_topic_name == "DATA_QUALITY" :
                selected_topic_name = "DSDQ"

            payload = {
                "userId": self.session.user_state.user_id,
                "topic": selected_topic_name,
                "searchBy": "",
                "sortBy": "",
                "ascending": True,
                "page": 0,
                "size": 1000,
                "statusFilter": [],
                "scheduledFrequencyFilter": []
            }

            if selected_topic_name == "DSDQ" or selected_topic_name == "PYTHON_NOTEBOOK" or selected_topic_name == "SQL_NOTEBOOK"  :
                pass
            else:
                print("Invalid topic selection. Please select from python_notebook, sql_notebook or data_quality.")
                return None
            
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()

            if response.status_code == 500:
                print(f"Server Error: {response.text}")

            return response.json().get("content", [])

        except requests.exceptions.HTTPError as http_err:
            print(f"Error while calling list scheduler API: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request exception occurred: {req_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return None

    
    def trigger_scheduler(self, scheduler_name, scheduler_id, job_type: JobType):
        """Trigger scheduler API."""
        try:
            job_type = job_type.strip().upper()
            if job_type == "PYTHON_NOTEBOOK" or job_type == "SQL_NOTEBOOK" :
                job_type = "NOTEBOOK"
            elif job_type == "DATA_QUALITY" :
                job_type = "DSDQ"

            endpoint = self.session.get_host() + SchedulerEndpoints.TRIGGER_API
            headers = {"Authorization": "Bearer " + self.session.user_state.access_token, "Content-Type": "application/json"}

            payload = {
                "jobName": scheduler_name,
                "jobId": scheduler_id,
                "topic": job_type, 
                "userId": self.session.user_state.user_id
            }

            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()

            return response.json()  
        except requests.exceptions.RequestException as req_err:
            print(f"Error while triggering scheduler: {req_err}")
            return None
