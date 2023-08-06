Object.defineProperty(exports, "__esModule", { value: true });
exports.DataStateSwitch = void 0;
const react_1 = require("react");
function DataStateSwitch(props) {
    if (props.isLoading && props.loadingComponent) {
        return props.loadingComponent;
    }
    if (props.isErrored) {
        return props.errorComponent;
    }
    if (!props.hasData) {
        return props.emptyComponent;
    }
    return <react_1.Fragment>{props.dataComponents}</react_1.Fragment>;
}
exports.DataStateSwitch = DataStateSwitch;
//# sourceMappingURL=dataStateSwitch.jsx.map