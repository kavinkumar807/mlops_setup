import evidently
from evidently import DataDefinition, Dataset, Regression
from evidently.core.report import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset, RegressionPreset
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import Project
from evidently.sdk.models import PanelMetric
from evidently.sdk.panels import DashboardPanelPlot
from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime
from typing import List



class GenerateReport(ABC):
    @abstractmethod
    def create_report(self, workspace, project, reference, current, column_mapping):
        pass

class DataDriftReport(GenerateReport):
    def create_report(self, workspace: Workspace, project: Project, reference, current):
        data_drift_report = Report(metrics=[DataDriftPreset()], tags=["drift_rep"], include_tests=True)
        data_drift_report = data_drift_report.run(reference_data=reference, current_data=current)
        workspace.add_run(project_id=project.id, run=data_drift_report)
        return data_drift_report

class DataSummaryReport(GenerateReport):
    def create_report(self, workspace: Workspace, project: Project, reference, current):
        data_quality_report = Report(metrics=[DataSummaryPreset()], tags=["summary_rep"], include_tests=True)
        data_quality_report = data_quality_report.run(reference_data=reference, current_data=current)
        workspace.add_run(project_id=project.id, run=data_quality_report)
        return data_quality_report

class RegressionReport(GenerateReport):
    def create_report(self, workspace: Workspace, project: Project, reference, current):
        regression_performance_report = Report(metrics=[RegressionPreset()], tags=["regression_rep"], include_tests=True)
        regression_performance_report = regression_performance_report.run(reference_data=reference, current_data=current)
        workspace.add_run(project_id=project.id, run=regression_performance_report)
        return regression_performance_report
 


class Monitoring:
    def __init__(self, strategy = DataDriftReport()):
        self._strategy = strategy
        self._workspace = None
        self._project = None
        self._schema = None

    def create_workspace(self, name:str):
        self._workspace = Workspace.create(name)
        return self._workspace
    
    def search_or_create_project(self, project_name:str, workspace: Workspace = None):
        if(self._workspace is None):
            self._workspace = workspace
        project_list = self._workspace.search_project(project_name=project_name)
        if(len(project_list) == 0):
            self._project = self._workspace.create_project(project_name)
        else:
            self._project = project_list[0]
        return self._project
    
    def set_schema(self, numerical_columns:list, categorical_columns:list, regression: List[Regression]):
        self._schema = DataDefinition(
            numerical_columns=numerical_columns,
            categorical_columns=categorical_columns,
            regression=regression
        )
        return self._schema
        
    @property
    def current_strategy(self):
        return self._strategy
        
    @current_strategy.setter
    def set_strategy(self, strategy: DataDriftReport):
        self._strategy = strategy

    def execute_strategy(self, reference: pd.DataFrame, current: pd.DataFrame, workspace: Workspace = None):
        if(self._workspace is None):
            self._workspace = workspace
        eval_ref = Dataset.from_pandas(data=pd.DataFrame(reference), data_definition=self._schema)
        eval_curr = Dataset.from_pandas(data=pd.DataFrame(current), data_definition=self._schema)
        report = self._strategy.create_report(self._workspace, self._project, eval_ref, eval_curr)
        print("Report Created successfully!!")
        return report

    def add_dashboard_panel(self, project: Project, panel_type: str, **kwargs):
        match panel_type:
            case "Counter":
                # project.dashboard.add_panel(
                #     DashboardPanelCounter(
                #         title=kwargs["title"],
                #         filter=ReportFilter(metadata_values={}, tag_values=kwargs["tags"]),
                #         value=PanelValue(
                #             metric_id=kwargs["metric_id"],
                #             field_path=kwargs["field_path"],
                #             legend=kwargs["legend"],
                #         ),
                #         text=kwargs["text"],
                #         agg=kwargs["agg"],
                #         size=kwargs["size"],
                #     )
                # )
            #     values = []
    
            # # Only create PanelMetric if metric_id is provided
            #     if kwargs.get("metric_id") is not None:
            #         values = [PanelMetric(
            #             legend=kwargs.get("legend", ""),
            #             metric=kwargs["metric_id"],  # Must be a valid metric name
            #             metric_labels=kwargs.get("metric_labels", {}),
            #     )]
                project.dashboard.add_panel(
                    DashboardPanelPlot(
                        title=kwargs["title"],
                        size=kwargs.get("size", "full"),  # "full" or "half"
                        values=[
                            PanelMetric(
                                legend=kwargs["legend"],
                                metric=kwargs["metric_id"],  # e.g., "RowCount", "Accuracy"
                                metric_labels=kwargs.get("metric_labels", {}),  # e.g., {"column": "target"}
                            )
                        ],
                        plot_params={
                            "plot_type": "counter",
                            "aggregation": kwargs.get("agg", "last"),  # "sum", "avg", "last"
                        },
                    ),
                    tab=kwargs.get("tab", "General")
                )
            case "Text":
                project.dashboard.add_panel(
                    DashboardPanelPlot(
                        title=kwargs["title"],
                        subtitle=kwargs.get("subtitle", ""),
                        size=kwargs.get("size", "full"),
                        values=[],  # Empty = text only
                        plot_params={"plot_type": "text"},
                    ),
                    tab=kwargs.get("tab", "General")
                )

            case "Plot":
            #     project.dashboard.add_panel(
            #         DashboardPanelPlot(
            #             title=kwargs["title"],
            #             filter=ReportFilter(metadata_values={}, tag_values=[]),
            #             values=[
            #                 PanelValue(
            #                     metric_id=kwargs["metric_id"],
            #                     metric_args=kwargs["metric_args"],
            #                     field_path=kwargs["field_path"],
            #                     legend=kwargs["legend"]
            #                 ),
            #             ],
            #             plot_type=kwargs["plot_type"],
            #             size=kwargs["size"]
            #         )
            #     )
                project.dashboard.add_panel(
                DashboardPanelPlot(
                    title=kwargs["title"],
                    subtitle=kwargs.get("subtitle", ""),
                    size=kwargs.get("size", "full"),  # "full" or "half"
                    values=[
                        PanelMetric(
                            legend=kwargs["legend"],
                            metric=kwargs["metric_id"],  # e.g., "RowCount", "Accuracy"
                            metric_labels=kwargs.get("metric_args", {}),  # Replaces metric_args + field_path
                        )
                    ],
                    plot_params={
                        "plot_type": kwargs["plot_type"],  # "line", "bar", "text", etc.
                        "is_stacked": kwargs.get("is_stacked", False),  # For bar charts
                    },
                ),
                tab=kwargs.get("tab", "General")
            )
                
            case "MultiPlot":
                # project.dashboard.add_panel(
                #     DashboardPanelPlot(
                #         title=kwargs["title"],
                #         filter=ReportFilter(metadata_values={}, tag_values=[]),
                #         values=[
                #             PanelValue(
                #                 metric_id=kwargs["metric_id"],
                #                 metric_args=kwargs["metric_args"],
                #                 field_path=kwargs["field_path"],
                #                 legend=kwargs["legend"]
                #             ),
                #             PanelValue(
                #                 metric_id=kwargs["metric_id_2"],
                #                 metric_args=kwargs["metric_args_2"],
                #                 field_path=kwargs["field_path_2"],
                #                 legend=kwargs["legend_2"]
                #             ),
                #         ],
                #         plot_type=kwargs["plot_type"],
                #         size=kwargs["size"]
                #     )
                # )
                project.dashboard.add_panel(
                DashboardPanelPlot(
                    title=kwargs["title"],
                    subtitle=kwargs.get("subtitle", ""),
                    size=kwargs.get("size", "full"),
                    values=[
                        PanelMetric(
                            legend=kwargs["legend"],
                            metric=kwargs["metric_id"],
                            metric_labels={**kwargs.get("metric_args", {}), **kwargs.get("field_path", {})},
                        ),
                        PanelMetric(
                            legend=kwargs["legend_2"],
                            metric=kwargs["metric_id_2"],
                            metric_labels={**kwargs.get("metric_args_2", {}), **kwargs.get("field_path_2", {})},
                        ),
                    ],
                    plot_params={
                        "plot_type": kwargs["plot_type"],  # "line", "bar", etc.
                        "is_stacked": kwargs.get("is_stacked", False),  # Optional for bar charts
                    },
                ),
                tab=kwargs.get("tab", "General")
            )

            case "TestSuite":
                # project.dashboard.add_panel(
                #     DashboardPanelTestSuite(
                #         title="All tests: detailed",
                #         filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
                #         size=WidgetSize.FULL,
                #         panel_type=TestSuitePanelType.DETAILED,
                #         time_agg="1H",
                #     )
                # )
                project.dashboard.add_panel(
                DashboardPanelPlot(
                    title=kwargs.get("title", "Test Summary"),
                    size=kwargs.get("size", "full"),
                    values=[
                        PanelMetric(legend="Failed Tests", metric="TestFailedCount"),
                        PanelMetric(legend="Passed Tests", metric="TestPassedCount"),
                    ],
                    plot_params={"plot_type": "counter", "aggregation": "last"},
                ),
                tab=kwargs.get("tab", "Tests")
            )

            case _:
                print("Specified panel type not defined!")
                
        project.save()
        print(f"Panel {panel_type} created!!")

    def delete_dashboard(self, project: Project, title: str, tab: str):
        project.dashboard.delete_panel(title, tab)
        project.save()
        print("Panels deleted!!")






