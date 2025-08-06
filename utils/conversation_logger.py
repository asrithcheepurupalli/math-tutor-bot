"""
Conversation logging for Math Tutor Bot
Logs interactions for analytics and improvement
"""

import asyncio
import json
import logging
import os
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import aiofiles
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ConversationEntry:
    """Data class for conversation entries"""
    timestamp: str
    user_id: int
    username: Optional[str]
    message_type: str  # text_problem, image_problem, command
    content: str
    response: Dict[str, Any]
    video_generated: bool = False
    processing_time: Optional[float] = None
    error: Optional[str] = None

class ConversationLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///math_tutor.db')
        self.log_to_file = True
        self.log_to_database = True
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Initialize database if using SQLite
        if self.database_url.startswith('sqlite:'):
            self._init_sqlite_db()
        
        self.logger.info("Conversation logger initialized")
    
    def _init_sqlite_db(self):
        """Initialize SQLite database for conversation logging"""
        try:
            db_path = self.database_url.replace('sqlite:///', '')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    message_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    response TEXT NOT NULL,
                    video_generated BOOLEAN DEFAULT FALSE,
                    processing_time REAL,
                    error TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for better query performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_user_id ON conversations(user_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_message_type ON conversations(message_type)
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info("SQLite database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing SQLite database: {str(e)}")
    
    async def log_interaction(
        self,
        user_id: int,
        username: Optional[str],
        message_type: str,
        content: str,
        response: Any,
        video_generated: bool = False,
        processing_time: Optional[float] = None,
        error: Optional[str] = None
    ):
        """
        Log a conversation interaction
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            message_type: Type of message (text_problem, image_problem, command)
            content: User's input content
            response: Bot's response
            video_generated: Whether a video was generated
            processing_time: Time taken to process the request
            error: Any error that occurred
        """
        try:
            # Create conversation entry
            entry = ConversationEntry(
                timestamp=datetime.now().isoformat(),
                user_id=user_id,
                username=username,
                message_type=message_type,
                content=content[:1000],  # Limit content length
                response=self._sanitize_response(response),
                video_generated=video_generated,
                processing_time=processing_time,
                error=error
            )
            
            # Log to file
            if self.log_to_file:
                await self._log_to_file(entry)
            
            # Log to database
            if self.log_to_database:
                await self._log_to_database(entry)
            
            self.logger.debug(f"Logged interaction for user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error logging interaction: {str(e)}")
    
    def _sanitize_response(self, response: Any) -> Dict[str, Any]:
        """Sanitize response data for logging"""
        if isinstance(response, dict):
            # Remove sensitive information and limit size
            sanitized = {}
            for key, value in response.items():
                if key not in ['api_key', 'token', 'credentials']:
                    if isinstance(value, str) and len(value) > 500:
                        sanitized[key] = value[:500] + "..."
                    else:
                        sanitized[key] = value
            return sanitized
        elif isinstance(response, str):
            return {'content': response[:500] + "..." if len(response) > 500 else response}
        else:
            return {'content': str(response)[:500]}
    
    async def _log_to_file(self, entry: ConversationEntry):
        """Log conversation entry to file"""
        try:
            log_file = f"logs/conversations_{datetime.now().strftime('%Y_%m')}.jsonl"
            
            async with aiofiles.open(log_file, 'a', encoding='utf-8') as f:
                await f.write(json.dumps(asdict(entry), ensure_ascii=False) + '\n')
                
        except Exception as e:
            self.logger.error(f"Error logging to file: {str(e)}")
    
    async def _log_to_database(self, entry: ConversationEntry):
        """Log conversation entry to database"""
        try:
            if self.database_url.startswith('sqlite:'):
                await self._log_to_sqlite(entry)
            else:
                # Placeholder for other database types
                self.logger.warning("Non-SQLite databases not yet implemented")
                
        except Exception as e:
            self.logger.error(f"Error logging to database: {str(e)}")
    
    async def _log_to_sqlite(self, entry: ConversationEntry):
        """Log to SQLite database"""
        try:
            db_path = self.database_url.replace('sqlite:///', '')
            
            # Use asyncio.to_thread for database operations
            await asyncio.to_thread(self._insert_sqlite_record, db_path, entry)
            
        except Exception as e:
            self.logger.error(f"Error logging to SQLite: {str(e)}")
    
    def _insert_sqlite_record(self, db_path: str, entry: ConversationEntry):
        """Insert record into SQLite database (sync function)"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations 
            (timestamp, user_id, username, message_type, content, response, 
             video_generated, processing_time, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.timestamp,
            entry.user_id,
            entry.username,
            entry.message_type,
            entry.content,
            json.dumps(entry.response),
            entry.video_generated,
            entry.processing_time,
            entry.error
        ))
        
        conn.commit()
        conn.close()
    
    async def get_user_history(
        self, user_id: int, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for a user
        
        Args:
            user_id: Telegram user ID
            limit: Maximum number of records to return
            
        Returns:
            List of conversation records
        """
        try:
            if self.database_url.startswith('sqlite:'):
                return await self._get_sqlite_user_history(user_id, limit)
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error getting user history: {str(e)}")
            return []
    
    async def _get_sqlite_user_history(
        self, user_id: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Get user history from SQLite"""
        try:
            db_path = self.database_url.replace('sqlite:///', '')
            
            result = await asyncio.to_thread(
                self._fetch_sqlite_user_history, db_path, user_id, limit
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error fetching SQLite user history: {str(e)}")
            return []
    
    def _fetch_sqlite_user_history(
        self, db_path: str, user_id: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Fetch user history from SQLite (sync function)"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM conversations 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        return [dict(row) for row in rows]
    
    async def get_analytics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get analytics data for the specified number of days
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Analytics data
        """
        try:
            if self.database_url.startswith('sqlite:'):
                return await self._get_sqlite_analytics(days)
            else:
                return {}
                
        except Exception as e:
            self.logger.error(f"Error getting analytics: {str(e)}")
            return {}
    
    async def _get_sqlite_analytics(self, days: int) -> Dict[str, Any]:
        """Get analytics from SQLite"""
        try:
            db_path = self.database_url.replace('sqlite:///', '')
            
            result = await asyncio.to_thread(
                self._fetch_sqlite_analytics, db_path, days
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error fetching SQLite analytics: {str(e)}")
            return {}
    
    def _fetch_sqlite_analytics(self, db_path: str, days: int) -> Dict[str, Any]:
        """Fetch analytics from SQLite (sync function)"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get date threshold
        date_threshold = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ).timestamp() - (days * 24 * 3600)
        
        analytics = {}
        
        # Total interactions
        cursor.execute('''
            SELECT COUNT(*) FROM conversations 
            WHERE created_at > datetime(?, 'unixepoch')
        ''', (date_threshold,))
        analytics['total_interactions'] = cursor.fetchone()[0]
        
        # Unique users
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) FROM conversations 
            WHERE created_at > datetime(?, 'unixepoch')
        ''', (date_threshold,))
        analytics['unique_users'] = cursor.fetchone()[0]
        
        # Message types breakdown
        cursor.execute('''
            SELECT message_type, COUNT(*) FROM conversations 
            WHERE created_at > datetime(?, 'unixepoch')
            GROUP BY message_type
        ''', (date_threshold,))
        analytics['message_types'] = dict(cursor.fetchall())
        
        # Videos generated
        cursor.execute('''
            SELECT COUNT(*) FROM conversations 
            WHERE created_at > datetime(?, 'unixepoch') AND video_generated = 1
        ''', (date_threshold,))
        analytics['videos_generated'] = cursor.fetchone()[0]
        
        # Average processing time
        cursor.execute('''
            SELECT AVG(processing_time) FROM conversations 
            WHERE created_at > datetime(?, 'unixepoch') AND processing_time IS NOT NULL
        ''', (date_threshold,))
        avg_time = cursor.fetchone()[0]
        analytics['avg_processing_time'] = round(avg_time, 2) if avg_time else 0
        
        # Errors
        cursor.execute('''
            SELECT COUNT(*) FROM conversations 
            WHERE created_at > datetime(?, 'unixepoch') AND error IS NOT NULL
        ''', (date_threshold,))
        analytics['errors'] = cursor.fetchone()[0]
        
        conn.close()
        return analytics
    
    def cleanup_old_logs(self, days_to_keep: int = 90):
        """
        Clean up old conversation logs
        
        Args:
            days_to_keep: Number of days of logs to keep
        """
        try:
            if self.database_url.startswith('sqlite:'):
                asyncio.create_task(self._cleanup_sqlite_logs(days_to_keep))
            
            # Also cleanup old log files
            asyncio.create_task(self._cleanup_log_files(days_to_keep))
            
        except Exception as e:
            self.logger.error(f"Error initiating cleanup: {str(e)}")
    
    async def _cleanup_sqlite_logs(self, days_to_keep: int):
        """Clean up old SQLite logs"""
        try:
            db_path = self.database_url.replace('sqlite:///', '')
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
            
            await asyncio.to_thread(self._delete_old_sqlite_records, db_path, cutoff_date)
            
        except Exception as e:
            self.logger.error(f"Error cleaning up SQLite logs: {str(e)}")
    
    def _delete_old_sqlite_records(self, db_path: str, cutoff_timestamp: float):
        """Delete old records from SQLite (sync function)"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM conversations 
            WHERE created_at < datetime(?, 'unixepoch')
        ''', (cutoff_timestamp,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        self.logger.info(f"Cleaned up {deleted_count} old conversation records")
    
    async def _cleanup_log_files(self, days_to_keep: int):
        """Clean up old log files"""
        try:
            import glob
            from pathlib import Path
            
            log_files = glob.glob('logs/conversations_*.jsonl')
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
            
            for log_file in log_files:
                file_stat = Path(log_file).stat()
                if file_stat.st_mtime < cutoff_date:
                    os.remove(log_file)
                    self.logger.info(f"Removed old log file: {log_file}")
                    
        except Exception as e:
            self.logger.error(f"Error cleaning up log files: {str(e)}")
