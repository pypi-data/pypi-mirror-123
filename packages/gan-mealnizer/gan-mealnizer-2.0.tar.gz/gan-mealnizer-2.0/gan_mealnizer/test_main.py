from typer.testing import CliRunner
import json
from main import app

runner = CliRunner()

def test_app():
    result = runner.invoke(app, ["run", "superactive", "2016-07-01", "2016-12-25"])
    assert result.exit_code == 0
    assert '2' in result.stdout
    assert '34407' in result.stdout