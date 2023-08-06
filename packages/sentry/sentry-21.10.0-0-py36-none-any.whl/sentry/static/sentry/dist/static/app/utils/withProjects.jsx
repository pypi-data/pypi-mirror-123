Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * Higher order component that uses ProjectsStore and provides a list of projects
 */
function withProjects(WrappedComponent) {
    class WithProjects extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                projects: projectsStore_1.default.getAll(),
                loading: projectsStore_1.default.isLoading(),
            };
            this.unsubscribe = projectsStore_1.default.listen(() => this.setState({
                projects: projectsStore_1.default.getAll(),
                loading: projectsStore_1.default.isLoading(),
            }), undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        render() {
            return (<WrappedComponent {...this.props} projects={this.state.projects} loadingProjects={this.state.loading}/>);
        }
    }
    WithProjects.displayName = `withProjects(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithProjects;
}
exports.default = withProjects;
//# sourceMappingURL=withProjects.jsx.map