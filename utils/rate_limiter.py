"""
Rate limiting for Math Tutor Bot
Prevents abuse and ensures fair usage
"""

import asyncio
import logging
import time
from typing import Dict, Optional
from collections import defaultdict, deque
import os
from dotenv import load_dotenv

load_dotenv()

class RateLimiter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.max_requests = int(os.getenv('RATE_LIMIT_REQUESTS', 10))
        self.window_seconds = int(os.getenv('RATE_LIMIT_WINDOW', 60))
        
        # Storage for user request timestamps
        self.user_requests: Dict[int, deque] = defaultdict(lambda: deque())
        
        # Storage for temporary bans
        self.banned_users: Dict[int, float] = {}
        
        # Cleanup task
        self._cleanup_task = None
        # Don't start cleanup task immediately to avoid event loop issues
        
        self.logger.info(f"Rate limiter initialized: {self.max_requests} requests per {self.window_seconds}s")
    
    async def check_rate_limit(self, user_id: int) -> bool:
        """
        Check if user is within rate limits
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if request is allowed, False if rate limited
        """
        try:
            # Start cleanup task if not already started
            if self._cleanup_task is None:
                self._start_cleanup_task()
                
            current_time = time.time()
            
            # Check if user is temporarily banned
            if user_id in self.banned_users:
                if current_time < self.banned_users[user_id]:
                    self.logger.warning(f"User {user_id} is temporarily banned")
                    return False
                else:
                    # Ban expired, remove from banned list
                    del self.banned_users[user_id]
            
            # Get user's request history
            user_requests = self.user_requests[user_id]
            
            # Remove old requests outside the window
            window_start = current_time - self.window_seconds
            while user_requests and user_requests[0] < window_start:
                user_requests.popleft()
            
            # Check if user has exceeded the limit
            if len(user_requests) >= self.max_requests:
                self.logger.warning(
                    f"Rate limit exceeded for user {user_id}: "
                    f"{len(user_requests)} requests in {self.window_seconds}s"
                )
                
                # Implement progressive penalties
                self._apply_penalty(user_id, len(user_requests))
                return False
            
            # Add current request timestamp
            user_requests.append(current_time)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking rate limit: {str(e)}")
            # In case of error, allow the request (fail open)
            return True
    
    def _apply_penalty(self, user_id: int, request_count: int):
        """Apply progressive penalties for rate limit violations"""
        current_time = time.time()
        
        if request_count >= self.max_requests * 3:
            # Severe violation: 1 hour ban
            ban_duration = 3600
            self.logger.warning(f"Applying 1-hour ban to user {user_id}")
        elif request_count >= self.max_requests * 2:
            # Moderate violation: 10 minute ban
            ban_duration = 600
            self.logger.warning(f"Applying 10-minute ban to user {user_id}")
        else:
            # Minor violation: 1 minute ban
            ban_duration = 60
            self.logger.warning(f"Applying 1-minute ban to user {user_id}")
        
        self.banned_users[user_id] = current_time + ban_duration
    
    def get_user_status(self, user_id: int) -> Dict[str, any]:
        """
        Get rate limiting status for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dictionary with user's rate limiting status
        """
        try:
            current_time = time.time()
            user_requests = self.user_requests.get(user_id, deque())
            
            # Count recent requests
            window_start = current_time - self.window_seconds
            recent_requests = sum(1 for req_time in user_requests if req_time >= window_start)
            
            # Check ban status
            is_banned = user_id in self.banned_users and current_time < self.banned_users[user_id]
            ban_expires = self.banned_users.get(user_id, 0) if is_banned else None
            
            return {
                'user_id': user_id,
                'recent_requests': recent_requests,
                'max_requests': self.max_requests,
                'window_seconds': self.window_seconds,
                'remaining_requests': max(0, self.max_requests - recent_requests),
                'is_banned': is_banned,
                'ban_expires': ban_expires,
                'ban_time_remaining': max(0, ban_expires - current_time) if ban_expires else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting user status: {str(e)}")
            return {'error': str(e)}
    
    def reset_user_limits(self, user_id: int):
        """
        Reset rate limits for a specific user (admin function)
        
        Args:
            user_id: Telegram user ID to reset
        """
        try:
            if user_id in self.user_requests:
                self.user_requests[user_id].clear()
            
            if user_id in self.banned_users:
                del self.banned_users[user_id]
            
            self.logger.info(f"Reset rate limits for user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error resetting user limits: {str(e)}")
    
    def _start_cleanup_task(self):
        """Start background cleanup task"""
        try:
            if self._cleanup_task is None:
                loop = asyncio.get_event_loop()
                self._cleanup_task = loop.create_task(self._cleanup_old_data())
        except RuntimeError:
            # No event loop running, cleanup will happen on demand
            pass
    
    async def _cleanup_old_data(self):
        """Background task to clean up old request data"""
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                current_time = time.time()
                
                # Clean up old request timestamps
                users_to_remove = []
                for user_id, requests in self.user_requests.items():
                    window_start = current_time - self.window_seconds
                    
                    # Remove old requests
                    while requests and requests[0] < window_start:
                        requests.popleft()
                    
                    # If no recent requests, remove user from tracking
                    if not requests:
                        users_to_remove.append(user_id)
                
                for user_id in users_to_remove:
                    del self.user_requests[user_id]
                
                # Clean up expired bans
                expired_bans = [
                    user_id for user_id, ban_time in self.banned_users.items()
                    if current_time >= ban_time
                ]
                
                for user_id in expired_bans:
                    del self.banned_users[user_id]
                
                if users_to_remove or expired_bans:
                    self.logger.debug(
                        f"Cleanup completed: removed {len(users_to_remove)} inactive users, "
                        f"expired {len(expired_bans)} bans"
                    )
                
            except Exception as e:
                self.logger.error(f"Error in cleanup task: {str(e)}")
                # Continue running despite errors
                continue
    
    def get_statistics(self) -> Dict[str, any]:
        """Get rate limiting statistics"""
        try:
            current_time = time.time()
            
            # Count active users (users with recent requests)
            active_users = 0
            total_recent_requests = 0
            
            for user_requests in self.user_requests.values():
                window_start = current_time - self.window_seconds
                recent_count = sum(1 for req_time in user_requests if req_time >= window_start)
                if recent_count > 0:
                    active_users += 1
                    total_recent_requests += recent_count
            
            # Count banned users
            active_bans = sum(
                1 for ban_time in self.banned_users.values()
                if current_time < ban_time
            )
            
            return {
                'active_users': active_users,
                'total_recent_requests': total_recent_requests,
                'active_bans': active_bans,
                'max_requests_per_window': self.max_requests,
                'window_seconds': self.window_seconds,
                'tracked_users': len(self.user_requests),
                'total_banned_users': len(self.banned_users)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {str(e)}")
            return {'error': str(e)}
    
    def shutdown(self):
        """Clean shutdown of rate limiter"""
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()
        self.logger.info("Rate limiter shutdown completed")
