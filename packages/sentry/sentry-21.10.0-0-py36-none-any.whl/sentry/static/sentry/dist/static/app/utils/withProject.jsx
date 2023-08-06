Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const sentryTypes_1 = (0, tslib_1.__importDefault)(require("app/sentryTypes"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * Currently wraps component with project from context
 */
const withProject = (WrappedComponent) => { var _a; return _a = class extends React.Component {
        render() {
            const _a = this.props, { project } = _a, props = (0, tslib_1.__rest)(_a, ["project"]);
            return (<WrappedComponent {...Object.assign({ project: project !== null && project !== void 0 ? project : this.context.project }, props)}/>);
        }
    },
    _a.displayName = `withProject(${(0, getDisplayName_1.default)(WrappedComponent)})`,
    _a.contextTypes = {
        project: sentryTypes_1.default.Project,
    },
    _a; };
exports.default = withProject;
//# sourceMappingURL=withProject.jsx.map