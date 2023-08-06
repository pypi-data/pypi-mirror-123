Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const getUnknownData_1 = (0, tslib_1.__importDefault)(require("../getUnknownData"));
const getRuntimeKnownData_1 = (0, tslib_1.__importDefault)(require("./getRuntimeKnownData"));
const types_1 = require("./types");
const runtimeKnownDataValues = [types_1.RuntimeKnownDataType.NAME, types_1.RuntimeKnownDataType.VERSION];
const runtimeIgnoredDataValues = [types_1.RuntimeIgnoredDataType.BUILD];
const Runtime = ({ data }) => {
    return (<react_1.Fragment>
      <contextBlock_1.default data={(0, getRuntimeKnownData_1.default)(data, runtimeKnownDataValues)}/>
      <contextBlock_1.default data={(0, getUnknownData_1.default)(data, [
            ...runtimeKnownDataValues,
            ...runtimeIgnoredDataValues,
        ])}/>
    </react_1.Fragment>);
};
exports.default = Runtime;
//# sourceMappingURL=runtime.jsx.map