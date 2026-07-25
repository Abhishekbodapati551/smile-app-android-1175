import zipfile
from pathlib import Path
from automation.config.config import AUTOMATION_ROOT, PROJECT_ROOT, REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR
from automation.utils.logger import logger

class ZipGenerator:
    @staticmethod
    def create_automation_zip(zip_filename="smileapp-e2e-automation.zip") -> str:
        output_zip_path = PROJECT_ROOT / zip_filename
        logger.info(f"Creating ZIP bundle at {output_zip_path}...")

        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root_folder in [AUTOMATION_ROOT]:
                for file_path in root_folder.rglob("*"):
                    if "__pycache__" in file_path.parts or ".pytest_cache" in file_path.parts:
                        continue
                    arcname = file_path.relative_to(PROJECT_ROOT)
                    zip_file.write(file_path, arcname)

        logger.info(f"✓ ZIP bundle created successfully: {output_zip_path}")
        return str(output_zip_path)

if __name__ == "__main__":
    ZipGenerator.create_automation_zip()
