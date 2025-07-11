#!/usr/bin/env python3
"""
Corporate Memory Backup Script for Agentic Agile System
"""

import os
import json
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import structlog
import psycopg2
from pymongo import MongoClient
import redis
import boto3
from google.cloud import storage
import azure.storage.blob
import click

logger = structlog.get_logger()


class MemoryBackup:
    """Corporate memory backup manager"""
    
    def __init__(self, config):
        self.config = config
        self.backup_dir = Path(config.get('backup_dir', './backups'))
        self.backup_dir.mkdir(exist_ok=True)
        
        # Database connections
        self.pg_conn = None
        self.mongo_client = None
        self.redis_client = None
        
        # Cloud storage clients
        self.s3_client = None
        self.gcs_client = None
        self.azure_client = None
        
    def connect_databases(self):
        """Connect to all databases"""
        try:
            # PostgreSQL
            if self.config.get('postgres_url'):
                self.pg_conn = psycopg2.connect(self.config['postgres_url'])
                logger.info("Connected to PostgreSQL")
            
            # MongoDB
            if self.config.get('mongodb_url'):
                self.mongo_client = MongoClient(self.config['mongodb_url'])
                logger.info("Connected to MongoDB")
            
            # Redis
            if self.config.get('redis_url'):
                self.redis_client = redis.from_url(self.config['redis_url'])
                logger.info("Connected to Redis")
                
        except Exception as e:
            logger.error("Failed to connect to databases", error=str(e))
            raise
    
    def backup_postgres(self):
        """Backup PostgreSQL data"""
        if not self.pg_conn:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"postgres_backup_{timestamp}.sql"
        
        try:
            # Use pg_dump for full backup
            pg_dump_cmd = f"pg_dump {self.config['postgres_url']} > {backup_file}"
            os.system(pg_dump_cmd)
            
            # Compress the backup
            compressed_file = backup_file.with_suffix('.sql.gz')
            with open(backup_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed file
            backup_file.unlink()
            
            logger.info("PostgreSQL backup completed", file=str(compressed_file))
            return compressed_file
            
        except Exception as e:
            logger.error("PostgreSQL backup failed", error=str(e))
            return None
    
    def backup_mongodb(self):
        """Backup MongoDB data"""
        if not self.mongo_client:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_dir / f"mongodb_backup_{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        try:
            # Use mongodump for full backup
            db_name = self.config.get('mongodb_database', 'agentic_agile')
            mongodump_cmd = f"mongodump --uri='{self.config['mongodb_url']}' --db={db_name} --out={backup_dir}"
            os.system(mongodump_cmd)
            
            # Create archive
            archive_file = self.backup_dir / f"mongodb_backup_{timestamp}.tar.gz"
            shutil.make_archive(str(archive_file.with_suffix('')), 'gztar', backup_dir)
            
            # Clean up temp directory
            shutil.rmtree(backup_dir)
            
            logger.info("MongoDB backup completed", file=str(archive_file))
            return archive_file
            
        except Exception as e:
            logger.error("MongoDB backup failed", error=str(e))
            return None
    
    def backup_redis(self):
        """Backup Redis data"""
        if not self.redis_client:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"redis_backup_{timestamp}.json"
        
        try:
            # Get all keys and their values
            data = {}
            for key in self.redis_client.scan_iter():
                key_type = self.redis_client.type(key)
                if key_type == 'string':
                    data[key.decode()] = self.redis_client.get(key).decode()
                elif key_type == 'hash':
                    data[key.decode()] = self.redis_client.hgetall(key)
                elif key_type == 'list':
                    data[key.decode()] = self.redis_client.lrange(key, 0, -1)
                elif key_type == 'set':
                    data[key.decode()] = list(self.redis_client.smembers(key))
                elif key_type == 'zset':
                    data[key.decode()] = self.redis_client.zrange(key, 0, -1, withscores=True)
            
            # Save to JSON file
            with open(backup_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            # Compress
            compressed_file = backup_file.with_suffix('.json.gz')
            with open(backup_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed file
            backup_file.unlink()
            
            logger.info("Redis backup completed", file=str(compressed_file))
            return compressed_file
            
        except Exception as e:
            logger.error("Redis backup failed", error=str(e))
            return None
    
    def backup_corporate_memory(self):
        """Backup corporate memory specifically"""
        if not self.pg_conn:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"corporate_memory_{timestamp}.json"
        
        try:
            cursor = self.pg_conn.cursor()
            cursor.execute("""
                SELECT id, timestamp, memory_type, category, title, description,
                       context, agent_id, user_id, project_id, tags, confidence_score,
                       usage_count, last_accessed, is_active, metadata
                FROM corporate_memory
                WHERE is_active = true
                ORDER BY timestamp DESC
            """)
            
            memories = []
            for row in cursor.fetchall():
                memory = {
                    'id': row[0],
                    'timestamp': row[1].isoformat() if row[1] else None,
                    'memory_type': row[2],
                    'category': row[3],
                    'title': row[4],
                    'description': row[5],
                    'context': row[6],
                    'agent_id': row[7],
                    'user_id': row[8],
                    'project_id': row[9],
                    'tags': row[10],
                    'confidence_score': float(row[11]) if row[11] else None,
                    'usage_count': row[12],
                    'last_accessed': row[13].isoformat() if row[13] else None,
                    'is_active': row[14],
                    'metadata': row[15]
                }
                memories.append(memory)
            
            # Save to JSON file
            with open(backup_file, 'w') as f:
                json.dump({
                    'backup_timestamp': datetime.now().isoformat(),
                    'total_memories': len(memories),
                    'memories': memories
                }, f, indent=2)
            
            # Compress
            compressed_file = backup_file.with_suffix('.json.gz')
            with open(backup_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed file
            backup_file.unlink()
            
            logger.info("Corporate memory backup completed", 
                       file=str(compressed_file), count=len(memories))
            return compressed_file
            
        except Exception as e:
            logger.error("Corporate memory backup failed", error=str(e))
            return None
    
    def upload_to_cloud(self, file_path, cloud_type):
        """Upload backup file to cloud storage"""
        try:
            if cloud_type == 's3' and self.config.get('aws_s3_bucket'):
                if not self.s3_client:
                    self.s3_client = boto3.client('s3')
                
                bucket = self.config['aws_s3_bucket']
                key = f"backups/{file_path.name}"
                self.s3_client.upload_file(str(file_path), bucket, key)
                logger.info("Uploaded to S3", bucket=bucket, key=key)
                
            elif cloud_type == 'gcs' and self.config.get('gcs_bucket'):
                if not self.gcs_client:
                    self.gcs_client = storage.Client()
                
                bucket = self.gcs_client.bucket(self.config['gcs_bucket'])
                blob = bucket.blob(f"backups/{file_path.name}")
                blob.upload_from_filename(str(file_path))
                logger.info("Uploaded to GCS", bucket=self.config['gcs_bucket'], blob=blob.name)
                
            elif cloud_type == 'azure' and self.config.get('azure_container'):
                if not self.azure_client:
                    connection_string = self.config['azure_connection_string']
                    self.azure_client = azure.storage.blob.BlobServiceClient.from_connection_string(connection_string)
                
                container = self.azure_client.get_container_client(self.config['azure_container'])
                blob = container.get_blob_client(f"backups/{file_path.name}")
                with open(file_path, 'rb') as data:
                    blob.upload_blob(data, overwrite=True)
                logger.info("Uploaded to Azure", container=self.config['azure_container'], blob=blob.blob_name)
                
        except Exception as e:
            logger.error(f"Failed to upload to {cloud_type}", error=str(e))
    
    def cleanup_old_backups(self, days_to_keep=30):
        """Clean up old backup files"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for backup_file in self.backup_dir.glob("*"):
            if backup_file.is_file():
                file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
                if file_time < cutoff_date:
                    backup_file.unlink()
                    logger.info("Deleted old backup", file=str(backup_file))
    
    def run_full_backup(self):
        """Run complete backup process"""
        logger.info("Starting full backup process")
        
        try:
            self.connect_databases()
            
            backup_files = []
            
            # Backup each database
            pg_backup = self.backup_postgres()
            if pg_backup:
                backup_files.append(pg_backup)
            
            mongo_backup = self.backup_mongodb()
            if mongo_backup:
                backup_files.append(mongo_backup)
            
            redis_backup = self.backup_redis()
            if redis_backup:
                backup_files.append(redis_backup)
            
            # Backup corporate memory specifically
            memory_backup = self.backup_corporate_memory()
            if memory_backup:
                backup_files.append(memory_backup)
            
            # Upload to cloud storage if configured
            for backup_file in backup_files:
                if self.config.get('upload_to_s3'):
                    self.upload_to_cloud(backup_file, 's3')
                if self.config.get('upload_to_gcs'):
                    self.upload_to_cloud(backup_file, 'gcs')
                if self.config.get('upload_to_azure'):
                    self.upload_to_cloud(backup_file, 'azure')
            
            # Cleanup old backups
            self.cleanup_old_backups(self.config.get('backup_retention_days', 30))
            
            logger.info("Full backup process completed", files_created=len(backup_files))
            return backup_files
            
        except Exception as e:
            logger.error("Backup process failed", error=str(e))
            raise
        finally:
            if self.pg_conn:
                self.pg_conn.close()


@click.command()
@click.option('--config', '-c', 'config_file', default='backup_config.json', help='Configuration file')
@click.option('--backup-dir', default='./backups', help='Backup directory')
@click.option('--postgres-url', help='PostgreSQL connection URL')
@click.option('--mongodb-url', help='MongoDB connection URL')
@click.option('--redis-url', help='Redis connection URL')
@click.option('--upload-to-s3', is_flag=True, help='Upload to AWS S3')
@click.option('--upload-to-gcs', is_flag=True, help='Upload to Google Cloud Storage')
@click.option('--upload-to-azure', is_flag=True, help='Upload to Azure Blob Storage')
def main(config_file, backup_dir, postgres_url, mongodb_url, redis_url, 
         upload_to_s3, upload_to_gcs, upload_to_azure):
    """Corporate Memory Backup Tool"""
    
    # Load configuration
    config = {}
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    
    # Override with command line options
    if backup_dir:
        config['backup_dir'] = backup_dir
    if postgres_url:
        config['postgres_url'] = postgres_url
    if mongodb_url:
        config['mongodb_url'] = mongodb_url
    if redis_url:
        config['redis_url'] = redis_url
    if upload_to_s3:
        config['upload_to_s3'] = True
    if upload_to_gcs:
        config['upload_to_gcs'] = True
    if upload_to_azure:
        config['upload_to_azure'] = True
    
    # Run backup
    backup_manager = MemoryBackup(config)
    backup_files = backup_manager.run_full_backup()
    
    print(f"Backup completed successfully! Created {len(backup_files)} backup files.")


if __name__ == '__main__':
    main() 