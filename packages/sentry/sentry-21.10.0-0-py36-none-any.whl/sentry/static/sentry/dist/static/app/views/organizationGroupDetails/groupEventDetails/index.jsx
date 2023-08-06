Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupEventDetailsContainer = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const environments_1 = require("app/actionCreators/environments");
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const organizationEnvironmentsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationEnvironmentsStore"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const groupEventDetails_1 = (0, tslib_1.__importDefault)(require("./groupEventDetails"));
class GroupEventDetailsContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = organizationEnvironmentsStore_1.default.get();
    }
    componentDidMount() {
        this.environmentUnsubscribe = organizationEnvironmentsStore_1.default.listen(data => this.setState(data), undefined);
        const { environments, error } = organizationEnvironmentsStore_1.default.get();
        if (!environments && !error) {
            (0, environments_1.fetchOrganizationEnvironments)(this.props.api, this.props.organization.slug);
        }
    }
    componentWillUnmount() {
        if (this.environmentUnsubscribe) {
            this.environmentUnsubscribe();
        }
    }
    render() {
        if (this.state.error) {
            return (<loadingError_1.default message={(0, locale_1.t)("There was an error loading your organization's environments")}/>);
        }
        // null implies loading state
        if (!this.state.environments) {
            return <loadingIndicator_1.default />;
        }
        const _a = this.props, { selection } = _a, otherProps = (0, tslib_1.__rest)(_a, ["selection"]);
        const environments = this.state.environments.filter(env => selection.environments.includes(env.name));
        return <groupEventDetails_1.default {...otherProps} environments={environments}/>;
    }
}
exports.GroupEventDetailsContainer = GroupEventDetailsContainer;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withGlobalSelection_1.default)(GroupEventDetailsContainer)));
//# sourceMappingURL=index.jsx.map