"""Tests for dataform_check module"""
import pytest
from pathlib import Path
import tempfile
import shutil
from dataform_viz.dataform_check import cleanup_sqlx_files, normalize_name


class TestCleanupSqlxFiles:
    """Tests for cleanup_sqlx_files function"""
    
    def setup_method(self):
        """Create temporary directory for test files"""
        self.test_dir = tempfile.mkdtemp()
        self.definitions_dir = Path(self.test_dir) / "definitions"
        self.definitions_dir.mkdir()
    
    def teardown_method(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_cleanup_removes_project_id_from_config(self):
        """Test removal of *_utils.PROJECT_ID pattern from config block"""
        test_file = self.definitions_dir / "test.sqlx"
        content = """config {
  type: "table",
  database: wwim_utils.PROJECT_ID,
  schema: "staging"
}

SELECT * FROM `${wwim_utils.PROJECT_ID}.dataset.table`
"""
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
        cleaned = test_file.read_text(encoding='utf-8')
        # Config block should be cleaned
        assert 'database: wwim_utils.PROJECT_ID' not in cleaned
        # SQL query should remain untouched
        assert '${wwim_utils.PROJECT_ID}.dataset.table' in cleaned
    
    def test_cleanup_removes_different_utils_prefixes(self):
        """Test removal of various *_utils.PROJECT_ID patterns"""
        test_file = self.definitions_dir / "test.sqlx"
        content = """config {
  database: wwim_utils.PROJECT_ID,
  schema: abc_utils.PROJECT_ID
}

SELECT * FROM table
"""
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
        cleaned = test_file.read_text(encoding='utf-8')
        assert 'wwim_utils.PROJECT_ID' not in cleaned
        assert 'abc_utils.PROJECT_ID' not in cleaned
    
    def test_cleanup_preserves_sql_queries(self):
        """Test that SQL queries outside config are not modified"""
        test_file = self.definitions_dir / "test.sqlx"
        content = """config {
  type: "table",
  database: wwim_utils.PROJECT_ID
}

SELECT 
  customer_id,
  wwim_utils.PROJECT_ID as project_id
FROM `${wwim_utils.PROJECT_ID}.dataset.table`
WHERE schema = 'wwim_utils.PROJECT_ID'
"""
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
        cleaned = test_file.read_text(encoding='utf-8')
        # Config should be cleaned
        lines = cleaned.split('\n')
        config_section = '\n'.join([l for l in lines if l.strip().startswith('database')])
        assert 'wwim_utils.PROJECT_ID' not in config_section
        # SQL should be preserved
        assert 'wwim_utils.PROJECT_ID as project_id' in cleaned
        assert '${wwim_utils.PROJECT_ID}.dataset.table' in cleaned
        assert "schema = 'wwim_utils.PROJECT_ID'" in cleaned
    
    def test_cleanup_with_braces_pattern(self):
        """Test removal of ${*_utils.PROJECT_ID} pattern in config"""
        test_file = self.definitions_dir / "test.sqlx"
        content = """config {
  database: ${wwim_utils.PROJECT_ID},
  schema: "staging"
}
"""
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
        cleaned = test_file.read_text(encoding='utf-8')
        assert 'wwim_utils.PROJECT_ID' not in cleaned
    
    def test_cleanup_with_backticks(self):
        """Test removal of `${*_utils.PROJECT_ID}` pattern in config"""
        test_file = self.definitions_dir / "test.sqlx"
        content = """config {
  database: `${project_utils.PROJECT_ID}`,
  schema: "staging"
}
"""
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
        cleaned = test_file.read_text(encoding='utf-8')
        assert 'project_utils.PROJECT_ID' not in cleaned
    
    def test_cleanup_removes_trailing_whitespace(self):
        """Test removal of trailing whitespace"""
        test_file = self.definitions_dir / "test.sqlx"
        content = "config { type: \"table\" }   \nSELECT * FROM table  \n"
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
        cleaned = test_file.read_text(encoding='utf-8')
        assert '   \n' not in cleaned
        assert '  \n' not in cleaned
    
    def test_cleanup_removes_excessive_blank_lines(self):
        """Test removal of excessive blank lines"""
        test_file = self.definitions_dir / "test.sqlx"
        content = "config { type: \"table\" }\n\n\n\n\nSELECT * FROM table\n"
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
        cleaned = test_file.read_text(encoding='utf-8')
        # Should keep max 2 consecutive blank lines
        assert '\n\n\n\n\n' not in cleaned
    
    def test_cleanup_creates_backup(self):
        """Test that backup files are created"""
        test_file = self.definitions_dir / "test.sqlx"
        content = "config { database: wwim_utils.PROJECT_ID }\nSELECT * FROM table\n"
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=True)
        
        assert result == 1
        backup_file = self.definitions_dir / "test.sqlx.bak"
        assert backup_file.exists()
        assert backup_file.read_text(encoding='utf-8') == content
    
    def test_cleanup_no_changes_needed(self):
        """Test file with no changes needed"""
        test_file = self.definitions_dir / "test.sqlx"
        content = "config { type: \"table\" }\nSELECT * FROM table\n"
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 0
    
    def test_cleanup_multiple_files(self):
        """Test cleanup of multiple files"""
        for i in range(3):
            test_file = self.definitions_dir / f"test{i}.sqlx"
            content = f"config {{ database: project{i}_utils.PROJECT_ID }}\nSELECT * FROM table{i}\n"
            test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 3
    
    def test_cleanup_nested_directories(self):
        """Test cleanup in nested directories"""
        nested_dir = self.definitions_dir / "subdir"
        nested_dir.mkdir()
        test_file = nested_dir / "test.sqlx"
        content = "config { database: my_utils.PROJECT_ID }\nSELECT * FROM table\n"
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
    
    def test_cleanup_nonexistent_directory(self):
        """Test cleanup with nonexistent directory"""
        result = cleanup_sqlx_files("nonexistent_dir", backup=False)
        assert result == 0
    
    def test_cleanup_empty_directory(self):
        """Test cleanup with empty directory"""
        empty_dir = Path(self.test_dir) / "empty"
        empty_dir.mkdir()
        
        result = cleanup_sqlx_files(str(empty_dir), backup=False)
        assert result == 0
    
    def test_cleanup_multiline_config(self):
        """Test cleanup in multiline config block"""
        test_file = self.definitions_dir / "test.sqlx"
        content = """config {
  type: "table",
  database: wwim_utils.PROJECT_ID,
  schema: "staging",
  name: "customers"
}

SELECT * FROM source
"""
        test_file.write_text(content, encoding='utf-8')
        
        result = cleanup_sqlx_files(str(self.definitions_dir), backup=False)
        
        assert result == 1
        cleaned = test_file.read_text(encoding='utf-8')
        assert 'database: wwim_utils.PROJECT_ID' not in cleaned
        assert 'schema: "staging"' in cleaned
        assert 'name: "customers"' in cleaned


class TestNormalizeName:
    """Tests for normalize_name function"""
    
    def test_normalize_name_with_schema_and_name(self):
        """Test normalizing target with schema and name"""
        target = {"schema": "staging", "name": "customers"}
        result = normalize_name(target)
        assert result == "staging.customers"
    
    def test_normalize_name_with_empty_schema(self):
        """Test normalizing target with empty schema"""
        target = {"schema": "", "name": "customers"}
        result = normalize_name(target)
        assert result == ".customers"
    
    def test_normalize_name_with_none(self):
        """Test normalizing None target"""
        result = normalize_name(None)
        assert result == "UNKNOWN"
    
    def test_normalize_name_with_empty_dict(self):
        """Test normalizing empty target dict"""
        result = normalize_name({})
        assert result == "."
    
    def test_normalize_name_with_database(self):
        """Test normalizing target with database field"""
        target = {"database": "prod", "schema": "staging", "name": "customers"}
        result = normalize_name(target)
        # Function ignores database field
        assert result == "staging.customers"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
