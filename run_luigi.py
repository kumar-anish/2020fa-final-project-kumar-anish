import luigi

from final_project.tasks import SQLLogsToJSON

if __name__ == "__main__":
    luigi.build(
        [SQLLogsToJSON()],
        local_scheduler=True
    )