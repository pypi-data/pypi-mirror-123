Object.defineProperty(exports, "__esModule", { value: true });
exports.AllTransactionsView = void 0;
const tslib_1 = require("tslib");
const pageError_1 = require("app/utils/performance/contexts/pageError");
const table_1 = (0, tslib_1.__importDefault)(require("../../table"));
const widgetChartRow_1 = require("../widgets/components/widgetChartRow");
const widgetDefinitions_1 = require("../widgets/widgetDefinitions");
function AllTransactionsView(props) {
    return (<div>
      <widgetChartRow_1.TripleChartRow {...props} allowedCharts={[
            widgetDefinitions_1.PerformanceWidgetSetting.USER_MISERY_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.TPM_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.FAILURE_RATE_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.APDEX_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.P50_DURATION_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.P95_DURATION_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.P99_DURATION_AREA,
        ]}/>
      <widgetChartRow_1.DoubleChartRow {...props} allowedCharts={[
            // TODO(k-fish): Temporarily adding extra charts here while trends widgets are in progress.
            widgetDefinitions_1.PerformanceWidgetSetting.TPM_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.TPM_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.TPM_AREA,
            widgetDefinitions_1.PerformanceWidgetSetting.MOST_IMPROVED,
            widgetDefinitions_1.PerformanceWidgetSetting.MOST_REGRESSED,
        ]}/>
      <table_1.default {...props} setError={(0, pageError_1.usePageError)().setPageError}/>
    </div>);
}
exports.AllTransactionsView = AllTransactionsView;
//# sourceMappingURL=allTransactionsView.jsx.map