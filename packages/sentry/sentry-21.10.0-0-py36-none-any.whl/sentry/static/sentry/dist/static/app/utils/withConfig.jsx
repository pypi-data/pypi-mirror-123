Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * Higher order component that passes the config object to the wrapped
 * component
 */
function withConfig(WrappedComponent) {
    const Wrapper = props => {
        const config = (0, useLegacyStore_1.useLegacyStore)(configStore_1.default);
        const allProps = Object.assign({ config }, props);
        return <WrappedComponent {...allProps}/>;
    };
    Wrapper.displayName = `withConfig(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return Wrapper;
}
exports.default = withConfig;
//# sourceMappingURL=withConfig.jsx.map