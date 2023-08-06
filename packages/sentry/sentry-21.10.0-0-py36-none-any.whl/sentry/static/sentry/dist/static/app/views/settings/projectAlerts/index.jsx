Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const ProjectAlerts = ({ children, organization }) => (<access_1.default organization={organization} access={['project:write']}>
    {({ hasAccess }) => (<feature_1.default organization={organization} features={['incidents']}>
        {({ hasFeature: hasMetricAlerts }) => (<React.Fragment>
            {React.isValidElement(children) &&
                React.cloneElement(children, {
                    organization,
                    canEditRule: hasAccess,
                    hasMetricAlerts,
                })}
          </React.Fragment>)}
      </feature_1.default>)}
  </access_1.default>);
exports.default = ProjectAlerts;
//# sourceMappingURL=index.jsx.map