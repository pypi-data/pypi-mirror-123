Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class AlertsContainer extends react_1.Component {
    render() {
        const { children, organization } = this.props;
        return (<feature_1.default organization={organization} features={['incidents']}>
        {({ hasFeature: hasMetricAlerts }) => (<react_1.Fragment>
            {children && (0, react_1.isValidElement)(children)
                    ? (0, react_1.cloneElement)(children, {
                        organization,
                        hasMetricAlerts,
                    })
                    : children}
          </react_1.Fragment>)}
      </feature_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)(AlertsContainer);
//# sourceMappingURL=index.jsx.map