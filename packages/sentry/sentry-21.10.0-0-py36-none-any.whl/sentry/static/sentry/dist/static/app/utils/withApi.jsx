Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
/**
 * XXX: Prefer useApi if you are wrapping a Function Component!
 *
 * React Higher-Order Component (HoC) that provides "api" client when mounted,
 * and clears API requests when component is unmounted.
 *
 * If an `api` prop is provided when the component is invoked it will be passed
 * through.
 */
const withApi = (WrappedComponent, options = {}) => {
    const WithApi = (_a) => {
        var { api: propsApi } = _a, props = (0, tslib_1.__rest)(_a, ["api"]);
        const api = (0, useApi_1.default)(Object.assign({ api: propsApi }, options));
        return <WrappedComponent {...props} api={api}/>;
    };
    WithApi.displayName = `withApi(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithApi;
};
exports.default = withApi;
//# sourceMappingURL=withApi.jsx.map