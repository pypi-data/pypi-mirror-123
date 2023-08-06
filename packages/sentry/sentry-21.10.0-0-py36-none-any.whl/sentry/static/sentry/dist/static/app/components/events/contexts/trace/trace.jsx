Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const getUnknownData_1 = (0, tslib_1.__importDefault)(require("../getUnknownData"));
const getTraceKnownData_1 = (0, tslib_1.__importDefault)(require("./getTraceKnownData"));
const types_1 = require("./types");
const traceKnownDataValues = [
    types_1.TraceKnownDataType.STATUS,
    types_1.TraceKnownDataType.TRACE_ID,
    types_1.TraceKnownDataType.SPAN_ID,
    types_1.TraceKnownDataType.PARENT_SPAN_ID,
    types_1.TraceKnownDataType.TRANSACTION_NAME,
    types_1.TraceKnownDataType.OP_NAME,
];
const traceIgnoredDataValues = [];
const InnerTrace = (0, withOrganization_1.default)(function ({ organization, event, data }) {
    return (<errorBoundary_1.default mini>
      <keyValueList_1.default data={(0, getTraceKnownData_1.default)(data, traceKnownDataValues, event, organization)} isSorted={false} raw={false}/>
      <keyValueList_1.default data={(0, getUnknownData_1.default)(data, [...traceKnownDataValues, ...traceIgnoredDataValues])} isSorted={false} raw={false}/>
    </errorBoundary_1.default>);
});
const Trace = (props) => {
    return <InnerTrace {...props}/>;
};
exports.default = Trace;
//# sourceMappingURL=trace.jsx.map