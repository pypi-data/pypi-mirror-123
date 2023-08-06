Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const getUnknownData_1 = (0, tslib_1.__importDefault)(require("../getUnknownData"));
const getGPUKnownData_1 = (0, tslib_1.__importDefault)(require("./getGPUKnownData"));
const types_1 = require("./types");
const gpuKnownDataValues = [
    types_1.GPUKnownDataType.NAME,
    types_1.GPUKnownDataType.VERSION,
    types_1.GPUKnownDataType.VENDOR_NAME,
    types_1.GPUKnownDataType.MEMORY,
    types_1.GPUKnownDataType.NPOT_SUPPORT,
    types_1.GPUKnownDataType.MULTI_THREAD_RENDERING,
    types_1.GPUKnownDataType.API_TYPE,
];
const gpuIgnoredDataValues = [];
const GPU = ({ data }) => {
    if (data.vendor_id > 0) {
        gpuKnownDataValues.unshift[types_1.GPUKnownDataType.VENDOR_ID];
    }
    if (data.id > 0) {
        gpuKnownDataValues.unshift[types_1.GPUKnownDataType.ID];
    }
    return (<react_1.Fragment>
      <contextBlock_1.default data={(0, getGPUKnownData_1.default)(data, gpuKnownDataValues)}/>
      <contextBlock_1.default data={(0, getUnknownData_1.default)(data, [...gpuKnownDataValues, ...gpuIgnoredDataValues])}/>
    </react_1.Fragment>);
};
exports.default = GPU;
//# sourceMappingURL=gpu.jsx.map