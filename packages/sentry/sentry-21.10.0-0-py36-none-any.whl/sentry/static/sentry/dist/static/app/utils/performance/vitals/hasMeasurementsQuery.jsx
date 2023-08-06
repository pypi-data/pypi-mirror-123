Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const utils_1 = require("app/utils");
const genericDiscoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/genericDiscoverQuery"));
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
function getHasMeasurementsRequestPayload(props) {
    const { eventView, location, transaction, type } = props;
    const escaped = (0, utils_1.escapeDoubleQuotes)((0, tokenizeSearch_1.escapeFilterValue)(transaction));
    const baseApiPayload = {
        transaction: `"${escaped}"`,
        type,
    };
    const additionalApiPayload = (0, pick_1.default)(eventView.getEventsAPIPayload(location), [
        'project',
        'environment',
    ]);
    return Object.assign(baseApiPayload, additionalApiPayload);
}
function HasMeasurementsQuery(props) {
    return (<genericDiscoverQuery_1.default route="events-has-measurements" getRequestPayload={getHasMeasurementsRequestPayload} {...(0, omit_1.default)(props, 'children')}>
      {(_a) => {
            var _b;
            var { tableData } = _a, rest = (0, tslib_1.__rest)(_a, ["tableData"]);
            return props.children(Object.assign({ hasMeasurements: (_b = tableData === null || tableData === void 0 ? void 0 : tableData.measurements) !== null && _b !== void 0 ? _b : null }, rest));
        }}
    </genericDiscoverQuery_1.default>);
}
exports.default = (0, withApi_1.default)(HasMeasurementsQuery);
//# sourceMappingURL=hasMeasurementsQuery.jsx.map