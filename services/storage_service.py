import os
import uuid
from pathlib import Path
from typing import Optional
import shutil

class StorageService:
    def __init__(self):
        self.storage_type = os.getenv("STORAGE_TYPE", "local")
        self.local_path = Path(os.getenv("UPLOAD_DIR", "uploads"))
        self.local_path.mkdir(exist_ok=True)
        
        # AWS S3 config
        self.aws_bucket = os.getenv("AWS_S3_BUCKET", "")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
    
    def save_file(self, file_content: bytes, filename: str, folder: str = "general") -> str:
        if self.storage_type == "s3" and self.aws_bucket:
            return self._save_to_s3(file_content, filename, folder)
        else:
            return self._save_locally(file_content, filename, folder)
    
    def _save_locally(self, file_content: bytes, filename: str, folder: str) -> str:
        folder_path = self.local_path / folder
        folder_path.mkdir(exist_ok=True)
        
        # Gerar nome único
        ext = Path(filename).suffix
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = folder_path / unique_name
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return f"/uploads/{folder}/{unique_name}"
    
    def _save_to_s3(self, file_content: bytes, filename: str, folder: str) -> str:
        try:
            import boto3
            
            s3_client = boto3.client('s3', region_name=self.aws_region)
            
            ext = Path(filename).suffix
            unique_name = f"{folder}/{uuid.uuid4()}{ext}"
            
            s3_client.put_object(
                Bucket=self.aws_bucket,
                Key=unique_name,
                Body=file_content
            )
            
            return f"https://{self.aws_bucket}.s3.{self.aws_region}.amazonaws.com/{unique_name}"
        except ImportError:
            print("⚠️ boto3 não instalado. Use: pip install boto3")
            return self._save_locally(file_content, filename, folder)
        except Exception as e:
            print(f"❌ Erro ao salvar no S3: {e}")
            return self._save_locally(file_content, filename, folder)
    
    def delete_file(self, file_url: str) -> bool:
        try:
            if file_url.startswith("/uploads/"):
                file_path = self.local_path / file_url.replace("/uploads/", "")
                if file_path.exists():
                    file_path.unlink()
                    return True
            elif self.storage_type == "s3":
                import boto3
                s3_client = boto3.client('s3', region_name=self.aws_region)
                key = file_url.split(f"{self.aws_bucket}.s3.{self.aws_region}.amazonaws.com/")[1]
                s3_client.delete_object(Bucket=self.aws_bucket, Key=key)
                return True
        except Exception as e:
            print(f"❌ Erro ao deletar arquivo: {e}")
        return False

storage_service = StorageService()