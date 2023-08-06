Object.defineProperty(exports, "__esModule", { value: true });
exports.loadDeviceListModule = exports.deviceNameMapper = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
function deviceNameMapper(model, iOSDeviceList) {
    const modelIdentifier = model.split(' ')[0];
    const modelId = model.split(' ').splice(1).join(' ');
    const modelName = iOSDeviceList.generationByIdentifier(modelIdentifier);
    return modelName === undefined ? model : modelName + ' ' + modelId;
}
exports.deviceNameMapper = deviceNameMapper;
function loadDeviceListModule() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        return Promise.resolve().then(() => (0, tslib_1.__importStar)(require('ios-device-list')));
    });
}
exports.loadDeviceListModule = loadDeviceListModule;
/**
 * This is used to map iOS Device Names to model name.
 * This asynchronously loads the ios-device-list library because of its size
 */
class DeviceName extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            iOSDeviceList: null,
        };
    }
    componentDidMount() {
        // This is to handle react's warning on calling setState for unmounted components
        // Since we can't cancel promises, we need to do this
        this._isMounted = true;
        // This library is very big, so we are codesplitting it based on size and
        // the relatively small utility this library provides
        loadDeviceListModule().then(iOSDeviceList => {
            if (!this._isMounted) {
                return;
            }
            this.setState({ iOSDeviceList });
        });
    }
    componentWillUnmount() {
        this._isMounted = false;
    }
    render() {
        const { value, children } = this.props;
        const { iOSDeviceList } = this.state;
        // value can be undefined, need to return null or else react throws
        if (!value) {
            return null;
        }
        // If library has not loaded yet, then just render the raw model string, better than empty
        if (!iOSDeviceList) {
            return value;
        }
        const deviceName = deviceNameMapper(value, iOSDeviceList);
        return (<span data-test-id="loaded-device-name">
        {children ? children(deviceName) : deviceName}
      </span>);
    }
}
exports.default = DeviceName;
//# sourceMappingURL=deviceName.jsx.map