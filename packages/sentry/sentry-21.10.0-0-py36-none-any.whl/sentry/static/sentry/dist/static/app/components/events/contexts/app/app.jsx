Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const getUnknownData_1 = (0, tslib_1.__importDefault)(require("../getUnknownData"));
const getAppKnownData_1 = (0, tslib_1.__importDefault)(require("./getAppKnownData"));
const types_1 = require("./types");
const appKnownDataValues = [
    types_1.AppKnownDataType.ID,
    types_1.AppKnownDataType.START_TIME,
    types_1.AppKnownDataType.DEVICE_HASH,
    types_1.AppKnownDataType.IDENTIFIER,
    types_1.AppKnownDataType.NAME,
    types_1.AppKnownDataType.VERSION,
    types_1.AppKnownDataType.BUILD,
];
const appIgnoredDataValues = [];
const App = ({ data, event }) => (<react_1.Fragment>
    <contextBlock_1.default data={(0, getAppKnownData_1.default)(event, data, appKnownDataValues)}/>
    <contextBlock_1.default data={(0, getUnknownData_1.default)(data, [...appKnownDataValues, ...appIgnoredDataValues])}/>
  </react_1.Fragment>);
exports.default = App;
//# sourceMappingURL=app.jsx.map