import csv

from final_project import models
from final_project.database import SessionLocal, engine

def load_query_result_file():
    db = SessionLocal()

    models.Base.metadata.create_all(bind=engine)
    print("loading csv results to database - start...")
    with open("data/query_result_file.csv", "r") as f:
        csv_reader = csv.DictReader(f)

        for row in csv_reader:
            db_record = models.QueryResult(
                QueryID=row["QueryID"],
                MatchScore=row["MatchScore"],
            )
            db.add(db_record)

        db.commit()
    print("loading csv results to database - end...")
    db.close()
