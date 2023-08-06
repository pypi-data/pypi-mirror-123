Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const sentryTypes_1 = (0, tslib_1.__importDefault)(require("app/sentryTypes"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const withOrganization = (WrappedComponent) => { var _a; return _a = class extends React.Component {
        render() {
            const _a = this.props, { organization } = _a, props = (0, tslib_1.__rest)(_a, ["organization"]);
            return (<WrappedComponent {...Object.assign({ organization: organization !== null && organization !== void 0 ? organization : this.context.organization }, props)}/>);
        }
    },
    _a.displayName = `withOrganization(${(0, getDisplayName_1.default)(WrappedComponent)})`,
    _a.contextTypes = {
        organization: sentryTypes_1.default.Organization,
    },
    _a; };
exports.default = withOrganization;
//# sourceMappingURL=withOrganization.jsx.map