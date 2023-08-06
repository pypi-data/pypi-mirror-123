Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const experimentConfig_1 = require("app/data/experimentConfig");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const experiments_1 = require("app/types/experiments");
const analytics_1 = require("app/utils/analytics");
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * A HoC wrapper that injects `experimentAssignment` into a component
 *
 * This wrapper will automatically log exposure of the experiment upon
 * receiving the componentDidMount lifecycle event.
 *
 * For organization experiments, an organization object must be provided to the
 * component. You may wish to use the withOrganization HoC for this.
 *
 * If exposure logging upon mount is not desirable, The `injectLogExperiment`
 * option may be of use.
 *
 * NOTE: When using this you will have to type the `experimentAssignment` prop
 *       on your component. For this you should use the `ExperimentAssignment`
 *       mapped type.
 */
function withExperiment(Component, { experiment, injectLogExperiment }) {
    var _a;
    return _a = class extends React.Component {
            constructor() {
                super(...arguments);
                this.logExperiment = () => (0, analytics_1.logExperiment)({
                    key: experiment,
                    organization: this.getProps().organization,
                });
            }
            // NOTE(ts): Because of the type complexity of this HoC, typescript
            // has a hard time understanding how to narrow Experiments[E]['type']
            // when we type assert on it.
            //
            // This means we have to do some typecasting to massage things into working
            // as expected.
            //
            // We DO guarantee the external API of this HoC is typed accurately.
            componentDidMount() {
                if (!injectLogExperiment) {
                    this.logExperiment();
                }
            }
            getProps() {
                return this.props;
            }
            get config() {
                return experimentConfig_1.experimentConfig[experiment];
            }
            get experimentAssignment() {
                const { type } = this.config;
                if (type === experiments_1.ExperimentType.Organization) {
                    const key = experiment;
                    return this.getProps().organization.experiments[key];
                }
                if (type === experiments_1.ExperimentType.User) {
                    const key = experiment;
                    return configStore_1.default.get('user').experiments[key];
                }
                return experimentConfig_1.unassignedValue;
            }
            render() {
                const WrappedComponent = Component;
                const props = Object.assign(Object.assign({ experimentAssignment: this.experimentAssignment }, (injectLogExperiment ? { logExperiment: this.logExperiment } : {})), this.props);
                return <WrappedComponent {...props}/>;
            }
        },
        _a.displayName = `withExperiment[${experiment}](${(0, getDisplayName_1.default)(Component)})`,
        _a;
}
exports.default = withExperiment;
//# sourceMappingURL=withExperiment.jsx.map