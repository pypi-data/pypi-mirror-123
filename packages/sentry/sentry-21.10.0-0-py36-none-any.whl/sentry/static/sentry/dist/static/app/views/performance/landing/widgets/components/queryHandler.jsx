Object.defineProperty(exports, "__esModule", { value: true });
exports.QueryHandler = void 0;
const react_1 = require("react");
const dates_1 = require("app/utils/dates");
/*
  Component to handle switching component-style queries over to state. This should be temporary to make it easier to switch away from waterfall style api components.
*/
function QueryHandler(props) {
    var _a;
    const children = (_a = props.children) !== null && _a !== void 0 ? _a : <react_1.Fragment />;
    if (!props.queries.length) {
        return <react_1.Fragment>{children}</react_1.Fragment>;
    }
    const globalSelection = props.queryProps.eventView.getGlobalSelection();
    const start = globalSelection.datetime.start
        ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.start)
        : null;
    const end = globalSelection.datetime.end
        ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.end)
        : null;
    return (<react_1.Fragment>
      {props.queries
            .filter(q => (q.enabled ? q.enabled(props.widgetData) : true))
            .map(query => (<query.component key={query.queryKey} fields={query.fields} yAxis={query.fields} start={start} end={end} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} organization={props.queryProps.organization}>
            {results => {
                return (<react_1.Fragment>
                  <QueryResultSaver results={results} {...props} query={query}/>
                </react_1.Fragment>);
            }}
          </query.component>))}
    </react_1.Fragment>);
}
exports.QueryHandler = QueryHandler;
function QueryResultSaver(props) {
    const { results, query } = props;
    const transformed = query.transform(props.queryProps, results, props.query);
    (0, react_1.useEffect)(() => {
        props.setWidgetDataForKey(query.queryKey, transformed);
    }, [transformed === null || transformed === void 0 ? void 0 : transformed.hasData, transformed === null || transformed === void 0 ? void 0 : transformed.isLoading, transformed === null || transformed === void 0 ? void 0 : transformed.isErrored]);
    return <react_1.Fragment />;
}
//# sourceMappingURL=queryHandler.jsx.map