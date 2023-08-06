Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const getUnknownData_1 = (0, tslib_1.__importDefault)(require("../getUnknownData"));
const getDeviceKnownData_1 = (0, tslib_1.__importDefault)(require("./getDeviceKnownData"));
const types_1 = require("./types");
const utils_1 = require("./utils");
const deviceKnownDataValues = [
    types_1.DeviceKnownDataType.NAME,
    types_1.DeviceKnownDataType.FAMILY,
    types_1.DeviceKnownDataType.CPU_DESCRIPTION,
    types_1.DeviceKnownDataType.ARCH,
    types_1.DeviceKnownDataType.BATTERY_LEVEL,
    types_1.DeviceKnownDataType.BATTERY_STATUS,
    types_1.DeviceKnownDataType.ORIENTATION,
    types_1.DeviceKnownDataType.MEMORY,
    types_1.DeviceKnownDataType.MEMORY_SIZE,
    types_1.DeviceKnownDataType.FREE_MEMORY,
    types_1.DeviceKnownDataType.USABLE_MEMORY,
    types_1.DeviceKnownDataType.LOW_MEMORY,
    types_1.DeviceKnownDataType.STORAGE_SIZE,
    types_1.DeviceKnownDataType.EXTERNAL_STORAGE_SIZE,
    types_1.DeviceKnownDataType.EXTERNAL_FREE_STORAGE,
    types_1.DeviceKnownDataType.STORAGE,
    types_1.DeviceKnownDataType.FREE_STORAGE,
    types_1.DeviceKnownDataType.SIMULATOR,
    types_1.DeviceKnownDataType.BOOT_TIME,
    types_1.DeviceKnownDataType.TIMEZONE,
    types_1.DeviceKnownDataType.DEVICE_TYPE,
    types_1.DeviceKnownDataType.ARCHS,
    types_1.DeviceKnownDataType.BRAND,
    types_1.DeviceKnownDataType.CHARGING,
    types_1.DeviceKnownDataType.CONNECTION_TYPE,
    types_1.DeviceKnownDataType.ID,
    types_1.DeviceKnownDataType.LANGUAGE,
    types_1.DeviceKnownDataType.MANUFACTURER,
    types_1.DeviceKnownDataType.ONLINE,
    types_1.DeviceKnownDataType.SCREEN_DENSITY,
    types_1.DeviceKnownDataType.SCREEN_DPI,
    types_1.DeviceKnownDataType.SCREEN_RESOLUTION,
    types_1.DeviceKnownDataType.SCREEN_HEIGHT_PIXELS,
    types_1.DeviceKnownDataType.SCREEN_WIDTH_PIXELS,
    types_1.DeviceKnownDataType.MODEL,
    types_1.DeviceKnownDataType.MODEL_ID,
    types_1.DeviceKnownDataType.RENDERED_MODEL,
];
const deviceIgnoredDataValues = [];
function Device({ data, event }) {
    const inferredData = (0, utils_1.getInferredData)(data);
    return (<react_1.Fragment>
      <contextBlock_1.default data={(0, getDeviceKnownData_1.default)(event, inferredData, deviceKnownDataValues)}/>
      <contextBlock_1.default data={(0, getUnknownData_1.default)(inferredData, [
            ...deviceKnownDataValues,
            ...deviceIgnoredDataValues,
        ])}/>
    </react_1.Fragment>);
}
exports.default = Device;
//# sourceMappingURL=device.jsx.map