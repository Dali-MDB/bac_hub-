from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

class ResourceReportThrottle(BaseThrottle):
    def __init__(self):
        super().__init__()
    
    def allow_request(self, request, view):
      #  print("here")
        # Get IP address
        ip = self.get_ident(request)
        
        # Get resource_id from URL kwargs
        resource_id = request.resolver_match.kwargs.get('resource_id')
        
        if not ip or not resource_id:
            return True  # Allow if we can't identify properly
        
        # Create unique cache key
        cache_key = f'throttle_resource_report_{ip}_{resource_id}'
        
        # Check if request was made recently
        last_request = cache.get(cache_key)
        now = timezone.now()
        
        if last_request:
            # Calculate time since last request
            time_diff = now - last_request
            
            # If less than 24 hours (1 day), deny request
            if time_diff < timedelta(hours=24):
                return False
        
        # Allow request and store timestamp
        cache.set(cache_key, now, timeout=86400)  # 24 hours in seconds
        return True
    
    def wait(self):
        """Return how long to wait before next request (optional)"""
        return 86400  # 24 hours in seconds
    





class QuestionReportThrottle(BaseThrottle):
    def __init__(self):
        super().__init__()
    
    def allow_request(self, request, view):
      #  print("here")
        # Get IP address
        ip = self.get_ident(request)
        
        # Get resource_id from URL kwargs
        question_id = request.resolver_match.kwargs.get('question_id')
        
        if not ip or not question_id:
            return True  # Allow if we can't identify properly
        
        # Create unique cache key
        cache_key = f'throttle_question_report_{ip}_{question_id}'
        
        # Check if request was made recently
        last_request = cache.get(cache_key)
        now = timezone.now()
        
        if last_request:
            # Calculate time since last request
            time_diff = now - last_request
            
            # If less than 2 hours , deny request
            if time_diff < timedelta(hours=2):
                return False
        
        # Allow request and store timestamp
        cache.set(cache_key, now, timeout=7200)  # 2 hours in seconds
        return True
    
    def wait(self):
        """Return how long to wait before next request (optional)"""
        return 7200  # 2 hours in seconds
    



class ReplyReportThrottle(BaseThrottle):
    def __init__(self):
        super().__init__()
    
    def allow_request(self, request, view):
      #  print("here")
        # Get IP address
        ip = self.get_ident(request)
        
        # Get resource_id from URL kwargs
        reply_id = request.resolver_match.kwargs.get('reply_id')
        
        if not ip or not reply_id:
            return True  # Allow if we can't identify properly
        
        # Create unique cache key
        cache_key = f'throttle_question_report_{ip}_{reply_id}'
        
        # Check if request was made recently
        last_request = cache.get(cache_key)
        now = timezone.now()
        
        if last_request:
            # Calculate time since last request
            time_diff = now - last_request
            
            # If less than 2 hours , deny request
            if time_diff < timedelta(hours=2):
                return False
        
        # Allow request and store timestamp
        cache.set(cache_key, now, timeout=7200)  # 2 hours in seconds
        return True
    
    def wait(self):
        """Return how long to wait before next request (optional)"""
        return 7200  # 2 hours in seconds