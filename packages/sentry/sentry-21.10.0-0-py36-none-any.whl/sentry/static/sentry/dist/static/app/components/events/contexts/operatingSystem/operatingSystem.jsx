Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const getUnknownData_1 = (0, tslib_1.__importDefault)(require("../getUnknownData"));
const getOperatingSystemKnownData_1 = (0, tslib_1.__importDefault)(require("./getOperatingSystemKnownData"));
const types_1 = require("./types");
const operatingSystemKnownDataValues = [
    types_1.OperatingSystemKnownDataType.NAME,
    types_1.OperatingSystemKnownDataType.VERSION,
    types_1.OperatingSystemKnownDataType.KERNEL_VERSION,
    types_1.OperatingSystemKnownDataType.ROOTED,
];
const operatingSystemIgnoredDataValues = [types_1.OperatingSystemIgnoredDataType.BUILD];
const OperatingSystem = ({ data }) => (<react_1.Fragment>
    <contextBlock_1.default data={(0, getOperatingSystemKnownData_1.default)(data, operatingSystemKnownDataValues)}/>
    <contextBlock_1.default data={(0, getUnknownData_1.default)(data, [
        ...operatingSystemKnownDataValues,
        ...operatingSystemIgnoredDataValues,
    ])}/>
  </react_1.Fragment>);
exports.default = OperatingSystem;
//# sourceMappingURL=operatingSystem.jsx.map