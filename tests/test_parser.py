"""Tests for parser module"""
import pytest
from pathlib import Path
import tempfile
from dataform_viz.parser import parse_dependencies_report


class TestParseDependenciesReport:
    """Tests for parse_dependencies_report function"""
    
    def setup_method(self):
        """Create temporary directory for test files"""
        self.test_dir = tempfile.mkdtemp()
    
    def test_parse_simple_table(self):
        """Test parsing a simple table with dependencies"""
        report_file = Path(self.test_dir) / "report.txt"
        content = """Table: staging.customers (table)
  Dependencies (1):
    <- source.raw_customers
  Dependents (1):
    -> analytics.customer_summary
"""
        report_file.write_text(content, encoding='utf-8')
        
        result = parse_dependencies_report(str(report_file))
        
        assert "staging.customers" in result
        assert result["staging.customers"]["type"] == "table"
        assert "source.raw_customers" in result["staging.customers"]["dependencies"]
        assert "analytics.customer_summary" in result["staging.customers"]["dependents"]
    
    def test_parse_multiple_tables(self):
        """Test parsing multiple tables"""
        report_file = Path(self.test_dir) / "report.txt"
        content = """Table: staging.customers (table)
  Dependencies (0):
  Dependents (1):
    -> analytics.summary

Table: analytics.summary (view)
  Dependencies (1):
    <- staging.customers
  Dependents (0):
"""
        report_file.write_text(content, encoding='utf-8')
        
        result = parse_dependencies_report(str(report_file))
        
        assert len(result) == 2
        assert "staging.customers" in result
        assert "analytics.summary" in result
        assert result["analytics.summary"]["type"] == "view"
    
    def test_parse_table_with_multiple_dependencies(self):
        """Test parsing table with multiple dependencies"""
        report_file = Path(self.test_dir) / "report.txt"
        content = """Table: analytics.combined (table)
  Dependencies (3):
    <- staging.customers
    <- staging.orders
    <- staging.products
  Dependents (0):
"""
        report_file.write_text(content, encoding='utf-8')
        
        result = parse_dependencies_report(str(report_file))
        
        assert len(result["analytics.combined"]["dependencies"]) == 3
        assert "staging.customers" in result["analytics.combined"]["dependencies"]
        assert "staging.orders" in result["analytics.combined"]["dependencies"]
        assert "staging.products" in result["analytics.combined"]["dependencies"]
    
    def test_parse_file_not_found(self):
        """Test parsing nonexistent file"""
        with pytest.raises(FileNotFoundError):
            parse_dependencies_report("nonexistent.txt")
    
    def test_parse_empty_file(self):
        """Test parsing empty file"""
        report_file = Path(self.test_dir) / "empty.txt"
        report_file.write_text("", encoding='utf-8')
        
        result = parse_dependencies_report(str(report_file))
        
        assert result == {}
    
    def test_parse_different_table_types(self):
        """Test parsing different table types"""
        report_file = Path(self.test_dir) / "report.txt"
        content = """Table: staging.data (table)
  Dependencies (0):
  Dependents (0):

Table: analytics.view (view)
  Dependencies (0):
  Dependents (0):

Table: ops.operation (operation)
  Dependencies (0):
  Dependents (0):
"""
        report_file.write_text(content, encoding='utf-8')
        
        result = parse_dependencies_report(str(report_file))
        
        assert result["staging.data"]["type"] == "table"
        assert result["analytics.view"]["type"] == "view"
        assert result["ops.operation"]["type"] == "operation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
