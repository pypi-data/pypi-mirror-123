Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const utils_1 = require("app/components/events/interfaces/spans/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const spanTree_1 = (0, tslib_1.__importDefault)(require("./spanTree"));
const utils_2 = require("./utils");
const TraceView = (props) => {
    const { baselineEvent, regressionEvent } = props;
    if (!(0, utils_2.isTransactionEvent)(baselineEvent) || !(0, utils_2.isTransactionEvent)(regressionEvent)) {
        return (<emptyMessage_1.default>
        <icons_1.IconWarning color="gray300" size="lg"/>
        <p>{(0, locale_1.t)('One of the given events is not a transaction.')}</p>
      </emptyMessage_1.default>);
    }
    const baselineTraceContext = (0, utils_1.getTraceContext)(baselineEvent);
    const regressionTraceContext = (0, utils_1.getTraceContext)(regressionEvent);
    if (!baselineTraceContext || !regressionTraceContext) {
        return (<emptyMessage_1.default>
        <icons_1.IconWarning color="gray300" size="lg"/>
        <p>{(0, locale_1.t)('There is no trace found in either of the given transactions.')}</p>
      </emptyMessage_1.default>);
    }
    return <spanTree_1.default baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>;
};
exports.default = TraceView;
//# sourceMappingURL=traceView.jsx.map