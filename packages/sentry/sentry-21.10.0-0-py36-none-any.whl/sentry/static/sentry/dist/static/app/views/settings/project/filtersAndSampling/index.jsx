Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const filtersAndSampling_1 = (0, tslib_1.__importDefault)(require("./filtersAndSampling"));
const Index = (_a) => {
    var { organization } = _a, props = (0, tslib_1.__rest)(_a, ["organization"]);
    return (<feature_1.default features={['filters-and-sampling']} organization={organization} renderDisabled={() => (<featureDisabled_1.default alert={panels_1.PanelAlert} features={organization.features} featureName={(0, locale_1.t)('Filters & Sampling')}/>)}>
    <access_1.default organization={organization} access={['project:write']}>
      {({ hasAccess }) => (<filtersAndSampling_1.default {...props} hasAccess={hasAccess} organization={organization}/>)}
    </access_1.default>
  </feature_1.default>);
};
exports.default = (0, withOrganization_1.default)(Index);
//# sourceMappingURL=index.jsx.map