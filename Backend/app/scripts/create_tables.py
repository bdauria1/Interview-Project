import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.core.database import get_engine, Base
import app.models.product_inspection
import app.models.molding_machine_state
import app.models.object_detection
import app.models.defect
import app.models.pixel_severity
from sqlalchemy import inspect

def main():
    engine = get_engine()
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()