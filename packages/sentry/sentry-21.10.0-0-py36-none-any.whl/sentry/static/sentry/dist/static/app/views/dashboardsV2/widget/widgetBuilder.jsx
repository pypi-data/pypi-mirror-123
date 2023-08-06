Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const eventWidget_1 = (0, tslib_1.__importDefault)(require("./eventWidget"));
const metricWidget_1 = (0, tslib_1.__importDefault)(require("./metricWidget"));
const utils_2 = require("./utils");
function WidgetBuilder({ dashboard, onSave, widget, params, location, router, organization, }) {
    const [dataSet, setDataSet] = (0, react_1.useState)(utils_2.DataSet.EVENTS);
    const isEditing = !!widget;
    const { widgetId, orgId, dashboardId } = params;
    const goBackLocation = {
        pathname: dashboardId
            ? `/organizations/${orgId}/dashboard/${dashboardId}/`
            : `/organizations/${orgId}/dashboards/new/`,
        query: Object.assign(Object.assign({}, location.query), { dataSet: undefined }),
    };
    (0, react_1.useEffect)(() => {
        checkDataSet();
    });
    function checkDataSet() {
        const { query } = location;
        const queryDataSet = query === null || query === void 0 ? void 0 : query.dataSet;
        if (!queryDataSet) {
            router.replace({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { dataSet: utils_2.DataSet.EVENTS }),
            });
            return;
        }
        if (queryDataSet !== utils_2.DataSet.EVENTS && queryDataSet !== utils_2.DataSet.METRICS) {
            setDataSet(undefined);
            return;
        }
        if (queryDataSet === utils_2.DataSet.METRICS) {
            if (dataSet === utils_2.DataSet.METRICS) {
                return;
            }
            setDataSet(utils_2.DataSet.METRICS);
            return;
        }
        if (dataSet === utils_2.DataSet.EVENTS) {
            return;
        }
        setDataSet(utils_2.DataSet.EVENTS);
    }
    function handleDataSetChange(newDataSet) {
        router.replace({
            pathname: location.pathname,
            query: Object.assign(Object.assign({}, location.query), { dataSet: newDataSet }),
        });
    }
    if (!dataSet) {
        return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
        {(0, locale_1.t)('Data set not found.')}
      </alert_1.default>);
    }
    function handleAddWidget(newWidget) {
        onSave([...dashboard.widgets, newWidget]);
    }
    if ((isEditing && !(0, utils_1.defined)(widgetId)) ||
        (isEditing && (0, utils_1.defined)(widgetId) && !dashboard.widgets[widgetId])) {
        return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
        {(0, locale_1.t)('Widget not found.')}
      </alert_1.default>);
    }
    function handleUpdateWidget(nextWidget) {
        if (!widgetId) {
            return;
        }
        const nextList = [...dashboard.widgets];
        nextList[widgetId] = nextWidget;
        onSave(nextList);
    }
    function handleDeleteWidget() {
        if (!widgetId) {
            return;
        }
        const nextList = [...dashboard.widgets];
        nextList.splice(widgetId, 1);
        onSave(nextList);
    }
    if (dataSet === utils_2.DataSet.EVENTS) {
        return (<eventWidget_1.default dashboardTitle={dashboard.title} widget={widget} onAdd={handleAddWidget} onUpdate={handleUpdateWidget} onDelete={handleDeleteWidget} onChangeDataSet={handleDataSetChange} goBackLocation={goBackLocation} isEditing={isEditing}/>);
    }
    return (<metricWidget_1.default organization={organization} router={router} location={location} dashboardTitle={dashboard.title} params={params} goBackLocation={goBackLocation} onChangeDataSet={handleDataSetChange}/>);
}
exports.default = WidgetBuilder;
//# sourceMappingURL=widgetBuilder.jsx.map