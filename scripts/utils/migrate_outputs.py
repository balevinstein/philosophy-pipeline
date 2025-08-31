#!/usr/bin/env python3
"""
Migration script to organize existing outputs into the new output management structure.

This script:
1. Identifies existing output files 
2. Categorizes them by phase
3. Moves them to the new current/ directory structure
4. Creates appropriate metadata
5. Archives the old structure
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add project root to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.outputs import OutputManager


def identify_phase_files(outputs_dir: Path) -> Dict[str, List[Path]]:
    """Identify which files belong to which phases"""
    phase_files = {
        "phase_1": [],
        "phase_2": [],  
        "phase_3": [],
        "general": []
    }
    
    # Phase 1 patterns (conceptual development)
    phase_1_patterns = [
        "**/conceptual_*.json",
        "**/final_selection.json",
        "**/culled_topics.json",
        "**/literature_readings.json"
    ]
    
    # Phase 2 patterns (framework and analysis)
    phase_2_patterns = [
        "**/framework_development/**",
        "**/key_moves_development/**",
        "**/literature_synthesis.*",
        "**/phase_two_two_*"
    ]
    
    # Phase 3 patterns (writing and integration)
    phase_3_patterns = [
        "**/writing/**",
        "**/integration/**",
        "**/final_paper*"
    ]
    
    # Collect files for each phase
    for pattern in phase_1_patterns:
        matches = outputs_dir.glob(pattern)
        phase_files["phase_1"].extend([f for f in matches if f.is_file()])
    
    for pattern in phase_2_patterns:
        matches = outputs_dir.glob(pattern)
        phase_files["phase_2"].extend([f for f in matches if f.is_file()])
    
    for pattern in phase_3_patterns:
        matches = outputs_dir.glob(pattern)
        phase_files["phase_3"].extend([f for f in matches if f.is_file()])
    
    # Find all other files
    all_files = set(f for f in outputs_dir.rglob("*") if f.is_file())
    categorized_files = set()
    for files in phase_files.values():
        categorized_files.update(files)
    
    uncategorized = all_files - categorized_files
    # Filter out files we don't want to migrate
    exclude_patterns = {".DS_Store", "Thumbs.db", "*.pyc", "*.pyo", "__pycache__"}
    for file in uncategorized:
        if not any(file.name.startswith('.') or file.match(pattern) for pattern in exclude_patterns):
            phase_files["general"].append(file)
    
    return phase_files


def create_migration_metadata(source_dir: Path, phase_files: Dict[str, List[Path]]) -> Dict[str, Any]:
    """Create metadata for the migration"""
    total_files = sum(len(files) for files in phase_files.values())
    total_size = sum(f.stat().st_size for files in phase_files.values() for f in files)
    
    metadata = {
        "migration_id": f"legacy_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "migrated_at": datetime.now().isoformat(),
        "source_directory": str(source_dir),
        "migration_summary": {
            "total_files_migrated": total_files,
            "total_size_bytes": total_size,
            "files_by_phase": {phase: len(files) for phase, files in phase_files.items()}
        },
        "phase_mappings": {
            phase: [str(f.relative_to(source_dir)) for f in files]
            for phase, files in phase_files.items()
        }
    }
    
    return metadata


def migrate_files(phase_files: Dict[str, List[Path]], current_dir: Path, outputs_dir: Path):
    """Migrate files to new structure"""
    
    for phase, files in phase_files.items():
        if not files:
            continue
            
        phase_dir = current_dir / phase
        phase_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Migrating {len(files)} files to {phase}...")
        
        for file_path in files:
            try:
                # Calculate relative path from outputs directory
                rel_path = file_path.relative_to(outputs_dir)
                
                # Create destination path maintaining directory structure
                dest_path = phase_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file (don't move original yet)
                shutil.copy2(file_path, dest_path)
                print(f"  Copied: {rel_path}")
                
            except Exception as e:
                print(f"  Error copying {file_path}: {e}")


def create_run_metadata(migration_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Create run metadata for the migrated content"""
    return {
        "run_id": migration_metadata["migration_id"],
        "created_at": migration_metadata["migrated_at"],
        "status": "migrated_legacy",
        "phases_completed": [],  # Will be updated based on what files we found
        "total_files": migration_metadata["migration_summary"]["total_files_migrated"],
        "pipeline_version": "1.0.0",
        "migration_info": {
            "is_migrated_run": True,
            "original_source": migration_metadata["source_directory"],
            "migration_date": migration_metadata["migrated_at"]
        }
    }


def main():
    """Main migration function"""
    print("🚚 Starting outputs migration to new structure...")
    
    project_root = Path(__file__).parent
    outputs_dir = project_root / "outputs"
    
    if not outputs_dir.exists():
        print("❌ No outputs directory found to migrate")
        return
    
    # Initialize output manager
    output_manager = OutputManager()
    
    # Identify files to migrate
    print("🔍 Identifying files to migrate...")
    phase_files = identify_phase_files(outputs_dir)
    
    # Show summary
    print("\n📊 Migration Summary:")
    for phase, files in phase_files.items():
        print(f"  {phase}: {len(files)} files")
    
    if sum(len(files) for files in phase_files.values()) == 0:
        print("ℹ️  No files found to migrate")
        return
    
    # Create migration metadata
    migration_metadata = create_migration_metadata(outputs_dir, phase_files)
    
    # Create new run directory
    print("\n📁 Creating new run directory for migrated content...")
    run_dir = output_manager.create_run_directory(migration_metadata["migration_id"])
    
    # Migrate files
    print("\n📦 Migrating files to new structure...")
    migrate_files(phase_files, run_dir, outputs_dir)
    
    # Create run metadata
    print("\n📄 Creating run metadata...")
    run_metadata = create_run_metadata(migration_metadata)
    
    # Determine phases completed based on files found
    phases_completed = []
    if phase_files["phase_1"]:
        phases_completed.append("phase_1")
    if phase_files["phase_2"]: 
        phases_completed.append("phase_2")
    if phase_files["phase_3"]:
        phases_completed.append("phase_3")
    
    run_metadata["phases_completed"] = phases_completed
    
    # Save run metadata
    metadata_file = run_dir / "run_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(run_metadata, f, indent=2)
    
    # Save migration details
    migration_file = run_dir / "migration_metadata.json"
    with open(migration_file, 'w') as f:
        json.dump(migration_metadata, f, indent=2)
    
    # Create backup of original structure
    print("\n💾 Creating backup of original outputs...")
    backup_dir = project_root / "outputs_backup_pre_migration"
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    
    # Only backup non-empty directories and files we care about
    backup_dir.mkdir()
    for item in outputs_dir.iterdir():
        if item.name not in {"current", "archive", "templates", "analysis"}:
            if item.is_file():
                shutil.copy2(item, backup_dir / item.name)
            elif item.is_dir() and any(item.iterdir()):
                shutil.copytree(item, backup_dir / item.name)
    
    print(f"✅ Migration completed successfully!")
    print(f"📁 Migrated content available in: {run_dir}")
    print(f"💾 Original outputs backed up to: {backup_dir}")
    print(f"🏷️  Run ID: {migration_metadata['migration_id']}")
    
    # Show next steps
    print("\n📋 Next Steps:")
    print("1. Verify migrated content looks correct")
    print("2. Test the new output management commands:")
    print("   python pipeline_cli.py outputs --list")
    print("   python pipeline_cli.py outputs --statistics")
    print("3. If satisfied, you can remove the backup directory")
    print("4. Use 'python pipeline_cli.py outputs --archive' to archive this migrated content")


if __name__ == "__main__":
    main()